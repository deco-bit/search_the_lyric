import os
import pickle
import time

from nltk.stem import PorterStemmer
import re
import mmh3
import csv
import copy
import operator
import math

title_year_artist_genera_dir = "C:\\Users\\Public\\shit\\proj\\title_year_artist_genera"

# chose any path  -> this is the path where you will get all inverted indexes
i_index_dir = "C:\\Users\\Public\\shit\\proj\\i_index"

# chose any path  -> this is the path where you will get all forward indexes
f_index_main_dir = "C:\\Users\\Public\\shit\\proj\\f_index"

# add any path in place of what given below but make sure it has  *text file in it* ,
# make sure that below path should match with whatever path you chose for
# **indexed_doc_path** declared and defined below
docs_subdir_log = 'C:\\Users\\Public\\shit\\proj\\docs_indexed\\doc_subdirectories.txt'

# chose any path -> this path must contain .csv file of dataset given at
# "https://www.kaggle.com/gyani95/380000-lyrics-from-metrolyrics"

i_log = "C:\\Users\\Public\\shit\\proj\\findex_i_indexed\\findex_i_indexed.txt"

#      ******************   NOTE   ******************************

# The dataset given above is faulty, it has many places where rows of one field got mixed into another

# TO see the fault open file converted in utf-8 , .csv format and search
# (I promise to kill them all til everybody's misse)
# after this line there should be a new document (following csv format) but there is not tag/pattern for new file
# You can fix it but checking that single quotation mark (") should only come in start of row and at end of it,
# every other single quotation in between these two should be escaped using one more quotation i.e ("").

docs_path = "C:\\Users\\Public\\shit\\proj\\docs"

# make sure you have a text file on below path, file name = "doc_subdirectories.txt"
indexed_docs_path = "C:\\Users\\Public\\shit\\proj\\docs_indexed"

# make sure you download stop words file and put it with name "stopwords.dat" on below path
stopwords_path = "C:\\Users\\Public\\shit\\proj\\stopwords\\stopwords.dat"
f_index_path = "C:\\Users\\Public\\shit\\proj\\f_index"
# f_placer

dict_rest = {"con": 1, "prn": 1, "aux": 1, "nul": 1, "com1": 1, "com2": 1, "com": 1, "com4": 1, "com5": 1,
             "com6": 1,
             "com7": 1,
             "com8": 1, "com9": 1, "lpt1": 1, "lpt2": 1, "lpt3": 1, "lpt4": 1, "lpt5": 1,
             "lpt6": 1, "lpt7": 1, "lpt8": 1, "lpt9": 1}


# pick a folder you have ...
def get_size(path):
    folder = path
    size = 0
    for (path, dirs, files) in os.walk(folder):
        for file in files:
            filename = os.path.join(path, file)
            size += os.path.getsize(filename)
            size = size / 1024 * 1024.0
            size = size / 1048576
    return size


def query_parser(stopwords_path_, query):
    f = None
    try:
        # read stopwords
        f = open(stopwords_path_, 'r')

    except Exception as e:
        print(e)

    # rstrip() method returns a copy of the string with trailing characters removed
    stopwords = [line.rstrip() for line in f]
    #
    # tokens = [ps.stem(word) for word in  [x for x in (re.sub(r'[^a-z0-9 ]', ' ', query.lower())).split() if x not
    # in [line.rstrip() for line in f]]]

    # close stopwords file
    f.close()

    # sw_d = dict.fromkeys(stopwords) don't remember why wrote this
    ps = PorterStemmer()

    query = query.lower()
    tokens = re.sub(r'[^a-z0-9 ]', ' ', query)
    tokens = tokens.split()

    tokens = [x for x in tokens if x not in stopwords]  # eliminate the stopwords
    # stemming tokens
    tokens = [ps.stem(word) for word in tokens]

    return tokens


def get_stopword_path():
    return stopwords_path


