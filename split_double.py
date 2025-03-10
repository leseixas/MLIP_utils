from ase.io import read, write
import numpy as np

# Load all configurations from the XYZ file
filename = "all_dataset.xyz"
atoms_list = read(filename, index=":")

# Define split ratio
train_ratio = 0.8  # 80% train, 20% test
#total_configs = len(atoms_list)
total_configs = 1000

# Shuffle indices
indices = np.arange(total_configs)
np.random.seed(42)  # For reproducibility
np.random.shuffle(indices)

# Define train/test split
split_idx = int(train_ratio * total_configs)
train_indices = indices[:split_idx]
test_indices = indices[split_idx:]

# Split configurations
train_configs = [atoms_list[i] for i in train_indices]
test_configs = [atoms_list[i] for i in test_indices]

# Save train and test sets
write("train.xyz", train_configs)
write("test.xyz", test_configs)

print(f"Total configurations: {total_configs}")
print(f"Training set: {len(train_configs)} configurations")
print(f"Test set: {len(test_configs)} configurations")
print("Files saved: train.xyz, test.xyz")

