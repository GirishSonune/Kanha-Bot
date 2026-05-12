import json
import re

input_file = r"e:\Hight Level Projects\Kanha AI-Bot\krishna_dataset.jsonl"
output_file = r"e:\Hight Level Projects\Kanha AI-Bot\krishna_dataset_fixed.jsonl"

def flatten_jsonl():
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # This regex finds everything between the outer { and } for each conversation
        # Even if it spans multiple lines.
        matches = re.findall(r'\{.*?"messages".*?\}\s*(?=\{|\Z)', content, re.DOTALL)
        
        if not matches:
            print("No valid JSON objects found. Check if your file contains 'messages' keys.")
            return

        with open(output_file, 'w', encoding='utf-8') as f:
            for match in matches:
                try:
                    # Parse the string into a dictionary
                    obj = json.loads(match)
                    # Write it back as a single line with no extra spaces
                    f.write(json.dumps(obj, ensure_ascii=False) + '\n')
                except json.JSONDecodeError:
                    continue # Skip partially matched or broken blocks

        print(f"Done! Successfully flattened {len(matches)} conversations.")
        print(f"New file created: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    flatten_jsonl()