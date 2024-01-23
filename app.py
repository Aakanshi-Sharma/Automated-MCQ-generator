# -------------Import library-----------
import pickle
import string
from heapq import nlargest
import nltk
from flashtext import KeywordProcessor
from nltk.tokenize import sent_tokenize
import streamlit as st

# ---------------IMPORT PICKLE FILES------------
stopwords = pickle.load(open("stopwords.pkl", "rb"))
normalized_frequencies = pickle.load(open("normalized_frequencies.pkl", "rb"))
vectorized = pickle.load(open("vectorized.pkl", "rb"))
s2v = pickle.load(open("s2v.pkl", "rb"))

# ------------------INITIALIZATION----------------
punctuations = string.punctuation


# # ---------------FUNCTIONS---------------
def get_summaries(text):
    sentences = text.strip().split(".")
    normalized_dict = {}
    for sentence in sentences:
        if len(sentence) > 0:
            temp_words_list = []
            words = sentence.strip().split(" ")
            for word in words:
                if word not in stopwords and word not in punctuations:
                    b = "".join([i for i in word if i not in punctuations])
                    if len(b) > 0:
                        temp_words_list.append(b)
            if len(temp_words_list) > 0:
                normalized_length = 0
                for i in temp_words_list:
                    if i in normalized_frequencies:
                        normalized_length += normalized_frequencies[i]
                    else:
                        normalized_length += 0
            normalized_dict[sentence] = normalized_length
    dict_length = int(len(normalized_dict) * 0.3)
    res = nlargest(dict_length, normalized_dict, key=normalized_dict.get)

    return ". ".join(res)


def extraction(text, vectorized_model):
    corpus = [text]
    tfidf_matrix = vectorized_model.fit_transform(corpus)
    features_names = vectorized_model.get_feature_names_out()
    if len(features_names) > 20:
        n = int(len(features_names) * 0.4)
        top_keywords = [features_names[i] for i in tfidf_matrix.sum(axis=0).argsort()[0, ::-1][:n]]
    else:
        top_keywords = [features_names[i] for i in tfidf_matrix.sum(axis=0).argsort()[0, ::-1][:len(features_names)]]
    return top_keywords


def sense2vec_get_words(word, sense_to_vec):
    output = []
    word = word.lower()
    word = word.replace(" ", "_")
    sense = sense_to_vec.get_best_sense(word)
    most_similar = sense_to_vec.most_similar(sense, n=20)
    for each_word in most_similar:
        append_word = each_word[0].split("|")[0].replace("_", " ").lower()
        if append_word.lower() != word:
            output.append(append_word.title())
    out2 = []
    for i in output:
        if i not in out2:
            out2.append(i)
    return out2


def tokenize_sentences(text):
    sentences = [sent_tokenize(text)]
    sentences = [y for x in sentences for y in x]
    sentences = [x.strip() for x in sentences if len(x) > 20]
    return sentences


def get_sentences_for_keyword(keywords, sentences):
    processor = KeywordProcessor()
    keywords_sentence_dict = {}
    for word in keywords:
        keywords_sentence_dict[word] = []
        processor.add_keyword(word)
    for sentence in sentences:
        keyword_found = set(processor.extract_keywords(sentence))
        for key in keyword_found:
            keywords_sentence_dict[key].append(sentence)
    for key in keywords_sentence_dict:
        values = keywords_sentence_dict[key]
        values = sorted(values, key=len, reverse=True)
        keywords_sentence_dict[key] = values
    return keywords_sentence_dict


# ----------------UI--------------------------
# input_text = st.text_area("Input")

# ------------------MAIN FUNCTION---------------------
def multiple_choice(text):
    summarized_text = get_summaries(text)
    top_keywords = extraction(summarized_text, vectorized)
    tokens = tokenize_sentences(summarized_text)
    keyword_sentence_dict = get_sentences_for_keyword(top_keywords[0][0], tokens)
    return keyword_sentence_dict


print(multiple_choice("The cat (Felis catus), commonly referred to as the domestic cat or house cat, is the only "
                      "domesticated species in the family Felidae. Recent advances in archaeology and genetics have "
                      "shown that the domestication of the cat occurred in the Near East around 7500 BC. It is "
                      "commonly kept as a house pet and farm cat, but also ranges freely as a feral cat avoiding "
                      "human contact. It is valued by humans for companionship and its ability to kill vermin. "
                      "Because of its retractable claws it is adapted to killing small prey like mice and rats. It "
                      "has a strong flexible body, quick reflexes, sharp teeth, and its night vision and sense of "
                      "smell are well developed. It is a social species, but a solitary hunter and a crepuscular "
                      "predator. Cat communication includes vocalizations like meowing, purring, trilling, hissing, "
                      "growling, and grunting as well as cat body language. It can hear sounds too faint or too "
                      "high in frequency for human ears, such as those made by small mammals. It also secretes and "
                      "perceives pheromones."))