# free word query
# free word query
def get_qdict(path_list):
    # count = 0
    # word_signal = 0
    # temp = 0
    # idict = {}
    # start_signal = 1
    # postings_signal = 0
    # word = ""
    # forgot why declared above seven

    doc_signal = 0
    pos_signal = 0

    doc = ""
    idict = {}

    for path in path_list:

        with open(path, "rb") as pickle_read:
            # read_csv = csv.reader(csvFile)
            word = os.path.basename(path)[0:-7]
            idict[word] = pickle.load(pickle_read)

            # for row in read_csv:
            #
            #     # tupleD = str(row)
            #     # tokens = re.sub(r'[^\[\.#a-z0-9]', ' ', row)
            #     # tokens = tokens.split()
            #     start = time.time_ns()
            #     print(str(row))
            #     tokens = (re.sub(r'[^\[\.#a-z0-9]', ' ', str(row))).split()
            #     # print(tokens)
            #     end = time.time_ns()
            #     print("pos_sig")
            #     print(end - start)
            #
            #     for t_word in tokens:

                    # if t_word == "|":
                    #     word_signal = 1
                    #     continue
                    # if t_word == "#":
                    #     doc_signal = 1
                    #     pos_signal = 0
                    #
                    #     continue
                    # if t_word == "[":
                    #     pos_signal = 1
                    #     weight_signal = 0
                    #     continue

                    # if doc_signal == 1:  # correct print order
                    #
                    #     doc = int(t_word)
                    #     if not idict.get(word):
                    #         idict[word] = {doc: []}
                    #     else:
                    #         idict.get(word).update({doc: []})
                    #
                    #     doc_signal = 0

                    # if pos_signal == 1:
                    #
                    #     # below specific way of code is simply not to repeatedly increase weight_signal
                    #     # when it is not required anymore
                    #     if weight_signal > 1:
                    #         idict.get(word).get(doc).append(int(t_word))
                    #
                    #     elif weight_signal == 0:
                    #         idict.get(word).get(doc).append(int(t_word))
                    #         weight_signal = weight_signal + 1
                    #     elif weight_signal == 1:
                    #         idict.get(word).get(doc).append(float(t_word))
                    #         weight_signal = weight_signal + 1
                # end = time.time_ns()
                # print("pos_sig")
                # print(end - start)
    return idict


def get_wposting_path(query_string):
    path_list = []
    restr = 0
    qmatch_list = []
    tokens = dict.fromkeys(query_parser(stopwords_path, query_string))

    for word in tokens:
        if word in dict_rest:
            word = word[1:]
            restr = 1

        # get hash value for word
        hashed = mmh3.hash(word)

        # int for folder 1
        folder1 = hashed & 255
        # int for folder 2
        folder2 = (hashed >> 8) & 255
        word_i_index_path = i_index_dir + "\\" + "{:0>3d}".format(folder1) + "\\" + "{:0>3d}".format(folder2)

        output_batch_address = word_i_index_path + "\\" + word + ".pickle"

        if os.path.exists(output_batch_address):
            path_list.append(output_batch_address)
            # print(path_list)
            # exit(0)
            if restr == 1:
                restr == 0

                # order of if conditions is on the basis of probability of occurance of a particular word
                if word[0] == "o":
                    word = "c" + word
                elif word[0] == "p":
                    key_word = "l" + word
                elif word[0] == "u":
                    if word[1] == "x":
                        key_word = "a" + word
                    elif word[1] == "l":
                        key_word = "n" + word
                elif word[0] == "r":
                    key_word = "p" + word

            qmatch_list.append(word)

            # .extend stores character wise.

    return path_list, qmatch_list


