import time
import winsound

from helper import *

#  code wont work because file name not included in the dictionary as a key
# to do this you have to get file name while reading the file

query = "ego"

start = time.time_ns()

path_list, qmatch_list = get_wposting_path(query)
idict = get_qdict(path_list)
# print(idict)
# print(list1, list3)


r_doc = unsorted_result(idict, qmatch_list)
print(str(len(r_doc)))
exit(0)
# print(r_doc)
if sort_result(r_doc)==-1:
    print("no documnets found")
else:
    print("unsorted")
    print(r_doc)
    print("sorted")
    print(sort_result(r_doc))

# exit(0)
# print(intersected_list)
# print(idict.get("good")[38932])
end = time.time_ns()
print(end - start)

freq = 2500
duration = 1000

winsound.Beep(freq, duration)
