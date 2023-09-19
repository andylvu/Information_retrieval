import re
import json

json_file = 'ksu5.json'
# Specify the encoding (e.g., 'utf-8') when opening the file
with open(json_file, 'r', encoding='utf-8') as file:
    data = json.load(file)  # Use json.load() directly to parse JSON



# find the average length of webpages counted in tokens
# the length of the webpage is only counted using the length of text of the body
def avg_len(data):
    total_tokens = 0
    total_webpages = len(data)
    # iterate through the data
    for webpage in data:
        text = webpage.get('body')
        tokens = text.strip().split()
        total_tokens += len(tokens)

    avg_token_len = total_tokens / total_webpages

    return avg_token_len
        
# top 10 most frequent emails
def top_emails(data):
    all_emails = []
    for webpage in data:
        email = webpage.get('emails')
    return

mail1 = data[18].get('emails')
print(mail1)