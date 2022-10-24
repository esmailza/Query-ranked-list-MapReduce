#!/usr/bin/python3

from io import StringIO
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import csv
import math
import sys
import re
import ast
import fileinput

stemmer = PorterStemmer()
stop_words = stopwords.words('english')
word_dic = {}
doc_Wfreq = {}
Query_tf_mult_idf ={}
output ={}
QueryNum = 225



file = open('ADD File','r').read()
data = ast.literal_eval(file)



#function that gets the query and count the frequiencies
def counter(word,docNum):
    
    if word not in word_dic:
        word_dic[word] = {}
        word_dic[word]["stat"] = {}
        word_dic[word]["documents"] = {}
        word_dic[word]["documents"][docNum] = {"frequency": 1}
    else:
        if docNum not in word_dic[word]["documents"]:
            word_dic[word]["documents"][docNum] = {"frequency": 1}
        else:
            word_dic[word]["documents"][docNum]["frequency"] = word_dic[word]["documents"][docNum]["frequency"] + 1

    if docNum not in doc_Wfreq:
        doc_Wfreq[docNum] = {}
        Query_tf_mult_idf[docNum] ={}
        Query_tf_mult_idf[docNum][word] ={}
        doc_Wfreq[docNum][word] = 1
        
        
    else:
        if word not in doc_Wfreq[docNum]:
            doc_Wfreq[docNum][word] = 1
        else:
            doc_Wfreq[docNum][word] = doc_Wfreq[docNum][word]+ 1

    return (word_dic , doc_Wfreq )


#################################################################################
#cleaning and counting
# for line in fileinput.input():
for line in sys.stdin:
    for row in csv.reader(StringIO(line)):
        if(row[0] != "\n"):
        	for term in re.findall(r'[A-Za-z]+|\d+', row[1].lower().casefold()):
            	 if (term is not "" and term.isnumeric() == False and term not in stop_words):
                    word = stemmer.stem(term)
                    counter(word, row[0])
                    

#calculating idf for each word
for key, value in word_dic.items():
    term_df = len(value["documents"])
    term_idf = round(math.log(float(QueryNum/int(term_df))), 4)   # idf = Log(N/df)
    word_dic[key]["stat"] = {"idf":term_idf}
  


#calculating tf vector
for key, value in doc_Wfreq.items():
    for key1, value1 in value.items():
        Query_tf_mult_idf[key][key1] = 1+ math.log(value1) 
       
       
       #multiplying idf to the tf vector
        for key_dic, value_dic in word_dic.items():
             if( key_dic == key1 ):
                 Query_tf_mult_idf[key][key1] = Query_tf_mult_idf[key][key1] * word_dic[key_dic]["stat"]["idf"]

      ############################################################  

#generating the final outout in the (query_id, doc_id{terms}) format
for q_id, q_value in Query_tf_mult_idf.items():
    output ={}  
        #data[key]["documents"].keys()
    for word, TFID_Value in q_value.items():    
        for doc_word in data.keys():                       
            if(doc_word == word):
                for doc in data[doc_word]["documents"].keys():
                    if doc not in output :                       
                        output[doc]={}                   
                    output[doc][word] = {"term_weighted_tf":TFID_Value, "term_normalized_weighted_tf": data[doc_word]["documents"][doc]["term_freq_normalized_weight"] }

    for key,value in output.items():
        print({q_id: {key: value}})

    


       
        



