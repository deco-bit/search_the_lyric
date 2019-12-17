from tkinter import *
from tkinter import ttk
from tkinter.ttk import Treeview
from helper import *
root_window = Tk()

root_window.title("Search the world of lyrics")
root_window.geometry('450x450')
out_label = Label(root_window, text="")
out_label.grid(column=0, row=3)
query_label = Entry(root_window, width=40)
query_label.grid(column=1, row=0)
query_label.focus_set()

def show_result(r_doc):

    show_window = Toplevel()
    show_window.title("Results")

    label = Label(show_window, text=query_label.get(), font=("Arial", 30)).grid(row=0, columnspan=3)
    # create Treeview with 3 columns
    cols = ('Rank', 'Title', 'Artist', 'Genera')

    listBox = ttk.Treeview(show_window, columns=cols, show='headings',selectmode='browse')

    listBox = Treeview(show_window, columns=cols, show='headings')
    # set column headings
    for col in cols:
        listBox.heading(col, text=col)
    listBox.grid(row=1, column=0, columnspan=2)
    show_window.resizable(width=0, height=0)


    # lis which will be the output to be filled
    tempList = [['Jim', '0.33'], ['Dave', '0.67'], ['James', '0.67'], ['Eden', '0.5'], ]
    tempList.sort(key=lambda e: e[1], reverse=True)

    for doc in r_doc:
        listBox.insert("", "end", values=(r_doc.get(doc), doc))


def open_result():

    path_list, qmatch_list = get_wposting_path(query_label.get())
    idict = get_qdict(path_list)
    r_doc = unsorted_result(idict, qmatch_list)

    # result_window = Toplevel()
    # result_window.title("Result")
    out_label.config(text=str(len(r_doc))+" results found")
    btn2 = Button(root_window, text="Show", height=1, command=lambda: show_result(r_doc))
    btn2.grid(column=1, row=3)


btn = Button(root_window, text="Search", height=1, command=open_result)

btn.grid(column=1, row=1)

root_window.mainloop()