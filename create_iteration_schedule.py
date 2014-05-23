'''This script is meant to prepare a directory of text files for parallel processing on an SGE network.
More specifically, this script reads in a directory of files and finds all unique file pairings between those files,
such that each file is paired with each other file in the directory exactly once.

Say your directory contains three files: f1, f2, f3. In that case, the matched pairs look like this:

iteration   A   B
0   f1  f2
1   f1  f3
2   f1  f4
3   f2  f3
4   f2  f4
5   f3  f4

Our first column keeps track of the iteration number--ie, the first pairing will be dubbed iteration 0 (0-based indexing),
the second pairing iteration 2, and so forth. The second column contains the file we are comparing against the file in the third column.

Given the resulting data structure, we can use the iteration numbers and text pairings to run parallel analysis on an SGE.'''

from os.path import basename
from itertools import combinations
import glob

directory_with_files_to_be_paired = "C:\\Text\\Professional\\Text Data\\EEBO\\eebo_plaintext\\*.txt"

list_of_filenames = []

for i in glob.glob(directory_with_files_to_be_paired):
    file_name = basename(i)
    list_of_filenames.append(file_name)

#We now have a list object that contains the names of all files in the directory we specified above.
#Let's find all unique pairings between those files, and, for each of those pairings, let's assign an iteration number
iteration_number = 0

with open("parallel_processing_iteratoin_schedule.txt","w") as out:
    
    for j in combinations(list_of_filenames,2):
        out.write( str(iteration_number) + "\t" + str(j[0]) + "\t" + str(j[1]) + "\n")
        iteration_number += 1