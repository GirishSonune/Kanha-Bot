from openai import AzureOpenAI

client = AzureOpenAI(api_key="[ENCRYPTION_KEY]", api_version="2024-05-01-preview", azure_endpoint="https://mera-kanha.openai.azure.com/")

# This bypasses the UI and uploads the file directly
client.files.create(file=open("krishna_dataset_fixed.jsonl", "rb"), purpose="fine-tune")