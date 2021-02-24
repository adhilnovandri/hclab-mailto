#!venv/scripts/python

from tkinter import * 
from kelas.Mailto import Mailto
import json,os

def send():
    infoLabel.config(text="Processing to sent email...")
    try:
        m = Mailto(email.get(),labno.get())
        m.sendEmail()
        infoLabel.config(text="Email sent!")
    except:
        infoLabel.config(text="Email failed to sent")

def preview():
    with open('application.json','r') as f:
        setting = json.load(f)
    path = setting['mail']['attachment_path']
    try:
        os.startfile(os.path.join(path,str(labno.get())+'.pdf'))
    except:
        infoLabel.config(text=f"File {labno.get()}.pdf not found!")
    

root = Tk()
root.title("HCLAB Email - RSAB. Harapan Kita")
root.geometry("520x170")
root.resizable(0,0)

#init components
labnoLabel = Label(root,text="Lab No.",anchor="e",font=("Courier",11))
labno = Entry(root, width=12, borderwidth=2)
emailLabel = Label(root,text="Email Address",anchor="e",font=("Courier",11))
email = Entry(root, width=12,  borderwidth=2)
previewButton = Button(root,text="Preview",width=7,height=1,border=2,font=("Courier",11,"bold"))
sendButton = Button(root,text="Send",width=7,height=1,border=2,font=("Courier",11,"bold"))
infoLabel = Label(root,anchor="e",font=("Courier",11))

#positioning components
labnoLabel.grid(row=1,column=1,padx=2,pady=5,sticky=W+E)
labno.grid(row=1,column=2,columnspan=3,padx=5,pady=3,sticky=W+E)
emailLabel.grid(row=2,column=1,padx=2,pady=5,sticky=W+E)
email.grid(row=2,column=2,columnspan=3,padx=2,pady=5,sticky=W+E)
previewButton.grid(row=3,column=2,padx=3,pady=5,sticky=W+E)
sendButton.grid(row=3,column=3,padx=3,pady=5,sticky=W+E)
infoLabel.grid(row=4,column=1, columnspan=3, padx=2,pady=5,sticky=W+E)

root.grid_columnconfigure(0,minsize=70)
root.grid_columnconfigure(3,minsize=100)
root.grid_rowconfigure(0,minsize=20)

sendButton.config(command=send)
previewButton.config(command=preview)

root.mainloop()
