from mm import treewalk

from pprint import pprint as pprint
import Tkinter as tkinter
import sys
import ttk

# opt_name: (from_, to, increment)
IntOptions = {
    'age': (1.0, 200.0, 1.0),
}

def close_ed(parent, edwin):
    parent.focus_set()
    edwin.destroy()

def set_cell(edwin, w, tvar):
    value = tvar.get()
    w.item(w.focus(), values=(value,))
    close_ed(w, edwin)

def edit_cell(e):
    w = e.widget
    if w and len(w.item(w.focus(), 'values')) > 0:
        edwin = tkinter.Toplevel(e.widget)
        edwin.protocol("WM_DELETE_WINDOW", lambda: close_ed(w, edwin))
        edwin.grab_set()
        edwin.overrideredirect(1)
        opt_name = w.focus()
        (x, y, width, height) = w.bbox(opt_name, 'Values')
        edwin.geometry('%dx%d+%d+%d' % (width, height, w.winfo_rootx() + x, w.winfo_rooty() + y))
        value = w.item(opt_name, 'values')[0]
        tvar = tkinter.StringVar()
        tvar.set(str(value))
        ed = None
        if opt_name in IntOptions:
            constraints = IntOptions[opt_name]
            ed = tkinter.Spinbox(edwin, from_=constraints[0], to=constraints[1],
                increment=constraints[2], textvariable=tvar)
        else:
            ed = tkinter.Entry(edwin, textvariable=tvar)
        if ed:
            ed.config(background='LightYellow')
            #ed.grid(column=0, row=0, sticky=(tkinter.N, tkinter.S, tkinter.W, tkinter.E))
            ed.pack()
            ed.focus_set()
        edwin.bind('<Return>', lambda e: set_cell(edwin, w, tvar))
        edwin.bind('<Escape>', lambda e: close_ed(w, edwin))

def mk_key(TagList, key):
    return '.'.join(TagList+[key])

def JSONTree(Tree, Parent, Dictionery, TagList=[]):
    for key in sorted(Dictionery.keys()) :
        #print("KEY={}, TAGLIST={}".format(key, TagList))
        if isinstance(Dictionery[key], dict):
            #print("## is dict")
            TagList = TagList + [key]
            Tree.insert(Parent, 'end', mk_key(TagList, key), text=key)
            JSONTree(Tree, mk_key(TagList, key), Dictionery[key], TagList)
            #pprint(TagList)
        elif isinstance(Dictionery[key], list):
            #print("## is list")
            Tree.insert(Parent, 'end', mk_key(TagList, key), text=key) # Still working on this
        else:
            #print("## other")
            Tree.insert(Parent, 'end', mk_key(TagList, key), text=key, value=Dictionery[key])

def main():
    # Setup the root UI
    root = tkinter.Tk()
    root.title("JSON editor")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    fname = None
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    Data = treewalk.loadfile(sys.argv[1])


    # Setup the Frames
    TreeFrame = ttk.Frame(root, padding="3")
    TreeFrame.grid(row=0, column=0, sticky=tkinter.NSEW)
    # Setup the Tree
    tree = ttk.Treeview(TreeFrame, columns=('Values'))
    tree.column('Values', width=100, anchor='w')
    tree.heading('Values', text='Values')
    tree.bind('<Double-1>', edit_cell)
    tree.bind('<Return>', edit_cell)
    JSONTree(tree, '', Data)
    tree.pack(fill=tkinter.BOTH, expand=1)
    # Limit windows minimum dimensions
    root.update_idletasks()
    root.minsize(root.winfo_reqwidth(), root.winfo_reqheight())
    root.mainloop()


# Setup Data
DemoData = {
    "firstName": "John",
    "lastName": "Smith",
    "gender": "man",
    "age": 32,
    "address": {
        "address": {
            "streetAddress": "21 2nd Street",
            "city": "New York",
            "state": "NY",
            "postalCode": "10021"},
        "streetAddress": "21 2nd Street",
        "city": "New York",
        "state": "NY",
        "postalCode": "10021"},
    "phoneNumbers": [
        { "type": "home", "number": "212 555-1234" },
        { "type": "fax", "number": "646 555-4567" },
        ]}


if __name__ == "__main__" :
    main()

