# Project Information

## Core Purpose
Kanha AI-Bot serves as a digital companion providing advice for modern-day struggles (such as anxiety, career stress, relationships, and imposter syndrome) through the philosophical lens of the Bhagavad Gita. It aims to deliver short, punchy, and conversational guidance in Hinglish, acting as a virtual *Saarthi* (charioteer) and avoiding standard AI clichés.

## Cloud/AI Services & Resource Utilization (Azure)
The project heavily relies on a Microsoft Azure Resource Group (`Kanha_Bot`) for its cloud infrastructure. Here are the specific resources used and their roles:

1. **Azure OpenAI (`Personal-Bot`)**: 
   - **Role**: The core brain of the chatbot.
   - **Use**: Deploys the GPT-4o model that processes user prompts alongside retrieved context to generate the persona-based, empathetic responses mimicking Lord Krishna.

2. **Azure AI Search (`krishna-search`)**: 
   - **Role**: The Retrieval-Augmented Generation (RAG) engine.
   - **Use**: Indexes the Bhagavad Gita text (`Gita-book` index). When a user asks a question, this service searches for the most relevant verses or philosophical context to feed to the OpenAI model.

3. **App Service (`Mera-Kanha`)**: 
   - **Role**: The hosting environment.
   - **Use**: Hosts the lightweight Flask web server and the Telegram bot background thread. This allows the bot to run continuously in the cloud and serves the web chat interface.

4. **Storage Account (`krishnastorage2026`)**: 
   - **Role**: Data repository.
   - **Use**: Stores the raw documents (e.g., PDFs or text files of the Bhagavad Gita) that are ingested and chunked by the Azure AI Search indexer. It can also host static assets for the web application.

5. **Azure Cosmos DB Account (`db-mera-kanhaiya`)**: 
   - **Role**: NoSQL Database.
   - **Use**: Serves as a fast, scalable database. In this architecture, it is typically used for storing conversation histories, maintaining user state/sessions, and application logging.

6. **Managed Identity (`Mera-Kanha-id-aa98`)**: 
   - **Role**: Security and Authentication.
   - **Use**: Provides a secure, passwordless identity for the App Service (`Mera-Kanha`) to securely authenticate and access other Azure resources (like Cosmos DB, Storage, and AI services) without needing to hardcode connection strings or secrets in the code.

## File Manifest & Usage

- **`main.py`**: The core application entry point. It contains the logic for:
  - Querying Azure AI Search for relevant Gita context.
  - Constructing the prompt and calling Azure OpenAI.
  - Managing the Telegram bot commands and message routing via `pyTelegramBotAPI`.
  - Running a Flask web server to satisfy Azure App Service port requirements and serve the web UI.

- **`requirements.txt`**: Lists all Python package dependencies required to run the project (`pyTelegramBotAPI`, `requests`, `python-dotenv`, `flask`).

- **`dataset_generator.py`**: A synthetic data generation script. It uses a hardcoded list of over 100 modern life problems (e.g., "Dealing with a difficult roommate", "Fear of being laid off") and calls Azure OpenAI to automatically generate example conversations. This is used for fine-tuning or evaluating the model's persona.

- **`fixingJSON.py` & `jsonValidatation.py`**: Data cleaning utilities. Because LLMs sometimes output malformed or markdown-wrapped JSON, these scripts extract and properly format the `messages` blocks from the raw generated `.jsonl` dataset into the strict JSONL format required for OpenAI fine-tuning.

- **`krishna_dataset_fixed.jsonl`**: The final, cleaned dataset containing the generated conversational examples, ready for use in fine-tuning the Azure OpenAI deployment.

- **`.env` & `.env.example`**: Configuration files. They store sensitive environment variables such as the `TELEGRAM_TOKEN`, Azure API keys, and endpoint URLs securely, keeping them out of the source code.

- **`bot.py` / `temp.py` / `temp.txt`**: Auxiliary files used for experimental testing, isolated logic testing, or temporary scratchpads during development.

- **`templates/`**: A directory containing the HTML templates (specifically `index.html`) rendered by the Flask server to provide a web-based chat interface as an alternative to Telegram.
