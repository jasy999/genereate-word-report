####################################################################################################
# DESCRIPTION
#   Python to generate a detailed report the word and its frequecy of occurances in all the files
#   under a folder. The script also generated a log file with processing logs. The script also
#   excludes numbers during processing and removes punctations added in the end of the words.
#
# INPUT
#    Directory/Folder name
# OUTPUT
#   List of words with its corresponding frequecy of occurances
#
# USAGE
#   This script can be used as a function by using import statement. It can also be used via CLI
#   using the following command.
#
#       get_unique_words_report.py <input-folder-name>
#
####################################################################################################

import os
import sys
import re
import logging
import string

def get_unique_words (dir_path):
    #Log file to capture processing logs
    logging.basicConfig(filename='unique_words_report.log', encoding='utf-8', level=logging.DEBUG)

    #Split text based on delimiters ;,. and empty space
    spliter = ";\s*|,\s*|\.\s*|\s+"

    all_files = []
    words_report = {}

    #Gathering all the file names under the directory and its subdirectory
    for r,d,f in os.walk(dir_path):
        for file in f:
            all_files.append (os.path.join(r,file))

    #Processing files one by one
    for file in all_files:
        logging.info('Processing file ' + file)
        file_content = ""
        file_obj = open (file)
        try:
            file_content = file_obj.read()
        except:
            #If we are unable to read a file, the it is a non-text file (or has Non-ASCII letters)
            logging.error(file + ' is not a plain text based ASCII file.')
            continue
        file_obj.close()

        #Converting all the letters to lower case to make he script case insenstive
        file_content = file_content.lower()

        #Using regex split function to split based on ;,. and empty space (stored in spliter variable)
        words = re.split(spliter, file_content)

        #Removed empty string and punctuations at the begining and end
        words = [word.strip(string.punctuation) for word in words if word.strip() != ""]
        unique_words = set (words)

        for unique_word in unique_words:
            #Ignoring numbers from the list
            if (unique_word.isnumeric()):
                logging.debug('Ignoring the number {0} in the file {1}'.format (unique_word, file))
                continue
            elif unique_word =="":
                continue
            if unique_word in words_report:
                words_report [unique_word] += words.count(unique_word)
            else:
                words_report [unique_word] = words.count(unique_word)
        logging.info('Finished processing file ' + file)

    #Sorting the list based on frequency
    sorted_word_report = sorted(words_report.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    for word, frequency in sorted_word_report:
        print ("{0} {1}".format (word, frequency))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print ("Usage")
        print ("-----")
        print ("\t{0} <input-folder-name>".format (sys.argv[0]))
    else:
        get_unique_words (sys.argv[1])
