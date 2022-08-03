
"""
Create a dir to run this script from. Place this script in it along with
as subdir with all the structures for all-vs-all comparison. 

Follow the prompts, script will output an alignment file []_all-v-all.csv

This script is unsupported.

Created by Matt Mortimer https://orcid.org/0000-0002-8135-9319 
matthew.mortimer@anu.edu.au
2022-08-03
"""

import os

# Create a foldseek database
# Takes a dir with pdb structures and converts to a database
print("Make sure all structures are in a subfolder in this directory")

struct_dir = input("What is the name of the directory with the structures: ")
db_name = input("Enter the name for the database: ")
max_seq = input("Maximum number of sequences to align against each other: ")
db_parent = f"{struct_dir}_{db_name}"
db_loc = f"{db_parent}/{db_name}"

if os.path.exists(db_parent) is False:
    os.mkdir(db_parent)
    os.mkdir(f"{db_loc}")
else:
    pass

os.system(f"foldseek createdb {struct_dir} {db_loc}/{db_name}")

# Run search for each sequence in struct_dir against db_name
for root, dirs, files in os.walk(f"{struct_dir}", topdown=True):
    for struct in files:
        name = struct.rstrip(".pdb")
        os.system(f"foldseek easy-search {struct_dir}/{struct} {db_loc}/{db_name} {db_parent}/{name}_aln {db_parent}/tmpFolder --max-seqs {max_seq}")

# List all alignment files outputted from the search
files = [os.path.join(db_parent,f) for f in os.listdir(db_parent) if os.path.isfile(os.path.join(db_parent,f))]

# Create a new csv file with column headings and append all the alignment files
with open(f"{struct_dir}_all-v-all.csv", "a") as all_file:
    all_file.write("query\ttarget\tfident\talnlen\tmsmatch\tgapopen\tqstart\tqend\ttstart\ttend\tevalue\tbits\n")
    for f in files:
        with open(f, "r") as ofile:
            for line in ofile:
                all_file.write(line)