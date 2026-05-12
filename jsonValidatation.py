import os

input_file = "krishna_dataset.jsonl"
output_file = "krishna_dataset_fixed.jsonl"

try:
    # Read using 'latin-1' to bypass the 0x97 error
    with open(input_file, 'r', encoding='latin-1') as f:
        content = f.read()

    # Write back as clean utf-8
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Success! Use '{output_file}' for your upload.")
except Exception as e:
    print(f"Error fixing file: {e}")