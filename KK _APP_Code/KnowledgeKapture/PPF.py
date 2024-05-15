
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import os
import json
import pandas as pd
import numpy as np

import os
import docx
from pdfquery import PDFQuery


def Pre_proccing_text(text):

    stop_words = set(stopwords.words('english') + ['us'])
    tokenizer = RegexpTokenizer(r'\w+')

    word_tokens = word_tokenize(text)

    filtered_sentence_stopword = [w.lower() for w in word_tokens if not w.lower() in stop_words]

    filtered_sentence_punc = tokenizer.tokenize(" ".join(filtered_sentence_stopword))

    return " ".join(filtered_sentence_punc)




def Stemming_sentences(text):

    ps = PorterStemmer()

    stemming_list = [ps.stem(w) for w in text.split()]

    return " ".join(stemming_list)


def test():
    return "h"

def Result_df(df_for_weight_df,df_for_freq_df,doc_dict):

    # FIRST METHOD , inner product ∑(𝒅𝒊𝒌.𝒒𝒌)

    # Calculate the inner product between query and documents weights
    query_weights = df_for_weight_df.loc['Q']
    doc_weights = df_for_weight_df.drop('Q')

    inner_product = doc_weights.dot(query_weights)


    # SECONDE METHOD , cosine

    query_tf = df_for_freq_df.loc['Q']
    doc_tf = df_for_freq_df.drop('Q')

    #Numerator :
    dot_products = doc_tf.dot(query_tf)

    #denominator :
    #length for doc and query
    len_query = np.sqrt(np.sum(np.square(query_tf)))

    len_docs = np.sqrt(np.sum(np.square(doc_tf), axis=1))

    cosine = dot_products / (len_docs * len_query)

    # THIRD METHOD , jaccard : i𝒏𝒏𝒆𝒓 𝒑𝒓𝒐𝒅𝒖𝒄𝒕/(∑𝒅𝟐ⅈ𝒌. + ∑𝒒𝟐𝒌−𝒊𝒏𝒏𝒆𝒓 𝒑𝒓𝒐𝒅𝒖𝒄𝒕)

    squared_weights_query= np.sum(np.square(query_weights))
    sum_squared_weights = np.square(doc_weights).sum(axis=1)
    Jaccard = inner_product / (squared_weights_query + sum_squared_weights - inner_product)



    #FORTH METHOD , dice
    #Numerator :
    dot_products = doc_tf.dot(query_tf)

    #denominator :
    sum_squared_query= np.sum(np.square(query_tf))
    sum_squared_doc = np.square(doc_tf).sum(axis=1)

    #final equation
    dice = 2*dot_products / (sum_squared_doc + sum_squared_query)



    methods_result = ['inner',"cosine","jaccard","dice"]


    df_result = pd.DataFrame(np.zeros((len(doc_dict),4)),index = doc_dict.keys() ,columns = methods_result)
    df_result["inner"]=inner_product
    df_result["cosine"]=cosine
    df_result["jaccard"]=Jaccard
    df_result["dice"]=dice


    x = list(df_result.columns)

    sorted_df2 = df_result.sort_values(by=x, ascending=False)

    return sorted_df2





def Weights_Tf_df(doc_dict,docfreq_idf_df,stemming_dict,stem_query):


    array_for_weight_freq_df = np.zeros((len(doc_dict)+1,len(docfreq_idf_df.index)))



    df_for_weight_freq_df = pd.DataFrame(array_for_weight_freq_df,
                                         columns = [f"T{i}" for i in docfreq_idf_df.index],index  = [i for i in doc_dict] + ['Q'])




    df_for_freq_df = df_for_weight_freq_df.copy()

    for i in df_for_weight_freq_df.index:


        if i == 'Q':
            continue

        for c in df_for_weight_freq_df.columns:

            term_freq_doc = stemming_dict[i].split(" ").count(docfreq_idf_df.loc[int(c[1:]),"terms"])

            df_for_freq_df.loc[i,c] = term_freq_doc


    for c in df_for_weight_freq_df.columns:

        term_freq_query = stem_query.split(" ").count(docfreq_idf_df.loc[int(c[1:]),"terms"])

        df_for_freq_df.loc["Q",c] = term_freq_query



    df_for_weight_df = df_for_weight_freq_df.copy()

    for i in df_for_weight_freq_df.index:


        if i == 'Q':
            continue

        for c in df_for_weight_freq_df.columns:

            term_freq_doc = stemming_dict[i].split(" ").count(docfreq_idf_df.loc[int(c[1:]),"terms"])

            idf = docfreq_idf_df.loc[int(c[1:]),"IDF"]

            df_for_weight_df.loc[i,c] = term_freq_doc * idf


    for c in df_for_weight_freq_df.columns:

        term_freq_query = stem_query.split(" ").count(docfreq_idf_df.loc[int(c[1:]),"terms"])

        idf = docfreq_idf_df.loc[int(c[1:]),"IDF"]

        df_for_weight_df.loc["Q",c] = term_freq_query * idf


    return df_for_weight_df,df_for_freq_df