def unsorted_result(idict, query_list):
    # intersection of documents on the basis of occurence of words of query
    doc_list = []

    # print((idict.get("ego").get("0")))
    # exit(0)
    # below variable is used to calculate the IDF -> inverse document frequency
    doc_with_required_terms = 0

    # we have to DEEP copy idict because idict has both doc_size and location_weight which we dont be needing next
    idict_nosize = copy.deepcopy(idict)

    # below code needs optimization
    for word in idict_nosize:
        for doc in idict_nosize.get(word):
            # [2:] below     -> 0 for doc_size and 1 for location_weight
            idict_nosize.get(word).update({doc: idict.get(word)[doc][2:]})

        # erraneoous             idict_nosize.get(word)[doc] = {doc:idict.get(word)[doc][1:]}

    # doc_list is a list of lists which conatin docs whcich have atleast one of the query word
    # for each word there could be one or more documents
    # each document against a word get placed in a list within doc_list
    for word in query_list:
        doc_list.append(list(idict.get(word).keys()))

    # each sublist correspond to a word of query
    # intersection of sublists means that resulting list corresponds to entire processed query not part of it
    # it yields only those documents that have all the words of processed query

    # there is possibility that doc_list is empty (when queried word do not exists in dataset)
    # In that case doc_list won't be empty but

    if len(doc_list) >= 1:
        intersected_list = list(set.intersection(*map(set, doc_list)))
    else:
        intersected_list = []

    # intersection of the documents on the basis of position of words in it
    r_doc = {}
    # posting_list

    # intersected_list has all documents that have all words of query
    # now intersecting on the basis of position of words

    for doc in intersected_list:
        # float(idict.get(query_list[0])[doc][1]) is the location weight we given to each word of corpus
        r_doc.update({doc: float(idict.get(query_list[0])[doc][1])})


        # we loop words of query in loop of docs (docs which have all query words)
        # if word is first word of query then do not make any change in positions
        first_word = 1

        # subtract word_no from subsequent word positions if first_word == 0
        word_no = -1

        # posting_list is list of lists
        # each sublist holds the non shifted(for first word)/shifted positions of one of the processed query words
        posting_list = []
        for word in query_list:
            word_no = word_no + 1
            if first_word:
                first_word = 0

                posting_list.append((idict_nosize.get(word)[doc]))
                continue
            else:
                # print(type((idict_nosize.get(word)[doc][0])))
                # exit(0)
                idict_nosize.get(word)[doc] = [x - word_no for x in idict_nosize.get(word)[doc]]
                posting_list.append(idict_nosize.get(word)[doc])

        posting_list2 = list(set.intersection(*map(set, posting_list)))
        if len(posting_list2) != 0:
            # r_doc.append(doc)

            doc_with_required_terms = doc_with_required_terms + 1

            # second operand of the plus in the below line is TF -> term frequency

            # print(type(r_doc.get(doc)))
            # print(type(float((len(posting_list2)))))
            #
            # # use be4low code to debug about query_list[0]
            # print(type(float((idict.get(query_list[0])[doc][0]))))
            # exit(0)
            # print(type(float((idict.get(query_list[0])[doc][0]))))
            r_doc[doc] = (r_doc.get(doc)) + float(len(posting_list2)) / float((idict.get(query_list[0])[doc][0]))

            # IDF equation below
    if doc_with_required_terms == 0:
        return r_doc
    else:
        idf = math.log(float(40134 / doc_with_required_terms), 10)

    for doc in r_doc:
        r_doc[doc] = float(r_doc.get(doc) * idf)

    return r_doc


def sort_result(r_doc):
    if r_doc == -1:
        # idiot len(r_doc)==0
        return -1
    else:

        sorted_r = {k: v for k, v in sorted(r_doc.items(), key=operator.itemgetter(1), reverse=True)}
        return sorted_r


def get_hashed_directory(higher_directory, key_word, mask):
    # higher_directory is the place where subdirectories are to be created
    # key_word is the word which is used to make hashed_directory on runtime

    restricted = 0
    if key_word in dict_rest:
        # there could be two logics to cater for restricted words
        # append/ change word for immutable objects passing acts as pass by value so you have to return this
        # changes string here and return string to outer function -> this is relatively slow process

        # better approach is to find a pattern in the restricted words, make use of that pattern
        # if you notice for restricted words you can just remove first letter
        # restricted signal will tell whether the letter is removed or not
        # if letter is removed then make use of pattern you observed in restricted words

        # if restricted is one and the first letter is o then just append c in the start
        #  if restricted is one and the first letter is p then just append l in the start
        #  if restricted is one and the first letter is r then just append p in the start
        # if restricted is one and the first letter is u then check for second letter
        key_word = key_word[1:]
        restricted = 1

    # get hash value for word
    hashed = mmh3.hash(key_word)
    # declare mask
    # int for folder 1
    folder1 = hashed & mask
    # int for folder 2
    folder2 = (hashed >> 8) & mask
    hashed_path = higher_directory + "\\" + "{:0>3d}".format(folder1) + "\\" + "{:0>3d}".format(folder2)
    # print(inverted_batch.get("2009"))
    # exit(0)
    #  dont write word_i_index_path + "\\" + word + ".txt"

    # forgot why declared below var
    # append_or_write = ""

    # hashed_path is path of folder where file is placed or to be placed
    # full_hashed_address is the full address of the file including the extension
    full_hashed_address = hashed_path + "\\" + key_word + ".pickle"
    return full_hashed_address, hashed_path, restricted


def check_for_path(hashed_path):
    if not os.path.exists(hashed_path):
        # with open (full_hashed_address,"wb") as p_file:
        #     pickle.dump({},p_file)
        os.makedirs(hashed_path)
        # append_or_write = 'w'


