# Correxy-AI

A lightweight Discord bot that suggests what a user likely intended to
say when spelling inconsistencies or typing errors are detected.

Built using Google Gemini, this bot is designed as an assistive writing
tool to support clearer communication, especially for users who benefit
from spelling and text assistance (including dyslexia-friendly use
cases).

------------------------------------------------------------------------

## Features

-   AI-powered text correction using Google Gemini or languagetool
-   Suggests intended meaning without heavily rewriting the user's
    voice
-   Opt-in system (users must explicitly enable it)
-   Lightweight and fast Discord integration
-   Focuses on clarity, not forced correction or tone alteration
-   Works both automatically and manually via command

------------------------------------------------------------------------

## How it works

Once a user enables the bot, it monitors their messages and detects
potential spelling inconsistencies or unclear phrasing.

When an issue is detected, the bot responds with a suggested correction,
helping the user express their intended message more clearly---without
changing their tone or intent.

------------------------------------------------------------------------

## Commands

### Enable autocorrect

!ac on

### Disable autocorrect

!ac off

### Manually fix text

!correx `<text>`{=html}

Example: !correx i fetl this way

------------------------------------------------------------------------

## Consent & Privacy

This bot is fully opt-in, opt-out.

-   Users must enable autocorrect manually
-   Only opted-in users are processed
-   Users can disable it at any time
-   No external logging of user messages

------------------------------------------------------------------------

## AI Model

Correxy-AI uses Google Gemini to understand context and correct text
intelligently.

It can handle phonetic spelling mistakes, missing or swapped words,
letters, word order issues, context-aware corrections and partial
sentence reconstruction.

------------------------------------------------------------------------

## Setup

### 1. Clone the repository

git clone https://github.com/scifimegahypee/correxy-ai.git cd
correxy-ai

### 2. Install dependencies

pip install discord.py python-dotenv google-genai

### 3. Create a .env file

DISCORD_TOKEN=your_discord_bot_token 
GEMINI_API_KEY=your_gemini_api_key

### 4. Run the bot

python v1.py

------------------------------------------------------------------------

## Tech Stack

-   Python
-   Discord.py
-   Google Gemini API
-   JSON-based local config storage

------------------------------------------------------------------------

## Design Philosophy

Correxy-AI is built around three principles:

-   Assist, don't overwrite
-   Respect user intent and voice
-   Make communication easier, not forced

The bot is designed to support users---not correct them in an intrusive way.

------------------------------------------------------------------------

## Disclaimer

This bot provides AI-generated suggestions only. It will not
automatically modify user messages unless explicitly configured 
to do so by the user in future.

<img src="https://github.com/ScifiMegaHype/correxy-ai/blob/main/version1.jpg" alt="Alt Text" width="1115" height="977">
