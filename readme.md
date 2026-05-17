# Kanha AI-Bot (Mera Kanha)

A spiritual AI chatbot acting as a virtual guide (saarthi), bringing the timeless wisdom of the Bhagavad Gita to modern-day challenges. Built with Python, Azure OpenAI, Azure AI Search, and Telegram.

## Features
- **Telegram Bot Integration**: Accessible via Telegram, providing quick, empathetic, and wise responses in Hinglish.
- **Web Interface**: A lightweight Flask backend serving a web chat UI.
- **Retrieval-Augmented Generation (RAG)**: Uses Azure AI Search to fetch relevant verses or context from the Bhagavad Gita before generating a response.
- **Azure OpenAI Integration**: Powered by GPT-4o, configured to speak with the calm, profound, and timeless tone of Lord Krishna.
- **Custom Dataset Generation**: Includes scripts to generate and clean synthetic data for testing or fine-tuning the AI model.

## Setup & Installation

1. **Clone the repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**
   Create a `.env` file based on `.env.example` with the following variables:
   ```env
   TELEGRAM_TOKEN=your_telegram_bot_token
   AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
   AZURE_OPENAI_KEY=your_azure_openai_key
   SEARCH_ENDPOINT=your_azure_search_endpoint
   SEARCH_KEY=your_azure_search_key
   SEARCH_INDEX_NAME=Gita-book
   ```

## Usage

To start the bot and the web server simultaneously:
```bash
python main.py
```
- The Flask server runs on port 8000 by default (or the `PORT` env variable), satisfying Azure App Service port requirements and serving the web UI.
- The Telegram bot runs concurrently in a background thread via `bot.infinity_polling()`.

## Tools included
- `dataset_generator.py`: Generates synthetic conversation data (modern problems addressed with Gita wisdom) using Azure OpenAI.
- `fixingJSON.py`: Utility script to clean and flatten the generated JSONL files into a valid format.
