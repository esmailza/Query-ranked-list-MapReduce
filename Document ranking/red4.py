#!/usr/bin/python3
import sys
import json
import math
import fileinput
import ast


output ={}

# for line in fileinput.input():
for lin in sys.stdin:
    line = line.rstrip() 
    diction  = ast.literal_eval(line)
    for q_id in diction.keys():
        
        temp = 0
        output[q_id] = 0
        for doc_id in diction[q_id]:
            temp = 0
            for key in diction[q_id][doc_id]:
                 temp = round((diction[q_id][doc_id][key]["term_weighted_tf"] * diction[q_id][doc_id][key]["term_normalized_weighted_tf"]),4)+temp
                 
            
        
            print(q_id, doc_id, temp)



                
               
   


    