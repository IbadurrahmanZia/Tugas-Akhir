##train
#@title Data Exploration
data_name = "balanced_multi_multi" #@param ["14lap", "14res", "15res", "16res"]

import sys
sys.path.append("aste")
from data_utils import Data

path = f"aste/data/triplet_data/{data_name}/train.txt"
data = Data.load_from_full_path(path)

for s in data.sentences[:3]:
    print("tokens:", s.tokens)
    for t in s.triples:
        print("target:", (t.t_start, t.t_end))
        print("opinion:", (t.o_start, t.o_end))
        print("label:", t.label)
    print()

from wrapper import SpanModel
# Train SpanModel from scratch
random_seed = 1
path_train = f"aste/data/triplet_data/{data_name}/train.txt"
path_dev = f"aste/data/triplet_data/{data_name}/dev.txt"
save_dir = f"outputs/{data_name}/seed_{random_seed}"

model = SpanModel(save_dir=save_dir, random_seed=random_seed)
model.fit(path_train, path_dev)

####
#score
@classmethod
    def score(cls, path_pred: str, path_gold: str) -> dict:
        pred = Data.load_from_full_path(path_pred)
        gold = Data.load_from_full_path(path_gold)
        assert pred.sentences is not None
        assert gold.sentences is not None
        assert len(pred.sentences) == len(gold.sentences)
        num_pred = 0
        num_gold = 0
        num_correct = 0
        not_predicted = 0
        mispredicted = 0

        for i in range(len(gold.sentences)):
            num_gold += len(gold.sentences[i].triples)

            for p in pred.sentences[i].triples:
                num_pred += 1

                found_match = False
                for g in gold.sentences[i].triples:
                    if p.dict() == g.dict():
                        num_correct += 1
                        found_match = True
                        break

                if not found_match:
                    mispredicted += 1

        not_predicted = num_gold - num_correct

        for i in range(len(gold.sentences)):
            words = pred.sentences[i].tokens
            sentence = " ".join(words)
            predictions = []
            golds = []

            for p in pred.sentences[i].triples:
                dict_pred = p.dict()
                opinion_pred = " ".join(words[dict_pred['o_start']:dict_pred['o_end']+1])
                target_pred = " ".join(words[dict_pred['t_start']:dict_pred['t_end']+1])
                pred_sen = dict_pred['label'].value
                predictions.append([opinion_pred, target_pred, pred_sen])

            for g in gold.sentences[i].triples:
                dict_gold = g.dict()
                opinion_gold = " ".join(words[dict_gold['o_start']:dict_gold['o_end']+1])
                target_gold = " ".join(words[dict_gold['t_start']:dict_gold['t_end']+1])
                gold_sen = dict_gold['label'].value
                golds.append([opinion_gold, target_gold, gold_sen])

            predictions_set = set(tuple(prediction) for prediction in predictions)
            golds_set = set(tuple(gold) for gold in golds)

            only_in_predictions = predictions_set - golds_set
            only_in_golds = golds_set - predictions_set
            # Open a file for writing
            
            output_file = open(f'{path_gold.split("/")[3]}_pred_report.txt', 'a')

            # Redirect the standard output to the file
            sys.stdout = output_file
            print("########################################################")
            print()
            print("Sentence")
            print("--------")
            print(sentence)

            print()
            print("Prediction")
            print("--------")
            for item in predictions:
                print(", ".join(item))

            print()
            print("Actual")
            print("--------")
            for item in golds:
                print(", ".join(item))

            if only_in_predictions:
                print()
                print("Only in Prediction (mispredict)")
                print("--------")
                for item in only_in_predictions:
                    print(", ".join(item))

            if only_in_golds:
                print()
                print("Only in Gold (not predicted)")
                print("--------")
                for item in only_in_golds:
                    print(", ".join(item))

            print()

        print(f"total predictions: {num_pred}")
        print(f"total gold: {num_gold}")
        print(f"correctly predicted: {num_correct}")
        print(f"mispredicted: {mispredicted}")
        print(f"not predicted: {not_predicted}")
        precision = safe_divide(num_correct, num_pred)
        recall = safe_divide(num_correct, num_gold)


        info = dict(
            path_pred=path_pred,
            path_gold=path_gold,
            precision=precision,
            recall=recall,
            score=safe_divide(2 * precision * recall, precision + recall),
        )
        print(json.dumps(info, indent=2))
        sys.stdout = sys.__stdout__
        output_file.close()
        return info