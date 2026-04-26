import os
import requests
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
from manage_consents import load_config, save_config
from backend import gemini_correct

class TempMessage:
    def __init__(self, content):
        self.content = content

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COMMANDS = ["!ac", "!correx"]

handler = logging.FileHandler(filename='Discord_D1.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

def correct_text(text):
    url = "https://api.languagetool.org/v2/check"
    data = {
        "text": text,
        "language": "en-US"
    }
    r = requests.post(url, data=data).json()

    corrected = text
    for match in r.get("matches", []):
        if match["replacements"]:
            wrong = match["context"]["text"][match["context"]["offset"]:
                                             match["context"]["offset"] + match["context"]["length"]]
            right = match["replacements"][0]["value"]
            corrected = corrected.replace(wrong, right, 1)

    return corrected

def correct_text_gemini(text):
    return gemini_correct(text)

def process_corrections(message) -> tuple[str, bool]:
    used_gemini = False
    try:
        corrected = correct_text_gemini(message.content)
        used_gemini = True
    except Exception:
        logging.error(f"Error correcting text for user {message.author.id}. Falling back to LanguageTool.")
        corrected = correct_text(message.content)

    return corrected, used_gemini

@bot.command()
async def ac(message, mode: str=""): # autocorrect on/off
    config = load_config()
    consented_users = set(config.get("consented_users", []))

    if mode.lower() == "on":
        consented_users.add(message.author.id)
        await message.reply(f"Autocorrect enabled for {message.author.mention}.")
    elif mode.lower() == "off":
        try:
            consented_users.discard(message.author.id)
            await message.reply(f"Autocorrect disabled for {message.author.mention}.")
        except KeyError:
            await message.reply(f"{message.author.mention} is not in the list of users who have given consent.")
    else:
        await message.reply("Use !ac on/off")

    config["consented_users"] = list(consented_users)
    save_config(config)

@bot.command()
async def correx(message, * ,text: str | None = None): # single use correction, no need for consent
    if not text:
        await message.reply("Please provide text to check.")
        return

    temp_message = TempMessage(text)

    corrected, used_gemini = process_corrections(temp_message)

    if corrected != temp_message.content:
        await message.reply(f"Suggested:\n{corrected}")

    print(f"User: {message.author.id} | Used Gemini: {used_gemini}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if not any(message.content.startswith(cmd) for cmd in COMMANDS):
        config = load_config()
        consented_users = set(config.get("consented_users", []))
        has_consent = message.author.id in consented_users

        used_gemini = False

        # Check if user has given consent for autocorrection
        if has_consent:
            corrected, used_gemini = process_corrections(message)

            if corrected != message.content:
                await message.reply(f"Suggested:\n{corrected}")

        print(f"User: {message.author.id} | Has Consent: {has_consent} | Used Gemini: {used_gemini}")

    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to the server and is ready to go!')

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)