#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Convert an ASE file to HDF5 format.
"""

from ase.io import read, Trajectory
from argparse import ArgumentParser

def main():
    parser = ArgumentParser(
        description="Convert an ASE file to HDF5 format."
    )

    parser.add_argument("input", type=str, help="Input file")
    parser.add_argument("--output", type=str, help="Output file", default="output.h5")

    args = parser.parse_args()

    input_file = args.input
    output_file = args.output

    # Read all frames from your extxyz file
    atoms_list = read(input_file, index=":")

    # Create a trajectory in HDF5 format (requires h5py)
    with Trajectory(output_file, "w") as traj:
        for atoms in atoms_list:
            traj.write(atoms)

    print(f"Converted {input_file} to {output_file}")
    print(f"Number of configurations: {len(atoms_list)}")

if __name__ == "__main__":
    main()
