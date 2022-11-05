from tkinter import *
import tkinter
import time
import os
import ctypes
from colorthief import ColorThief
import webcolors
from icrawler.builtin import GoogleImageCrawler



directory = os.getcwd()

#window properties
window = tkinter.Tk()
window.title('OfTheEssence')
window.geometry("700x150")
themecolour = 'white'
window.configure(background=themecolour)
window.overrideredirect(True)




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
timelabel.config(bg=themecolour)
timelabel.pack()
digitalclock()






def searchbg(*args):
    new_window = Toplevel(window)
    new_window.geometry("250x100")
    new_window.title('Theme')

    def detectcolour():
        dominant_color = ColorThief('000001.jpg').get_color(quality=1)
        themecolour = webcolors.rgb_to_hex(dominant_color)
        timelabel.config(bg=themecolour)
        window.configure(background=themecolour)



    def setbg():
        url = textbox.get()

        if os.path.exists("000001.jpg"):
            os.remove("000001.jpg")
        else:
            print("The file does not exist")

        google_Crawler = GoogleImageCrawler(storage={'root_dir': directory})
        google_Crawler.crawl(keyword=url, max_num=1)

        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, directory + '/000001.jpg', 0)

        detectcolour()
        new_window.destroy()



    textbox = Entry(new_window,width=30)
    textbox.pack()
    searchbutton = Button(new_window, text="Search Theme", padx=10, pady=5, command=setbg)
    searchbutton.pack()

def button_hover(*args):
    timelabel.config(font=('Helvetica bold', 80))

def button_hover_leave(*args):
    timelabel.config(font=('Helvetica bold', 72))



timelabel.bind("<Button-1>", searchbg)
timelabel.bind("<Enter>", button_hover)
timelabel.bind("<Leave>", button_hover_leave)

window.mainloop()