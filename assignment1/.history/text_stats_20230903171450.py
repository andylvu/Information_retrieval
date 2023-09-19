import re
import json
from collections import Counter

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
# an empty list of all_emails to store them
# go through each page of the json file and extract the emails
# since each webpage has its own list of emails, that list needs to be checked for uniqueness
# each unique email is added to the overall all_emails
# count each unique email and find return the top ten
def top_emails(data):
    all_emails = []
    for webpage in data:
        emails = webpage.get('emails')
        for email in emails:
            if email not in all_emails:
                all_emails.append(email)
    email_counter = Counter(all_emails)
    top_emails = email_counter.most_common(10)

    return top_emails

def percent_have_email(data):
    total_webpages = data(len)
    webpage_without = 0
    for webpage in data:
        if len(webpage.get('email')) == 0:
            webpage_without += 1

    percent = webpage_without / total_webpages
    return percent