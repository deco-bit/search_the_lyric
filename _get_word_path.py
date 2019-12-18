# get hash value for word
import mmh3
i_index_dir = "C:\\Users\\Public\\shit\proj\\i_index"

word = "123"
out_batch_address = ""
hashed = mmh3.hash(word)

mask = 255
# int for folder 1
folder1 = hashed & mask
# int for folder 2
folder2 = (hashed >> 8) & mask
word_i_index_path = i_index_dir + "\\" + "{:0>3d}".format(folder1) + "\\" + "{:0>3d}".format(folder2)
# print(inverted_batch.get("2009"))
# exit(0)
#  dont write word_i_index_path + "\\" + word + ".txt"
append_or_write = ""
output_batch_address = word_i_index_path + "\\" + word + ".txt"

print(output_batch_address)