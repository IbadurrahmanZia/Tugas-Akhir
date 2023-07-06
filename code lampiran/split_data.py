import random

# Set the file paths
input_file = "multi_sentence_multi_word_balanced.txt"
train_file = "train.txt"
dev_file = "dev.txt"
test_file = "test.txt"

# Set the percentages
train_percent = 0.7
dev_percent = 0.15
test_percent = 0.15

# Read the input file
with open(input_file, "r") as f:
    lines = f.readlines()

# Shuffle the lines
random.shuffle(lines)

# Calculate the number of lines for each set
total_lines = len(lines)
train_lines = int(total_lines * train_percent)
dev_lines = int(total_lines * dev_percent)
test_lines = total_lines - train_lines - dev_lines

# Write the lines to the output files
with open(train_file, "w") as f:
    f.writelines(lines[:train_lines])

with open(dev_file, "w") as f:
    f.writelines(lines[train_lines:train_lines+dev_lines])

with open(test_file, "w") as f:
    f.writelines(lines[train_lines+dev_lines:])
