# file_path = "split_sentence.txt"  # Replace with the path to your text file
file_path = "final_dataset.txt"  # Replace with the path to your text file

import ast
limit_words_aspect = 5
limit_words_opinion = 7
limit_tokens_aspect = 100
limit_tokens_opinion = 100
pos_to_keep = 2000

with open(file_path) as topo_file:
    counter = 0
    final_res = []
    for index, line in enumerate(topo_file):
        outlier = False
        txt_data = line.split("#### #### ####")
        tagging = txt_data[1]
        res = ast.literal_eval(tagging)
        final_tagged = []
        sentence = txt_data[0]
        sentence_split = sentence.split(" ")
        # print(txt_data)
        for i, x in enumerate(res):
            opinion_length = len(x[1])
            aspect_length = len(x[0])
            aspect_index = x[0]
            opinion_index = x[1]

            aspect = sentence_split[(aspect_index[0]):(aspect_index[-1]) + 1]

            target_len = 0
            for targets in aspect:
                if(len(targets)>target_len):
                    target_len = len(targets)

            opinion = sentence_split[(opinion_index[0]):(opinion_index[-1]) + 1]
            opinion_len = 0
            for opin in opinion:
                if(len(opin)>opinion_len):
                    opinion_len = len(opin)

            if (opinion_length > limit_words_opinion or aspect_length > limit_words_aspect or target_len > limit_tokens_aspect or opinion_len >limit_tokens_opinion):
                print(f"outlier detected: {line}")
                outlier=True
                counter += 1

            else:
                final_tagged.append(x)

        if len(final_tagged) != 0:
            c = f"{txt_data[0]}#### #### ####{final_tagged}"
            if outlier:
                print(c)
            final_res.append(c)
    # print(f"Opinions with more than {limit_words} words: {counter}")

# with open('test filter.txt', 'w') as f:
#     for c in final_res:
#         f.write(c)
#         f.write('\n')
comments_to_keep =[]
total_pos=0
total_neg=0
total_neu=0
for line in final_res:
    sentences = line.strip()
    counter_pos=0
    counter_neg=0
    counter_neu=0
    splitted = sentences.split("#### #### ####")
    tagged_info = splitted[1]
    tagged_data_list = eval(tagged_info)
    for z in tagged_data_list:
        sen = z[2]
        if sen =="POS":
            counter_pos+=1    
        if sen =="NEU":
            counter_neu+=1
        if sen =="NEG":
            counter_neg+=1 
    

    if counter_neg+counter_neu ==0 and pos_to_keep ==0 :
        continue
    
    if counter_neg+counter_neu ==0:
        pos_to_keep-=1
    comments_to_keep.append(sentences)
    total_pos+=counter_pos
    total_neg+=counter_neg
    total_neu+=counter_neu

print(total_pos,total_neg,total_neu) 
print(f"total lines: {len(comments_to_keep)}")  

# with open('multi_sentence_multi_word_balanced.txt', 'w') as f:
#     for c in final_res:
#         f.write(c)
#         f.write('\n')

