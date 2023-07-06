# Use pretrained SpanModel weights for prediction
import csv
import sys
import json
import os
sys.path.append("aste")
from pathlib import Path
from data_utils import Data, Sentence, SplitEnum
from wrapper import SpanModel


def predict_sentence(text: str, model: SpanModel) -> Sentence:
    path_in = f"/home/zia/Span-ASTE/run/{data_name}/seed_{seed}/temp_data/temp_in.txt"
    path_out = f"/home/zia/Span-ASTE/run/{data_name}/seed_{seed}/temp_data/temp_out.txt"
    sent = Sentence(tokens=text.split(), triples=[], pos=[], is_labeled=False, weight=1, id=0)
    data = Data(root=Path(), data_split=SplitEnum.test, sentences=[sent])
    data.save_to_path(path_in)
    model.predict(path_in, path_out)
    data = Data.load_from_full_path(path_out)
    return data.sentences[0]

def predict(id,text,model_dir,file_output):
    model = SpanModel(save_dir=model_dir, random_seed=0)
    sent = predict_sentence(text, model)

    # Read the JSON data from file
    with open(f'/home/zia/Span-ASTE/run/{data_name}/seed_{seed}/temp_data/pred_out.json', 'r') as file:
        json_data = file.read()

    data = json.loads(json_data)

    # Rest of the code remains the same...
    # Extract information from the JSON
    sentences = data['sentences']
    predicted_ner = data['predicted_ner'][0]
    predicted_relations = data['predicted_relations'][0]

    # Extract target and opinion from each predicted relation
    relations = []
    for relation in predicted_relations:
        opinion_start = relation[0]
        opinion_end = relation[1]
        target_start = relation[2]
        target_end = relation[3]

        # Extract target and opinion tokens
        target_tokens = sentences[0][target_start:target_end + 1]
        opinion_tokens = sentences[0][opinion_start:opinion_end + 1]

        # Join target and opinion tokens to form strings
        target = ' '.join(target_tokens)
        opinion = ' '.join(opinion_tokens)

        # Extract sentiment and confidence
        sentiment = relation[4]
        confidence = relation[6]

        # Create relation dictionary
        relation_dict = {
            'comment_id':id,
            'target': target,
            'opinion': opinion,
            'sentiment': sentiment,
            'confidence': confidence
        }
        relations.append(relation_dict)

    # Print the relations
    for relation in relations:
        print(relation)
    # Check if the CSV file exists
    file_exists = os.path.isfile(file_output)
    fieldnames = ['comment_id', 'target', 'opinion', 'sentiment', 'confidence']

    # Open the CSV file in append mode or create a new file
    with open(file_output, 'a', newline='') as file:
        # Create a CSV DictWriter object
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Create the header only if the file is newly created
        if not file_exists:
            writer.writeheader()

        # Append the data dictionaries to the CSV file
        writer.writerows(relations)
        print(f"adding {relations}")



def run(reviews_file,data_name,seed):
    # Download pretrained SpanModel weights
    model_dir = f"/home/zia/Span-ASTE/run/{data_name}/seed_{seed}"
    file_output = f'/home/zia/Span-ASTE/run/{data_name}/seed_{seed}/outputs/outputs.csv'

    file_path = file_output

    # Check if the file exists before deleting it
    if os.path.exists(file_path):
        os.remove(file_path)
        print("File deleted successfully.")
    else:
        print("File does not exist.")

    folder_path = f'/home/zia/Span-ASTE/run/{data_name}/seed_{seed}/outputs'

    # Check if the folder already exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print("Folder created successfully.")
    else:
        print("Folder already exists.")

    # Open the CSV file
    with open(reviews_file, 'r') as file:
        # Create a CSV reader object
        reader = csv.reader(file)

        # Loop through each row in the CSV file
        for row in reader:
            # Check if the row has at least two columns
            if len(row) >= 2:
                # Print the first and second column
                review = row[0]
                id = row[1]
                predict(id,review,model_dir,file_output)

# reviews_file = "split_reviews.csv"
reviews_file = "data_scrap_full.csv"

# data_name = "single_sentence_single_word"
data_name = "multi_sentence_single_word"
# data_name ="multi_sentence_multi_word"
# data_name ="single_sentence_multi_word"

seed = 1
run(reviews_file,data_name,seed)

run(reviews_file,data_name,seed)