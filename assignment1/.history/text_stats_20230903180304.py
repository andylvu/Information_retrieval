import re
import json
from collections import Counter
import nltk
from nltk.corpus import stopwords
from matplotlib import pyplot as plt

# download nltk lirbary of stopwords
nltk.download('stopwords')

json_file = 'ksu5.json'
# Specify the encoding (e.g., 'utf-8') when opening the file
with open(json_file, 'r', encoding='utf-8') as file:
    data = json.load(file)  # Use json.load() directly to parse JSON

# find the average length of webpages counted in tokens
# the length of the webpage is only counted using the length of text of the body
# start with total tokens as 0
# get text from the body of the webpages, and use text.strip().split() to remove whitespaces and tokenize words
# add the number of tokens to the total number of tokens
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

# find the percentage of webpages that have at least one email
# count number of webpages with atleast one email
# divide number of webpages with one email by total number of webpages
def percent_have_email(data):
    total_webpages = len(data)
    webpage_with = 0
    for webpage in data:
        if len(webpage.get('emails', [])) > 0:
            webpage_with += 1

    percent = webpage_with / total_webpages * 100
    return percent

# word frequencies are calculated using the body text of the webpages
# considered against using the title of the webpages as well because that would lead to abundant words such as Kennesaw, state, university, etc
# using a set to keep word uniqueness
# words obtained from splitting the text
# update the set and count the vocabulary to obtain the top 30 words
def word_frequencies_nostop(data):
    vocabulary = set()
    for webpage in data:
        text = webpage.get('body', '')
        words = text.split()
        vocabulary.update(words)

    word_counter = Counter(vocabulary)
    top_words = word_counter.most_common(30)
    
    return top_words

# remove stop words from the text
# create an empty list for the corpus
# go through each webpage and obtain the body text
# tokenize each word using text.strip().split() instead of nltk word_tokenize
# check each token and compare it using its lowercase version to the stopword library
# if the word is not in the stopword libary add it to the filtered text string
# this string of filtered text is added to the corpus
# final corpus is obtained by joining all the corpus together sepearated by a space
# final corpus is tokenized using text.strip().split() instead of nltk word_tokenize
# word counter is counted using Counter on the final words
# top 30 words are obtained and returned
def word_frequencies_withstop(data):
    corpus = []
    for webpage in data:
        text = webpage.get('body', '')
        words = text.strip().split()
        filtered_words = [word for word in words if word.lower() not in stopwords.words('english')]
        filtered_text = ' '.join(filtered_words)
        corpus.append(filtered_text)

    final_corpus = ' '.join(corpus)
    final_words = final_corpus.strip().split()

    word_counter = Counter(final_words)
    top_words = word_counter.most_common(30)
    return top_words

print('average document length in tokens: ', avg_len(data))
print('top 10 most frequent emails: ', top_emails(data))
print('percentage of webpages that contain atleast one email: ', percent_have_email(data))
print('top 30 words of all webpages without stopword removal: ', word_frequencies_nostop(data))
print(' top 30 words of all webpages with stopword removal: ', word_frequencies_withstop(data))
