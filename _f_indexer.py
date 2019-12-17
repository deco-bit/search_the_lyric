import csv
from nltk.stem import PorterStemmer
from collections import defaultdict
import time
import re
import io
import winsound


def forward_indexer(stopwords_file, data_set, output_file):
    # string that will hold entire posting of a batch of forward index , this is to avoid loops that will slow program
    out = ""

    try:
        # read stopwords
        f = open(stopwords_file, 'r')

    except Exception as e:
        print(e)
        f.close()

    # rstrip() method returns a copy of the string with trailing characters removed
    stopwords = [line.rstrip() for line in f]

    # close stopwords file
    f.close()

    sw_d = dict.fromkeys(stopwords)
    ps = PorterStemmer()

    # forward_batch is a dictionary, its key is word and element is a list of positions
    forward_batch = {}

    try:

        with open(data_set, encoding="utf8", errors='ignore') as csvFile:

            # creating a csv reader object
            read_csv = csv.reader(csvFile, delimiter=',')

            # parse row-wise
            for row in read_csv:
                # if row[0] != "8651":
                #     continue

                # concatenate title,year,artist,genre and lyric
                title = row[1]
                year = row[2]
                artist = row[3]
                genera = row[4]
                # row[5] = lyric
                tuple_a = row[1] + " " + row[2] + " " + row[3] + " " + row[4] + " " + row[5]

                # wrd_loci is all the possible locations of word
                # on the basis of which precedence could be given to it on a query
                wrd_loci = row[1] + " " + row[2] + " " + row[3] + " " + row[4]

                # to check whether the word in any of wrd_loci we must convert wrd_loci into the form in which
                # our corpus is indexed that is we must convert them to lower case and stem them

                wrd_loci = wrd_loci.lower()

                # get only alphanumeric and replace other by space
                # put spaces instead of non-alphanumeric characters
                wrd_loci = re.sub(r'[^a-z0-9 ]', ' ', wrd_loci)

                # convert to list
                wrd_loci = wrd_loci.split()

                # eliminate the stopwords
                wrd_loci = [x for x in wrd_loci if x not in stopwords]

                wrd_loci = [ps.stem(word) for word in wrd_loci]

                # lowercase all
                # tuple_a is an entire tuple entire tuple of excel
                tuple_a = tuple_a.lower()

                # get only alphanumeric and replace other by space
                tokens = re.sub(r'[^a-z0-9 ]', ' ', tuple_a)  # put spaces instead of non-alphanumeric characters

                # convert tokens string into a list so that it gets easy to remove stop words
                tokens = tokens.split()

                tokens = [x for x in tokens if x not in stopwords]  # eliminate the stopwords
                # stemming tokens
                tokens = [ps.stem(word) for word in tokens]
                doc_size = len(tokens)

                # index storing index of word in tokenized  list
                for index, word in enumerate(tokens):

                    # whether word is located in title/artist_name/year/genera or not
                    # if it is in these columns then in how many of them it is present
                    # this location weight will be used for ranking purpose
                    location_weight = 0

                    for wrd_locus in wrd_loci:
                        if word == wrd_locus:
                            location_weight = location_weight + 1

                    # storing (|)+word in dictionary, this is to make inverted indexing easier,
                    # | will act as signal character for word while reading forward index file
                    if "(|)" + word in forward_batch:
                        forward_batch["(|)" + word].append(index)

                    else:
                        temp_list = [str(location_weight / 10), index]
                        forward_batch["(|)" + word] = temp_list

                out = out + row[0] + "," + str(doc_size) + "," + str(forward_batch) + "\n"
                forward_batch = {}
                tokens = []
    except Exception as e:
        # print(tuple_a)
        freq = 2500
        duration = 1000

        winsound.Beep(freq, duration)
        print("doc:" + row[0] + " index: " + index + " word: " + word)
        print("In Read:" + str(e))
        # no need to close as "with open" method automatically does this

    try:
        # print(out)

        with open(output_file, "w", encoding="utf8") as fileOut:

            fileOut.write(out)
    except Exception as e:
        freq = 2500
        duration = 1000

        winsound.Beep(freq, duration)
        print("In write:" + str(e))
        # no need to close as "with open" method automatically does this


start = time.time()

end = time.time()
print(end - start)

freq = 2500
duration = 1000

winsound.Beep(freq, duration)
