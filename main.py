import tkinter as tk
import tkinter.scrolledtext as scrolledText
from get_read_mails import get_service,get_message,search_message,delete_message
import os

GMAIL = ""

def make_menu(w):
    global the_menu
    the_menu = tk.Menu(w, tearoff=0)
    the_menu.add_command(label="Cut")
    the_menu.add_command(label="Copy")
    the_menu.add_command(label="Paste")

def show_menu(e):
    w = e.widget
    the_menu.entryconfigure("Cut",
    command=lambda: w.event_generate("<<Cut>>"))
    the_menu.entryconfigure("Copy",
    command=lambda: w.event_generate("<<Copy>>"))
    the_menu.entryconfigure("Paste",
    command=lambda: w.event_generate("<<Paste>>"))
    the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)

def get_id():
    out =  search_message(get_service(),GMAIL,search_entry.get())
    for i in out:
        mylist.insert(tk.END,i)

def get_msg(id):
    out = get_message(get_service(),GMAIL,id)
    show_msg_text.insert(tk.INSERT,out)

root = tk.Tk()
root.geometry("1200x650")

search_frame = tk.Frame(root,bg="#121212")
search_frame.place(relx=0.5,rely=0.05,relheight=0.05,relwidth=0.8,anchor="n")

search_entry = tk.Entry(search_frame,font=("Helvetica",12))
search_entry.place(relx = 0.05,relheight=1,relwidth=0.65)

id_search_button = tk.Button(search_frame,bg="#4700b3",command =get_id,text = "get id" )
id_search_button.place(relx=0.75,relheight=1,relwidth = 0.09)

msg_search_button = tk.Button(search_frame,bg="#4700b3",command =lambda : get_msg(search_entry.get()),text ="get msg" )
msg_search_button.place(relx=0.9,relheight=1,relwidth = 0.09)

show_id_frame = tk.Frame(root)
show_id_frame.place(rely=0.2,relheight=0.4,relwidth=0.2)

show_id_text = tk.Scrollbar(show_id_frame,orient="vertical",bg="#4700b3")
show_id_text.pack(side = tk.RIGHT,fill=tk.Y)

mylist = tk.Listbox(show_id_frame, yscrollcommand = show_id_text.set )

mylist.pack(side=tk.LEFT,fill=tk.BOTH)
show_id_text.config(command= mylist.yview)

show_msg_frame = tk.Frame(root)
show_msg_frame.place(relx = 0.3,rely=0.15,relwidth= 0.7,relheight=0.8)

show_msg_text = tk.Text(show_msg_frame,bg="#121212",fg="#cccccc")
show_msg_text.place(relheight=1,relwidth=1)

make_menu(root)
e1 = tk.Entry()

e1.place(relx=0.3,relwidth=0.4)
e1.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)

utils = tk.Frame(root,bg="#121212")
utils.place(relx=0.025,rely=0.65,relwidth=0.175,relheight=0.3)

delete_button = tk.Button(utils,text="Delete message with this id",command=lambda : delete_message(get_service(),GMAIL,search_entry.get()))
delete_button.grid(row=0,column=0)

root.mainloop()
