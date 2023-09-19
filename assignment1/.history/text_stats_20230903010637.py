import re
import json

json_file = 'ksu5.json'
# Specify the encoding (e.g., 'utf-8') when opening the file
with open(json_file, 'r', encoding='utf-8') as file:
    data = json.load(file)  # Use json.load() directly to parse JSON

total_tokens = 0
total_webpages = 0
webpage1 = data[0]
text = webpage1.get('body')
tokens = text.strip().split()
print(len(tokens))

# Iterate through the list of webpages
#for webpage in data:
    # Access the webpage content from the JSON data (modify the key as needed)
#    content = webpage.get('body', '')

    # Tokenize the content using strip() and split by whitespace
#    tokens = content.strip().split()

    # Update counters
#    total_tokens += len(tokens)
#    total_webpages += 1

# Calculate the average length of webpages in tokens
#average_length = total_tokens / total_webpages if total_webpages > 0 else 0

#print(f"Total Webpages: {total_webpages}")
#print(f"Total Tokens: {total_tokens}")
#print(f"Average Length in Tokens: {average_length}")