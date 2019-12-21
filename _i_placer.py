import winsound

from _i_indexer import inverted_indexer
from _helper import *

count = 0
while 1:
    dir_dict_i = get_sub_dir_of_findex(docs_subdir_log)
    i_dict = read_ilog()
    # print(i_dict)
    # exit(0)
    # inverted_batch = {}
    for key in dir_dict_i:
        inverted_batch = {}



        if key not in i_dict:
            print("Batch ", key, " inverted indexing started")
            start = time.time()
            print(key, str(dir_dict_i))
            f_index = f_index_main_dir + "\\" + dir_dict_i[key] + "\\" + key
            inverted_batch = inverted_indexer(f_index)
            # count = count + 1
            # if count == 2:
                # exit(0)
            # print(inverted_batch)
            for word in inverted_batch:
                # full_hashed_address, hashed_path, restricted = get_hashed_directory(i_index_dir, word, 255)
                # check_for_path(hashed_path)
                # output_on_hashed_path(inverted_batch, full_hashed_address, word, restricted)
                # print(word)
                store_on_hashed_directory(word, inverted_batch, i_index_dir, 1)


            with open(i_log, 'a') as out:
                writer = csv.writer(out)
                writer.writerow([key, str(1)])
            end = time.time()
            print("Batch ", key, " inverted Index Stored, time taken is written below")
            print(end - start)

