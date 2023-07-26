import string

import spacy
from collections import Counter

import test_text

def generate_semantic_core(text, num_keywords=10):
    # Load spaCy
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)
    # Извлечение лемматизированных слов с учетом части речи, исключая стоп-слова и знаки препинания
    filtered_words = [token.text.lower() for token in doc if not token.is_stop and token.text not in string.punctuation]
    word_freq = Counter(filtered_words)
    # Извлечение наиболее частых слов (как ключевые слова)
    keywords = word_freq.most_common(num_keywords)

    return keywords

print(generate_semantic_core(text=test_text.text.strip()))