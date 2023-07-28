import re
from collections import Counter

import nltk
import pymorphy2
import spacy
from iso639 import to_name
from langdetect import detect
from nltk import word_tokenize, BigramAssocMeasures, BigramCollocationFinder
from nltk.corpus import stopwords


class TextAnalyzer:
    nltk.download('punkt')
    nltk.download('stopwords')

    def __init__(self, text: str):
        self.text = text
        self.lang = detect(text)
        self.full_lang = to_name(self.lang).lower()

    def get_count_characters(self):
        """Количество символов"""
        count_char = len(self.text)
        return count_char

    def count_characters_without_spaces(self):
        """Количество символов без пробелов	"""
        total_characters_without_spaces = len([char for char in self.text if not char.isspace()])
        return total_characters_without_spaces

    def count_worlds(self):
        """Количество слов	"""
        word_list = re.findall(r'[^\W\d_]+', self.text)
        count_worlds = len(word_list)
        return count_worlds

    def count_unique_worlds(self):
        """Количество уникальных слов"""
        morph = pymorphy2.MorphAnalyzer(lang=self.lang)
        word_list = re.findall(r'[^\W\d_]+', self.text.lower())
        count_worlds = len(set(word_list))

        unique_words = set()
        words = set(word_list)
        for word in words:
            parsed_word = morph.parse(word)[0]
            lemma = parsed_word.normal_form
            unique_words.add(lemma)

        return len(unique_words)

    def get_lemma(self, word):
        morph = pymorphy2.MorphAnalyzer()
        parsed_word = morph.parse(word)[0]
        return parsed_word.normal_form

    def dict_significant_words(self):
        stop_words = set(stopwords.words(self.full_lang))
        words = word_tokenize(self.text.lower())
        words = [self.get_lemma(word) for word in words if word.isalpha() and word not in stop_words]
        word_counts = Counter(words)
        significant_words_counts = {word: count for word, count in word_counts.items() if count >= 2}
        return dict(sorted(significant_words_counts.items(), key=lambda item: item[1], reverse=True))

    def count_significant_words(self):
        return sum(self.dict_significant_words().values())

    def count_stop_words(self):
        """Количество стоп-слов"""
        words = word_tokenize(self.text.lower())
        stop_words = set(stopwords.words(self.full_lang))
        stop_word_count = sum(word in stop_words for word in words)
        return stop_word_count

    def percent_stop_words(self):
        """Процент стоп слов"""
        return round(self.count_stop_words() / self.count_worlds() * 100, 2)

    def water(self):
        count_words = self.count_worlds()
        water = (count_words - self.count_significant_words()) / count_words
        return int(water * 10000) / 100

    # def count_grammar_errors(self):
    #     tool = language_tool_python.LanguageTool(
    #         'ru')  # Language code for English (replace with appropriate language code)
    #     matches = tool.check(self.text)
    #     return len(matches)

    def dict_stop_words(self):
        """Стоп-слова"""
        words = word_tokenize(self.text.lower())
        stop_words = set(stopwords.words(self.full_lang))
        stop_words_list = [word for word in words if word in stop_words]

        stop_words_list = Counter(stop_words_list)
        stop_words_list = sorted(dict(stop_words_list).items(), key=lambda x: x[1], reverse=True)
        #
        return dict(stop_words_list)

    def generate_semantic_core(self):
        """Семантическое ядро"""
        word_list = re.findall(r'[^\W\d_]+', self.text.lower())
        nlp = spacy.load("en_core_web_sm")
        stopwords = self.dict_stop_words().keys()
        doc = nlp(' '.join(word_list))
        filtered_words = [token.text.lower() for token in doc if
                          not token.is_stop and token.text not in stopwords]
        word_freq = Counter(filtered_words)
        keywords = word_freq.most_common(10)

        bigram_measures = BigramAssocMeasures()
        finder = BigramCollocationFinder.from_words(filtered_words)

        n_best_phrases = finder.nbest(bigram_measures.raw_freq, 10)

        # Adding phrases to the semantic core
        for phrase in n_best_phrases:
            keywords.append((" ".join(phrase), word_freq[phrase[0]] + word_freq[phrase[1]]))
        keywords = sorted(dict(keywords).items(), key=lambda x: x[1], reverse=True)
        return dict(keywords)

    def classic_nausea(self):
        return round(max(self.dict_significant_words().values()) ** 0.5, 2)

    def academic_nausea(self):
        return round(self.count_significant_words() / self.count_worlds() * 0.39 * 100, 2)

    def average_words_per_sentence(self):
        sentences = nltk.sent_tokenize(self.text)
        valid_sentences = [sentence for sentence in sentences if len(nltk.word_tokenize(sentence)) > 1
                           and not sentence[:-1].isdigit()]
        words_per_sentence = [len(nltk.word_tokenize(sentence)) for sentence in valid_sentences]
        if len(words_per_sentence) == 0:
            return 0
        average_words = sum(words_per_sentence) / len(words_per_sentence)
        return round(average_words, 2)

    def count_paragraphs(self):
        paragraphs = re.split(r'\n\s*\n', self.text)
        # Remove leading and trailing whitespaces from each paragraph
        paragraphs = [paragraph.strip() for paragraph in paragraphs]
        # Remove empty paragraphs
        paragraphs = [paragraph for paragraph in paragraphs if paragraph]
        return len(paragraphs)


if __name__ == '__main__':
    import test_text

    text = test_text.text
    text = TextAnalyzer(text=str(text))
    # print('Язык: ', text.lang, text.full_lang)
    # print('Количество символов: ', text.get_count_characters())
    # print('Количество символов без пробелов: ', text.count_characters_without_spaces())
    # print('Количество слов: ', text.count_worlds())
    # print('Количество уникальных слов: ', text.count_unique_worlds())
    # print('Количество значимых слов: ', text.count_significant_words())
    # print('Количество стоп-слов: ', text.count_stop_words())
    # print('Процент стоп-слов: ', text.percent_stop_words())
    # print('Вода (%): ', text.water())
    # # print(text.count_grammar_errors())
    # print('Классическая тошнота документа: ', text.classic_nausea())
    # print('Академическая тошнота документа (%): ', text.academic_nausea())
    # print('Среднее количество слов в предложении: ', text.average_words_per_sentence())
    # print('Количество параграфов: ', text.count_paragraphs())
    # print('Семантическое ядро: ', text.generate_semantic_core())
    print('Значемые слова: ', text.dict_significant_words())
    print('Словарь стоп-слов: ', text.dict_stop_words())
