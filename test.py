import sys, re

#
# Program mainline.
#
def __main__():
    num_runs = 0

    # Parse command line arguments.
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if i == 1:
            num_runs = int(arg)
        i += 1
        
    # In our first execution of the process outlined below, the iteration_number = 0; in the second pass, iteration_number = 1, and so on
    iteration_number = ""
    iteration_number += str(num_runs)
    
    ##########################################################################################################################################################
    # Using that iteration number, we can divide our routine into all of its constitive components, each of which can be run independently and in parallel
    # Our task, from this point forward, is roughly: read in the "parallel_processing_iteration_schedule" file to determine which two files are to be compared in this iteration
    # Read in those two files, run our matching algorithm, and write out the matching results.
    ##########################################################################################################################################################
    
    #1) define our parsing functions
    def to_words(text):
        #Break text into a list of words without punctuation
        return re.findall(r"[a-zA-Z']+", text)
    
    def match(a, b):
        # Make b the longer list.
        if len(a) > len(b):
            a, b = b, a
        # Map each word of b to a list of indices it occupies.
        b2j = {}
        for j, word in enumerate(b):
            b2j.setdefault(word, []).append(j)
        j2len = {}
        nothing = []
        unique = set() # set of all results
        def local_max_at_j(j):
            # maximum match ends with b[j], with length j2len[j]
            length = j2len[j]
            unique.add(" ".join(b[j-length+1: j+1]))
        # during an iteration of the loop, j2len[j] = length of longest
        # match ending with b[j] and the previous word in a
        for word in a:
            # look at all instances of word in b
            j2lenget = j2len.get
            newj2len = {}
            for j in b2j.get(word, nothing):
                newj2len[j] = j2lenget(j-1, 0) + 1
            # which indices have not been extended?  those are
            # (local) maximums
            for j in j2len:
                if j+1 not in newj2len:
                    local_max_at_j(j)
            j2len = newj2len
        # and we may also have local maximums ending at the last word
        for j in j2len:
            local_max_at_j(j)
        return unique
    
    # 2) Read in metadata file. Because this file is huge (1.4 billion lines long), we'll only read the row in which we're currently interested
    with open("reduced_iteration_schedule.txt") as lookup_table:
        for i, line in enumerate(lookup_table):
            if i == int(iteration_number):
                
                #the rows in the iteration schedule look like this: iteration_number    text_one    text_two, so let's grab values and delete trailing newline character
                split_line = line.split("\t")
                file_one = split_line[1]
                file_two = split_line[2].rstrip("\n\r")
                
                with open( str(file_one) ) as open_one:
                    with open( str(file_two) ) as open_two:
                        
                        read_one = open_one.read()
                        read_two = open_two.read()
                        
                        matches = match( to_words(read_one), to_words(read_two) )
            
            #if we made it to the line beyond our current iteration number, we can stop reading that line, as we've found what we're looking for
            elif i > int(iteration_number):
                break
            
    # Now we have a list object named "matches" that contains all identified matches between the two texts compared in this iteration.
    # Let's reduce this list so that it contains only those matches that are three words or longer
    reduced_matches = []
    for i in matches:
        if len(i.split()) > 2:
            reduced_matches.append(i)
    
    # We want to write that to disk, but we can't simply write all matches for all 1.5 billion lookups to the same file, or we'll never be able to open the thing.
    # Let's write the first n iterations to one file (using "append" rather than "write"), then write the next n iterations to a different file
    
    if int(iteration_number) < 100:
        with open("eebo_string_comparison_1.txt","a") as out:
            out.write( str(file_one) + "\t" + str(file_two) + "\t" + str(reduced_matches) + "\n" )

__main__()