# information to be stored on hashed path, hashed path, base word (base word could be different from key word)
# restricted word flag, and a flag to tell whether the information is nested dictionary or string
def output_on_hashed_path(information, full_hashed_address, key_word, restricted, single_nested_dict_or_str):
    if restricted == 1:
        # if restricted is one and the first letter is o then just append c in the start
        #  if restricted is one and the first letter is p then just append l in the start
        #  if restricted is one and the first letter is r then just append p in the start
        # if restricted is one and the first letter is u then check for second letter

        # order of if conditions is on the basis of probability of occurance of a particular word
        if key_word[0] == "o":
            key_word = "c" + key_word
        elif key_word[0] == "p":
            key_word = "l" + key_word
        elif key_word[0] == "u":
            if key_word[1] == "x":
                key_word = "a" + key_word
            elif key_word[1] == "l":
                key_word = "n" + key_word
        elif key_word[0] == "r":
            key_word = "p" + key_word
    # pickle_in = open ( full_hashed_address , "rb" )
    # pickle_in =  pickle.load(pickle_in)
    # print(full_hashed_address)
    # exit(0)
    pickle_in = {}
    if os.path.exists(full_hashed_address):

        if os.path.getsize(full_hashed_address) > 0:
            with open(full_hashed_address, "rb") as input_file:
                pickle_in = pickle.load(input_file)

    with open(full_hashed_address, "wb") as out:

        # writer = csv.writer(out)
        if single_nested_dict_or_str == 1:
            # print(pickle_in)
            # exit(9)
            pickle_in.update(information[key_word].items())
            pickle.dump(pickle_in, out)
            # writer.writerow(information[key_word].items())
            # information[key_word].items() is entire posting list of a word. it is an entire dictionary

        # string case is ditched
        # if single_nested_dict_or_str == 0:
        #     writer.writerow([information])


def get_sub_dir_of_findex(sub_dir_log_file_path):
    dir_dict_i = {}
    with open(sub_dir_log_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row:
                dir_dict_i[row[0]] = row[1]
    return dir_dict_i


def read_doc_sub_directories():
    # reading doc_subdirectories file to get name of all files that are indexed
    dir_dict = {}
    with open(docs_subdir_log, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row:
                dir_dict[row[0]] = row[1]
    return dir_dict


def read_ilog():
    _ilog = {}
    with open(i_log, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row:
                _ilog[row[0]] = row[1]
    return _ilog


def get_out_path_for_f_index(doc, f_index_folder):
    output_path = ""

    # sub_d is required to update the sub directory of the forward index of a particular document
    sub_d = str(doc)[:-4]
    if len(f_index_folder) == 0:
        # if f_index is empty it means not a single document is indexed
        # it means first folder is to be created let its name be the name of the document
        # if at the time of indexing of next document size of this folder is less then a certain threshold
        # then that document index is also stored in folder having name of previous document
        # %%%%%%%%%%%%%%%%%% to_do:    give folders proper naming
        path = f_index_path + "\\" + str(doc)[:-4]

        if not os.path.exists(path):
            os.makedirs(path)
        output_path = path + "\\" + str(doc)

        # forgot use of below commented code
        # now update f_index so that it contains name of newly created folder too
        # f_index_folder = [dI for dI in os.listdir(f_index_path) if
        #                   os.path.isdir(os.path.join(f_index_path, dI))]

    else:
        # data = {}
        # available_dir keeps track whether int he f_index directory there is any folder
        # whose size if less then our threshold limit
        available_dir = 0

        # f_index below is list containing name of all folders that are in f_index directory
        for f in f_index_folder:

            # maybe useless
            # available_dir = available_dir + 1

            # if size of folder is less then 50 MB then select this folder to store new forward_index
            if get_size(f_index_path + str(f)) < 50:
                output_path = f_index_path + "\\" + str(f) + "\\" + str(doc)
                sub_d = str(f)
                available_dir = 1
                break

        # if no folder in f_index with required limit of size then create new
        if available_dir == 0:
            path = f_index_path + "\\" + str(doc)[:-4]
            if not os.path.exists(path):
                os.makedirs(path)
            output_path = f_index_path + "\\" + str(doc)[:-4] + "\\" + str(doc)

    return output_path, sub_d


def store_on_hashed_directory(key_word, information, base_directory, single_nested_dict_or_str):
    # exit(0)
    full_hashed_address, hashed_path, restricted = get_hashed_directory(base_directory, key_word, 255)
    check_for_path(hashed_path)

    output_on_hashed_path(information, full_hashed_address, key_word, restricted, single_nested_dict_or_str)
