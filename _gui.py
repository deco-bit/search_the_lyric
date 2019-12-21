import time
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Treeview
from _helper import *

root_window = Tk()

root_window.title("Search the world of lyrics")
root_window.geometry('450x450')
out_label = Label(root_window, text="")
out_label.grid(column=0, row=3)
query_label = Entry(root_window, width=40)
query_label.grid(column=1, row=0)
query_label.focus_set()


def show_result(_sorted_r):
    show_window = Toplevel()
    show_window.title("Results")

    label = Label(show_window, text=query_label.get(), font=("Arial", 30)).grid(row=0, columnspan=3)
    # create Treeview with 3 columns
    cols = ('Rank', 'Title', 'Year', 'Artist', 'Genera')

    listBox = ttk.Treeview(show_window, columns=cols, show='headings', selectmode='browse')

    listBox = Treeview(show_window, columns=cols, show='headings')
    # set column headings
    for col in cols:
        listBox.heading(col, text=col)
    listBox.grid(row=1, column=0, columnspan=2)
    show_window.resizable(width=0, height=0)
    tyag = []
    for doc in _sorted_r:
        full_hashed_address, hashed_path, restricted = get_hashed_directory(title_year_artist_genera_dir, str(doc), 255)

        with open(full_hashed_address, 'r') as file:
            for row in file:
                tyag = re.sub(r'"', ' ', row)
                tyag = tyag.split(",")
                break
        if len(tyag) == 3:
            listBox.insert("", "end", values=(_sorted_r.get(doc), tyag[0], tyag[1], tyag[2]))
        if len(tyag) == 4:
            listBox.insert("", "end", values=(_sorted_r.get(doc), tyag[0], tyag[1], tyag[2],tyag[3]))

def open_result():

    start = time.time_ns()
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    path_list, qmatch_list = get_wposting_path(query_label.get())

    end = time.time_ns()
    print("get_wposting_path time below")
    print(end - start)

    start = time.time_ns()

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    idict = get_qdict(path_list)

    end = time.time_ns()
    print("get_qdict time below")
    # print(idict.items())
    print(end - start)
    # exit(0)
    start = time.time_ns()

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    r_doc = unsorted_result(idict, qmatch_list)
    end = time.time_ns()
    print("unsorted_result time below")
    print(end - start)

    # result_window = Toplevel()
    # result_window.title("Result")
    out_label.config(text=str(len(r_doc)) + " results found")
    btn2 = Button(root_window, text="Show", height=1, command=lambda: show_result(_sorted_r))
    btn2.grid(column=1, row=3)
    _sorted_r = sort_result(r_doc)


btn = Button(root_window, text="Search", height=1, command=open_result)

btn.grid(column=1, row=1)

root_window.mainloop()