def df_idf(set_of_words,doc_dict,list_of_words):

    docfreq_idf_dict = {

            "terms" : set_of_words,

            "DocFreq" : [i * 0 for i in range(len(set_of_words))],

            "IDF" : [i * 0 for i in range(len(set_of_words))]

        }

    docfreq_idf_df = pd.DataFrame(docfreq_idf_dict).sort_values(by = 'terms').reset_index(drop=True)



    for i in list(docfreq_idf_df.index):

        doc_freq_term = list_of_words.count(docfreq_idf_df.loc[i,"terms"])

        docfreq_idf_df.loc[i,"DocFreq"] = doc_freq_term
        docfreq_idf_df.loc[i,"IDF"]  = np.log10(len(doc_dict) / doc_freq_term)

    docfreq_idf_df.index =  docfreq_idf_df.index +1

    return docfreq_idf_df








def crawling(path):



    entries = os.listdir(fr'{path}')


    path_of_files = path

    entries = os.listdir(fr'{path_of_files}')
    doc_dict_alpha = {

    }

    for name in entries:

        if name[-3:] == 'txt':
            with open(fr'{path_of_files}\{name}', "r", encoding='utf8') as w:
                doc_dict_alpha[name] = w.readlines()

        elif name[-4:] == 'docx':

            doc = docx.Document(fr'{path_of_files}\{name}')

            new_list = []
            # Read the content
            for paragraph in doc.paragraphs:
                text = paragraph.text
                new_list.append(text)
            doc_dict_alpha[name] = new_list


        elif name[-3:] == 'pdf':

            pdf = PDFQuery(fr'{path_of_files}\{name}')
            pdf.load()

            # Use CSS-like selectors to locate the elements
            text_elements = pdf.pq('LTTextLineHorizontal')

            # Extract the text from the elements
            text = [t.text for t in text_elements]
            doc_dict_alpha[name] = text

    doc_dict_beta = {



    }
    for i in doc_dict_alpha:
        res = []
        for sub in doc_dict_alpha[i]:
            res.append(sub.replace("\n", ""))

        doc_dict_beta[i] = Stemming_sentences(Pre_proccing_text(" ".join(res).strip()))


    inverted_index_list_word = list()

    for i in doc_dict_beta:

        inverted_index_list_word.extend(doc_dict_beta[i].split())

    inverted_index_list_word = list(set(inverted_index_list_word))

    inverted_index_dict_wrod = {


    }


    for i in inverted_index_list_word:

        doc_word_list = []

        for c in doc_dict_beta:

            if i in doc_dict_beta[c]:
                doc_word_list.append(c)

        inverted_index_dict_wrod[i] = doc_word_list


    return inverted_index_dict_wrod,doc_dict_beta



def create_json_file(name,thing):
    with open(f'{name}', 'w') as fp:
        json.dump(thing, fp)






def queries_in_any_doc(query,new_inverted_index):


    stem_query = Stemming_sentences(query)


    set_of_doc_query = list()

    for i in new_inverted_index:
        if i in stem_query.split():
            set_of_doc_query.extend(new_inverted_index[i])

    set_of_doc_query = list(set(set_of_doc_query))

    return set_of_doc_query


def doc_word_create(set_of_doc_query,doc_dict_beta):
    doc_dict = {



        }

    for i in sorted(set_of_doc_query):

        doc_dict[i] = doc_dict_beta[i]

    stemming_dict = doc_dict.copy()

    set_of_words = set()
    list_of_words = []
    for i in stemming_dict.values():

        for c in set(i.split(" ")):
            set_of_words.add(c)
            list_of_words.append(c)
    set_of_words = list(set_of_words)

    return doc_dict,set_of_words,list_of_words,stemming_dict