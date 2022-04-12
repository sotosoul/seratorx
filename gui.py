from tkinter import *
import main
import seratorx
from time import sleep

window = Tk()

window.title('Seratorx')
window.geometry('640x400')

lbl = Label(window, text='Serato library tools', font=('Times New Roman', 18))
lbl.grid(column=0, row=0)


def archive_lib():
    """
    Archives Serato library.
    :return: True (if successful) or False
    """
    archive_status = seratorx.archive_srt_lib()  # True: OK. False: Error, not archived
    lbl_bup_lib.configure(text=f'Most recent backup: {archive_status[1]}')


btn = Button(window, text='Archive', command=archive_lib)
btn.grid(column=0, row=25)
lbl_bup_lib = Label(window, text='Most recent backup: ', font=('Times New Roman', 18))
lbl_bup_lib.grid(column=0, row=300)

window.mainloop()
