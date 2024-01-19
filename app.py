# -------------Import library-----------
import pickle

# ---------------IMPORT PICKLE FILES------------

summarization = pickle.load(open("summarization.pkl", "rb"))
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
