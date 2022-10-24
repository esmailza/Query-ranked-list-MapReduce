#!/usr/bin/python3
import sys
import json
import math 

unique_stem_dic = {}
NUMBER_OF_DOCUMENTS = 1400
doc_term_freq = {} 

def get_normalize_value(doc_id):
    squares = 0.0
    for key, value in doc_term_freq[doc_id].items():
        tf = float(1+math.log(value))
        squares += round( math.pow(tf ,2) , 4)
    cosine_normalize_value = round(math.sqrt(squares), 4)
    return cosine_normalize_value

for line in sys.stdin:

    stem_word, doc_id, stem_count = line.split()
    
    if stem_word not in unique_stem_dic:
        unique_stem_dic[stem_word] = {}
        unique_stem_dic[stem_word]["stat"] = {}
        unique_stem_dic[stem_word]["documents"] = {}
        unique_stem_dic[stem_word]["documents"][doc_id] = {"frequency": 1}
    else:
        if doc_id not in unique_stem_dic[stem_word]["documents"]:
            unique_stem_dic[stem_word]["documents"][doc_id] = {"frequency": 1}
        else:
            unique_stem_dic[stem_word]["documents"][doc_id]["frequency"] = unique_stem_dic[stem_word]["documents"][doc_id]["frequency"] + 1
    
    if doc_id not in doc_term_freq:
        doc_term_freq[doc_id] = {}
        doc_term_freq[doc_id][stem_word] = 1
    else:
        if stem_word not in doc_term_freq[doc_id]:
            doc_term_freq[doc_id][stem_word] = 1
        else:
            doc_term_freq[doc_id][stem_word] = doc_term_freq[doc_id][stem_word] + 1

for key, value in unique_stem_dic.items():
    term_df = len(value["documents"])
    term_idf = round(math.log(float(NUMBER_OF_DOCUMENTS/int(term_df))), 4)   # idf = Log(N/df)
    unique_stem_dic[key]["stat"] = {"df":term_df, "idf":term_idf}

    for doc_id in value["documents"]:
        doc_normalize_val = get_normalize_value(doc_id)
        term_freq_weight = round(float(1 + math.log(value["documents"][doc_id]["frequency"])), 4)    # tf-wght = 1+Log(term_freq_in_doc)
        unique_stem_dic[key]["documents"][doc_id]["term_freq_normalized_weight"] = round(float(term_freq_weight/doc_normalize_val),5) 
        

print(unique_stem_dic)

