#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Split an extxyz file into train, validation, and test sets for ML.
"""

import argparse
import random
from ase.io import read, write

def main():
    parser = argparse.ArgumentParser(
        description="Split ASE traj dataset (xyz, traj or hdf5) into train, validation, and test sets for ML."
    )
    parser.add_argument("input", type=str, help="Input file")
    parser.add_argument(
        "--ratios", type=float, nargs=3, default=[0.8, 0.1, 0.1],
        help="Three numbers (train, validation, test) that sum to 1.0. Default is 0.8 0.1 0.1"
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for shuffling (default: 42)"
    )

    parser.add_argument(
        "--total", type=int, default=0,
        help="Total number of configurations to split into train, validation, and test sets. Default is 0 (all)."
    )

    args = parser.parse_args()

    # Ensure the ratios sum to 1
    if abs(sum(args.ratios) - 1.0) > 1e-4:
        raise ValueError("The provided ratios must sum to 1.0.")

    # Read all atoms from the extxyz file
    atoms_list = read(args.input, index=":")
    
    # Extract forces and store them in atoms.info
    for atoms in atoms_list:
        if atoms.calc is not None:
            forces = atoms.get_forces()
            atoms.set_array("REF_forces", forces)
            energy = atoms.get_total_energy()
            atoms.info["REF_energy"] = energy
        atoms.calc = None
    
    # Shuffle the dataset to randomize the split
    random.seed(args.seed)
    random.shuffle(atoms_list)
    
    if args.total > 0:
        total = args.total
    else:
        total = len(atoms_list)

    train_count = int(total * args.ratios[0])
    valid_count = int(total * args.ratios[1])
    # Assign the rest to the test set
    # test_count = total - train_count - valid_count

    # Split the atoms list
    train_atoms = atoms_list[:train_count]
    validation_atoms = atoms_list[train_count:train_count + valid_count]
    test_atoms = atoms_list[train_count + valid_count : total]

    # Write to respective files
    write("train.xyz", train_atoms)
    write("validation.xyz", validation_atoms)
    write("test.xyz", test_atoms)

    print(f"Total frames: {total}")
    print(f"Train: {len(train_atoms)} | Validation: {len(validation_atoms)} | Test: {len(test_atoms)}")

if __name__ == "__main__":
    main()

