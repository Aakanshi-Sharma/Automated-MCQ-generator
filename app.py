# -------------Import library-----------
import pickle
import streamlit as st
import os


# ---------------IMPORT PICKLE FILES------------
file_path = os.path.abspath("get_summaries.pkl")
summarization = pickle.load(open(file_path, "rb"))
extraction = pickle.load((open("extraction.pkl", "rb")))
tokenize_sentence = pickle.load(open("tokenize_sentences.pkl", "rb"))
get_sentences_for_keywords = pickle.load(open("get_sentences_for_keyword.pkl", "rb"))
get_multiple_choice = pickle.load(open("get_multiple_choice.pkl", "rb"))


# ---------------FUNCTIONS---------------

def multiple_choice(text):
    summarized_text = summarization(text)
    keywords = extraction(summarized_text)[0][0]
    tokens = tokenize_sentence(summarized_text)
    keyword_sentence_dict = get_sentences_for_keywords(keywords, tokens)
    multiple_choice_lists = get_multiple_choice(keyword_sentence_dict)
    return multiple_choice_lists


# ---------------UI--------------------------
input_text = st.text_area("Input")

st.text(multiple_choice("The cat (Felis catus), commonly referred to as the domestic cat or house cat, is the only "
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
