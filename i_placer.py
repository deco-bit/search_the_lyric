from i_indexer import inverted_indexer
from helper import *

while 1:
    dir_dict_i = get_sub_dir_of_findex(docs_subdir_log)
    inverted_batch = {}
    for key in dir_dict_i:
        f_index = f_index_main_dir + "\\" + dir_dict_i[key] + "\\" + key
        inverted_batch = inverted_indexer(f_index)

        for word in inverted_batch:
            full_hashed_address, hashed_path, restricted = get_hashed_directory(i_index_dir, word, 255)
            check_for_path(hashed_path)
            output_on_hashed_path(inverted_batch, full_hashed_address, word, restricted)
