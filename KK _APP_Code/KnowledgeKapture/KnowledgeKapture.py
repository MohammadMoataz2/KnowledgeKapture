import PPF
import tkinter as tk
from tkinter import filedialog
import os
import json

from PIL import Image as PILImage
import PIL


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
def retrieve_documents(query,folder_path):

    stem_query = PPF.Stemming_sentences(query)

    new_inverted_index = json.load(open("inverted_index.json"))
    doc_dict_beta = json.load(open('doc_dict_beta.json'))

    set_of_doc_query = PPF.queries_in_any_doc(stem_query,new_inverted_index)




    doc_dict,set_of_words,list_of_words,stemming_dict = PPF.doc_word_create(set_of_doc_query,doc_dict_beta)


    docfreq_idf_df = PPF.df_idf(set_of_words,doc_dict,list_of_words)


    df_for_weight_freq_df,df_for_freq_df = PPF.Weights_Tf_df(doc_dict,docfreq_idf_df,stemming_dict,stem_query)

    sorted_df2  = PPF.Result_df(df_for_weight_freq_df.copy(),df_for_freq_df.copy(),doc_dict.copy())



    return list(sorted_df2.index)








def search():
    query = query_var.get()
    folder_path = folder_var.get()

    if query and folder_path:
        relevant_documents = retrieve_documents(query, folder_path)
        result_listbox.delete(0, tk.END)

        if relevant_documents:
            for doc in relevant_documents:
                result_listbox.insert(tk.END, doc)
        else:
            result_listbox.insert(tk.END, "Thrers is NO Relevant Documents Found.")
    else:
        result_listbox.delete(0, tk.END)
        result_listbox.insert(tk.END, "Enter a query and select a A Valid Folder.")



def open_document(event):
    selected_document = result_listbox.get(result_listbox.curselection())
    if selected_document:
        document_path = os.path.join(folder_var.get(), selected_document)
        try:
            os.startfile(document_path)
        except Exception as e:
            print("Error Opening Documents:", e)






def choose_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_var.set(folder_path)
        inverted_index_dict_wrod,doc_dict_beta = PPF.crawling(folder_var.get())

        PPF.create_json_file('inverted_index.json',inverted_index_dict_wrod)
        PPF.create_json_file('doc_dict_beta.json',doc_dict_beta)




from tkinter import *


def btn_clicked():
    print("Button Clicked")


window = Tk()
window.title("KnowledgeKapture")
window.geometry("1322x853")
window.configure(bg = "#ededed")
canvas = Canvas(
    window,
    bg = "#ededed",
    height = 853,
    width = 1322,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)







########SearchButton####################
img0 = PhotoImage(file = f"img0.png")
search_button = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = search,
    relief = "flat")

search_button.place(
    x = 463, y = 307,
    width = 111,
    height = 44)
########Search####################







########ChooseButton####################

folder_var = tk.StringVar()


img1 = PhotoImage(file = f"img1.png")
folder_button = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = choose_folder,
    relief = "flat")

folder_button.place(
    x = 463, y = 384,
    width = 111,
    height = 44)
########ChooseButton####################




########SearchEntry####################

query_var = tk.StringVar()


entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    260.0, 327.5,
    image = entry0_img)

query_entry = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0, textvariable=query_var
    ,font=("Helvetica", 25)
)

query_entry.place(
    x = 91.0, y = 307,
    width = 338.0,
    height = 39)


########SearchEntry####################





canvas.create_text(
    244.0, 405.5,
    text = "Select the files you want to use :",
    fill = "#000000",
    font = ("Poppins-Regular", int(18.0)))

canvas.create_text(
    180.0, 470.0,
    text = "Here are the results :",
    fill = "#000000",
    font = ("Poppins-Regular", int(18.0)))

img2 = PhotoImage(file = f"img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b2.place(
    x = 79, y = 27,
    width = 481,
    height = 268)

img3 = PhotoImage(file = f"img3.png")
b3 = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b3.place(
    x = 635, y = 39,
    width = 712,
    height = 406)




entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    686.0, 665.0,
    image = entry1_img)

result_listbox = Listbox(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0,font=("Helvetica", 25)
)

result_listbox.place(
    x = 60.0, y = 492,
    width = 1166.0,
    height = 344)




result_listbox.bind("<Double-Button-1>", open_document)



window.resizable(True, True)
window.mainloop()
