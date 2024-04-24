import os
import re
import docx
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx


def read_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension == ".txt":
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    elif file_extension == ".docx":
        doc = docx.Document(file_path)
        return " ".join([paragraph.text for paragraph in doc.paragraphs])
    else:
        raise ValueError("Unsupported file format. Supported formats: .txt, .docx")
        

def write_summary_to_file(summary, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(summary)


def read_article(text):
    # Use regular expressions to split the text into sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    return sentences


def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []

    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    for w in sent1:
        if w not in stopwords:
            vector1[all_words.index(w)] += 1

    for w in sent2:
        if w not in stopwords:
            vector2[all_words.index(w)] += 1

    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                similarity_matrix[i][j] = sentence_similarity(sentences[i], sentences[j], stop_words)

    return similarity_matrix

def generate_summary(text, top_n=5):
    stop_words = stopwords.words('english')
    summarize_text = []

    sentences = read_article(text)

    sentence_similarity_matrix = build_similarity_matrix(sentences, stop_words)

    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)

    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentences[i][1]))

    return " ".join(summarize_text)


def generate_summary_from_text(input_text, top_n=3):
    stop_words = stopwords.words('english')
    sentences = read_article(input_text)
    sentence_similarity_matrix = build_similarity_matrix(sentences, stop_words)
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    summarize_text = [ranked_sentence[1] for ranked_sentence in ranked_sentences[:top_n]]
    return " ".join(summarize_text)