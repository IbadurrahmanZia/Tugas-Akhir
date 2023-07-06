import json

def getIndex(aspect,indexStart, txt):

    index=[]
    counter = 0
    for x in txt[indexStart::-1]:
        if(x == " "):
            counter+=1
    index.append(counter)
    if(" " in aspect):
        for x in range (0,(aspect.count(" "))):
            index.append(counter+x+1)
    return index

f = open('kesa.json')

data = json.load(f)

metadata = []
for i in data:
    relationList = []
    sentence = i['data']['review']
    for x in (i['annotations'][0]['result']):
        if "from_id" in x:
            id_aspect = x["from_id"]
            idOpinion = x["to_id"]
            sent = x['labels'][0]
            relationList.append([id_aspect,idOpinion,sent])
    # metadata.append([sentence,relationList])

# for k in metadata:
#     wordlist=[]
#     for l in k[1]:
#         words=[]
#         for m in l:
#             for i in data:
#                 for x in (i['annotations'][0]['result']):
#                     if "value" in x:
#                         if x["id"] == m:
#                             word = x["value"]["text"]
#                             word_start = x["value"]["start"]
#                             index = getIndex(word,word_start,k[0])
#                             words.append(index)
#         words.append(l[2].split(":")[1])
#         words = tuple(words)
#         wordlist.append(words)
#     # res = [k[0],wordlist]
#     res = wordlist
#     print(f"{k[0]}#### #### ####{res}" )