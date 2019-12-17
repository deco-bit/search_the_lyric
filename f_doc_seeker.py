import csv
from f_indexer import forward_indexer
from os import listdir
from os.path import os
from os.path import isfile, join
from helper import docs_path, indexed_docs_path, f_index_path, stopwords_path, docs_subdir_path,read_doc_sub_directories
from helper import get_out_path_for_f_index

output_path = ""
sub_d=""
while 1 == 1:

    # get name of all documents in the directory which contain only those documents that are indexed or are to be
    # indexed
    docs = [fa for fa in listdir(docs_path) if isfile(join(docs_path, fa))]

    # docs_indexed contain name of the documents in doc_path/docs that are already indexed
    docs_indexed = [f for f in listdir(indexed_docs_path) if isfile(join(indexed_docs_path, f))]

    # extracting name of folder in f_index directory
    # f_index directory contain forward indices
    # if data set contain multiple files then f_index contain folder for each file and in it contains its forward_index
    dir_dict = {}

    for doc in docs:

        f_index_folder = [dI for dI in os.listdir(f_index_path) if os.path.isdir(os.path.join(f_index_path, dI))]

        # reading doc_subdirectories file to get name of all files that are indexed
        dir_dict = read_doc_sub_directories()

        # if doc not in indexed directory then it needs to be indexed
        if doc not in dir_dict:
            # if f_index list is empty it means no folder in directory
            output_path,sub_d = get_out_path_for_f_index(doc,dir_dict,f_index_folder)

            # docs_path_n is the path of nth doc in docs_path directory
            docs_path_n = docs_path + "\\" + str(doc)
            forward_indexer(stopwords_path, docs_path_n, output_path)

            # against new forward index document write name of the folder it is stored in
            with open(docs_subdir_path, 'a') as out:
                writer = csv.writer(out)
                writer.writerow([str(doc), sub_d])
