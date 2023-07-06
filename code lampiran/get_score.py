# Evaluate SpanModel F1 Score
import json
import sys
sys.path.append("aste")
from data_utils import Data
from wrapper import SpanModel

data_name="multi_sentence_single_word"
random_seed=1
save_dir = f"outputs/{data_name}/seed_{random_seed}"

model = SpanModel(save_dir=save_dir, random_seed=random_seed)

path_pred = "pred.txt"
path_test = f"aste/data/triplet_data/{data_name}/test.txt"
model.predict(path_in=path_test, path_out=path_pred)
results = model.score(path_pred, path_test)
print(json.dumps(results, indent=2))

# Restore the standard output
sys.stdout = sys.__stdout__
