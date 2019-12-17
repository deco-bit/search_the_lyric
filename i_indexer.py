import csv
import re
import time
import winsound


def inverted_indexer(forwardindex_file):
    # inverted index ad dictionary
    inverted_batch = {}

    # tells whether next word in list is keyword or position in doc
    word_signal = 0

    # tells whether next word in list is keyword or position in doc
    pos_signal = 0

    try:

        with open(forwardindex_file) as csvFile:
            # creating a csv reader object
            read_csv = csv.reader(csvFile)

            for row in read_csv:

                # tuple_a is an entire tuple entire tuple of
                tuple_a = str(row)
                pos_signal = 0
                # put spaces instead of non-alphanumeric characters
                tokens = re.sub(r'[^\|\.a-z0-9-]', ' ', tuple_a)

                tokens = tokens.split()

                # adding "#" before each docNumber as a signal word, it will be simplify parsing of invertedIndex file
                doc_no = "(#)" + row[0]
                doc_size = row[1]

                for word in tokens:

                    # if word is "|" then it means next word is word to be added as key in dictionary.
                    if word == "|":

                        # make word signal 1, it make next iteration to consider word as key to be added or used in
                        # dictionary
                        word_signal = 1

                        # next word is not position so make position signal = 0
                        pos_signal = 0
                        continue

                    # if word Signal is 1 it means this word is word to be used in dictionary
                    elif word_signal == 1:

                        # store this word as temp, (|) concatenated before using this word in dictionary,
                        # this will be used as signal word for reading back inverted index file
                        temp_word = word

                        # make position signal 1 because next items of list are positions of this word
                        pos_signal = 1
                        # word has been recorded now next item is not a word of dictionary
                        word_signal = 0
                        continue

                    elif pos_signal == 1:
                        # check if temp word is in inverted_batch dictionary
                        if temp_word in inverted_batch:
                            # if word is in inverted_batch dict then check whether new document is in it
                            # you dont check in doc_dict you check in doc_dict of corresponding word

                            if doc_no in inverted_batch.get(temp_word):

                                # if word is in inverted dict and doc_no also in doc_dict of inverteddict
                                # then add positions in docDic value(list)

                                (inverted_batch.get(temp_word)).get(doc_no).append(word)



                            else:
                                # if there is no key for docNO in doc_dict dict then add it

                                inverted_batch.get(temp_word)[doc_no] = [doc_size, word]



                        else:
                            inverted_batch[temp_word] = {doc_no: [doc_size, word]}

                            # MUST NOTE : A TOUGH BUG : above one line code is replaced by below three line codes(
                            # which gave wrong answer) tempDocList = [word] doc_dict[doc_no] = tempDocList
                            # inverted_batch[temp_word] = doc_dict

    except Exception as e:
        print(e)
    return inverted_batch
