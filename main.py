from tkinter import *
import tkinter
import time
import os

#window properties
window = tkinter.Tk()
window.title('OfTheEssence')
window.configure(background="#60b26c")
window.overrideredirect(True)
window.wm_attributes("-transparentcolor", '#60b26c')



def digitalclock():
    hours = time.strftime("%I")
    mins = time.strftime("%M")
    secs = time.strftime("%S")
    daynight = time.strftime("%p")
    compiledtime = hours + ":" + mins + ":" + secs + ":" + daynight
    timelabel.config(text=compiledtime)
    timelabel.after(1000, digitalclock)

Font = "Helvetica 72 bold"
timelabel = tkinter.Label(window, text="00:00:00", font=Font)

digitalclock()






def searchbg(*args):
    new_window = Toplevel(window)
    new_window.geometry("250x100")
    new_window.title('Theme')

    def helpneeded():
        link = textbox.get()
        print(link)
        f = open("url.txt", "a+")
        f.write(str(link))
        f.close()
        if os.path.exists("bg.jpg"):
            os.remove("bg.jpg")
        else:
            print("The file does not exist")
        new_window.destroy()
        import settheme

    textbox = Entry(new_window,width=30)
    textbox.pack()
    searchbutton = Button(new_window, text="Search Theme", padx=10, pady=5, command= helpneeded)
    searchbutton.pack()

def button_hover(*args):
    Font="Helvetica 84 bold"
    timelabel.pack()


def button_hover_leave(*args):
    Font="Helvetica 72 bold"
    timelabel.pack()




timelabel.bind("<Button-1>", searchbg)
timelabel.pack()

timelabel.bind("<Enter>", button_hover)
timelabel.bind("<Leave>", button_hover_leave)

window.mainloop()



