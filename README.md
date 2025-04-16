# CusChatAI

CusChatAI is a chatbot to assist customers and to help businesses to have a better support service

Anne's favorite quote: "The future is as bright as your faith." Thomas S. Monson

Juan Plasencia:
Allow [the Lord] to make more of you than you can make of yourself on your own. Treasure His involvement.
Ronald A. Rasband

“It is mentally rigorous to strive to look unto Him in every thought. But, when we do, our doubts and fears flee.”—President Russell M. Nelson, “Drawing the Power of Jesus Christ into Our Lives”
-Matthew Perkins

Timoteo Tapia:
"Obedience brings success; exact obedience brings miracles."Russell M. Nelson (Kevin Tapia)

## Tech Stack:

- Telegram for interface platform (Matthew Perkins). Telegram has a bot API called Telegram Bot, which allows for easy building of chatbots and choosing what functionaility you want to build for your chatbot. We will use the Telegram Bot API for basic interfacing with the user, and will integrate an AI model with Telegram Bot to allow for natural language to be used during a conversation.

### Links:

- [Telegram Bot](https://core.telegram.org/bots)
- [Telegram Bot API Docs](https://core.telegram.org/bots/api)

Standup Week 03:
LLMs Mode Integration with Telegram (Juan Plasencia)
When investigating the integration of LLMs with Telegram, it has been found that it is necessary to design an API that integrates the interface services offered by Telegram with those of a back-end that consumes the pre-trained models in the cloud, and these can return the necessary information to the chat bot.

## Hosting Platforms for CusChatAI

For hosting the backend of the CusChatAI project, we researched several hosting platforms to identify the best option based on scalability, ease of use, integration capabilities, and cost-effectiveness. Below are the platforms we considered and the reasons for selecting the final choice.

### Platforms Considered:

1. **Vercel**

   - **Pros**:
     - Easy deployment with GitHub integration.
     - Excellent for serverless functions, making it a good fit for a chatbot-based application.
     - Automatic scaling.
     - Free tier with generous usage limits.
     - Fast global CDN for low-latency responses.
   - **Cons**:
     - Some limitations on serverless execution duration and memory on free tier.

2. **Render**

   - **Pros**:
     - Simple deployment with auto-scaling.
     - Free tier available for small projects.
     - Supports databases and backend services.
   - **Cons**:
     - Not as widely known as other platforms like AWS, so some documentation might be lacking.

## Prerequisites

- Python 3.10 or higher
- Poetry for dependency management
- Telegram Bot Token
- Other API keys as required by your application

## Environment Variables

Before running the application, make sure you have set the following environment variables:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GOOGLE_SERVICE_ACCOUNT_JSON=path_to_service_account_json_file
GOOGLE_CALENDAR_ID=your_google_calendar_id
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

You can create a `.env` file in the root directory of the project with these variables.

## Local Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/TimoteoTapia/cuschatai/commits/kevin/
```

### 2. Install dependencies using Poetry

```bash
# Install Poetry if you don't have it
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
```

### 3. Run the application locally

```bash
# Activate the virtual environment
poetry shell

# Run the bot
python telegram_app.py
```

The bot will start in polling mode and begin responding to messages on Telegram.

## Project Structure

```
├── src/
│   ├── app/
│   │   ├── handlers.py   # Telegram bot handlers
│   │   ├── config.py     # Configuration and environment variables
│   │   └── ...
├── telegram_app.py       # Main application file
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Troubleshooting

If you encounter issues with the bot:

1. Check that all environment variables are correctly set
2. Verify that your Telegram bot token is valid and the bot is properly configured
