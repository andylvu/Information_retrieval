"""
Simple indexer and search engine built on an inverted-index and the BM25 ranking algorithm.
"""
import os
from collections import defaultdict
import pickle
import math
from tqdm import tqdm
from nltk import pos_tag
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from datasets import load_dataset
import code
# commented out the import and download of the stopwords and word net as these only needed to be run once
# import nltk
# nltk.download('wordnet')
# nltk.download('stopwords')

# indexer class
class Indexer:
    dbfile = "./ir.idx"  # This is the index file you will create and manager for indexing

    def __init__(self):
        # data structures to store and manage elements from the search engine

        self.tok2idx = {}                       # dictionary for token to id mapping
        self.idx2tok = {}                       # dictionary for id to token mapping
        self.postings_lists = {}                # term to postings list mapping
        self.docs = []                          # list to store document information
        self.raw_ds = []                        # list to store raw documents from search result
        self.corpus_stats = { 'avgdl': 0 }      # dictionary for corpus level statistics
        self.stopwords = stopwords.words('english') # list of stopwords from NLTK library of stopwords

        if os.path.exists(self.dbfile):
            # if the index file exist, load the data from it
            self.load_index_data()
            
            pass
        else:
            # if the index file does not exist, load and preprocess the dataset

            ds = load_dataset("cnn_dailymail", '3.0.0', split="test")
            self.raw_ds = ds['article']
            self.clean_text(self.raw_ds)
            self.create_postings_lists()

    def load_index_data(self):
        # load the data from the index file using pickle
        # open the index file in binary read mode 'rb'
        # use pickle.load to deserialize the data 
        with open (self.dbfile, 'rb') as f:
            index_data = pickle.load(f)

        # populate the data structures with the loaded data
        self.tok2idx = index_data['tok2idx']
        self.idx2tok = index_data['idx2tok']
        self.postings_lists = index_data['postings_lists']
        self.docs = index_data['docs']
        self.raw_ds = index_data['raw_ds']
        self.corpus_stats = index_data['corpus_stats']
        self.stopwords = index_data['stopwords']

    def save_index_data(self):
        # create a dictionary to hold the index data
        index_data = {
            'tok2idx': self.tok2idx,
            'idx2tok': self.idx2tok,
            'postings_lists': self.postings_lists,
            'docs': self.docs,
            'raw_ds': self.raw_ds,
            'corpus_stats': self.corpus_stats,
            'stopwords': self.stopwords
        }

        # serialize and save index data to the index file using pickle
        with open(self.dbfile, 'wb') as f:
            pickle.dump(index_data, f)
            

    def clean_text(self, lst_text, query=False):
        # Initialize tokenizer and lemmatizer
        tokenizer = RegexpTokenizer(r'\w+')
        lemmatizer = WordNetLemmatizer()

        # Initialize a list for the cleaned text
        cleaned_text = [] 

        for text in lst_text:
            tokens = tokenizer.tokenize(text.lower())  # Tokenize and lowercase

            if not query:
                # Remove stopwords for indexing (not for query)
                tokens = [token for token in tokens if token not in self.stopwords]

            lemmatized_tokens = []
            for token in tokens:
                lemmatized_tokens.append(lemmatizer.lemmatize(token))  # Lemmatize

            # Join the tokens back into a single string
            cleaned_text.append(" ".join(lemmatized_tokens))

        if not query:
            self.docs = cleaned_text  # Assign the cleaned text to self.docs for indexing

        return cleaned_text

    def create_postings_lists(self):
        # Initialize data structures for postings and document statistics
        self.postings_lists = defaultdict(list)
        doc_lengths = []
        df = defaultdict(int)

        for doc_id, doc_text in enumerate(self.docs):
            # Tokenize the document
            tokens = doc_text.split()

            # Update document length
            doc_length = len(tokens)
            doc_lengths.append(doc_length)

            # Compute document frequencies (df)
            unique_tokens = set(tokens)
            for token in unique_tokens:  # Use unique tokens to count each term only once per document
                df[token] += 1

            # Create postings list
            for token in unique_tokens:  # Use unique tokens to create postings list
                self.postings_lists[token].append(doc_id)

        # Compute the average document length (avgdl)
        total_doc_length = sum(doc_lengths)
        num_docs = len(self.docs)
        avgdl = total_doc_length / num_docs
        self.corpus_stats['avgdl'] = avgdl

        # Create an index data dictionary to store postings lists, document frequencies, and avgdl
        index_data = {
            'postings_lists': dict(self.postings_lists),
            'document_frequencies': dict(df),
            'avgdl': avgdl
        }


class SearchAgent:
    k1 = 1.5                # BM25 parameter k1 for tf saturation
    b = 0.75                # BM25 parameter b for document length normalization

    def __init__(self, indexer):
        
        self.indexer = indexer

    def query(self, q_str):
        # process the query using the same clean_text process
        cleaned_query = self.indexer.clean_text([q_str], query=True)[0]

        # Calculate BM25 scores for documents
        results = self.calculate_bm25_scores(cleaned_query)

        # Sort the results by scores in descending order
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

        # display results
        self.display_results(sorted_results)

    def calculate_bm25_scores(self, cleaned_query):
        # Create a dictionary to store document scores
        results = {}

        # Calculate IDF (inverse document frequency) for each query term
        query_terms = cleaned_query.split()
        idf_values = {}
        for term in query_terms:
            df_term = len(self.indexer.postings_lists.get(term, []))
            idf_term = math.log((len(self.indexer.docs) - df_term + 0.5) / (df_term + 0.5) + 1.0)
            idf_values[term] = idf_term

        # Iterate through documents and calculate scores
        for doc_id, doc_text in enumerate(self.indexer.docs):
            doc_score = 0.0

            # Tokenize the document
            doc_terms = doc_text.split()

            # Calculate document length (|D|)
            doc_length = len(doc_terms)

            # Calculate average document length (avgdl) from corpus stats
            avgdl = self.indexer.corpus_stats['avgdl']

            for term in query_terms:
                # Calculate TF (term frequency) for the term in the document
                tf_term = doc_terms.count(term)

                # Calculate BM25 score for the term in the document
                score_term = (idf_values[term] * tf_term * (self.k1 + 1)) / (
                    tf_term + self.k1 * ((1 - self.b) + self.b * (doc_length / avgdl))
                )

                doc_score += score_term

            results[doc_id] = doc_score

        return results

    def display_results(self, results):

        for docid, score in results[:5]:  # print top 5 results
            print(f'\nDocID: {docid}')
            print(f'Score: {score}')
            print('Article:')
            print(self.indexer.raw_ds[docid])



if __name__ == "__main__":
    i = Indexer()           # instantiate an indexer
    q = SearchAgent(i)      # document retriever
    code.interact(local=dict(globals(), **locals())) # interactive shell