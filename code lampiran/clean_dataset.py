file_path = "combined_tagging_data.txt"  # Replace with the path to your text file
final_res=[]

with open(file_path, 'r') as file:
    for line in file:
        # Process each line here
        tagged_data = line.strip()  # Print the line after removing leading/trailing whitespace
        splitted = tagged_data.split("#### #### ####")
        sentence = splitted[0]
        tagged_info = splitted[1]
        tagged_data_list = eval(tagged_info)


        split_sentence = sentence.split(".")
        word_counter = -1
        grouping =[]
        sentence_list=[]
        # print(split_sentence)
        for x in split_sentence:
            text = x.strip()+" ."
            sentence_list.append([text])
            # print(text)
            # print(text.split())
            num = len(text.split(" "))
            if num ==2:
                num=1
            # print(num)
            new_counter = word_counter+num
            # print(f"index_range: {word_counter+1} - {new_counter}")
            grouping.append([word_counter+1,new_counter])
            word_counter = new_counter
            
            # print(grouping)

        for x in tagged_data_list:
        # print(x)
            group_index =[0]
            for indexes in x[:-1]:
                for num in indexes:
                # print(num)
                    for index_sentence,groups in enumerate(grouping):
                        if groups[0] <= num <= groups[1]:
                        # print(f"this index is in group: {groups}")
                            if group_index == [0] or group_index == groups:
                                group_index = groups
                                include = True
                                idx = index_sentence
                            else:
                                include=False
                                # print("mismatched sentence")
            if include:
                final_index=[]
                for indexes in x[:-1]:
                    new_index=[]
                    for num in indexes:
                        new_index.append(num-group_index[0])
                    final_index.append(new_index)
                final_index.append(x[-1])
                sentence_list[idx].append(tuple(final_index))
        
        print(f"before {line}")

        for x in sentence_list:
            txt = x[0]
            tag=[]
            for tagged in x[1:]:
                tag.append(tagged)
            if tag == []:
                continue
            print(f"after {txt}#### #### ####{tag}")
            final_res.append(f"{txt}#### #### ####{tag}")

# with open('split_sentence.txt', 'w') as f:
#     for c in final_res:
#         f.write(c)
#         f.write('\n')