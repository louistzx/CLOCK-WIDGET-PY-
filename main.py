from tkinter import *
import tkinter
import time
import os
import ctypes
from colorthief import ColorThief
import webcolors
from icrawler.builtin import GoogleImageCrawler
import datetime as dt
import requests
from PIL import ImageTk, Image





directory = os.getcwd()





#window properties
window = tkinter.Tk()
window.title('OfTheEssence')
window.geometry("700x200")
themecolour = 'white'
window.configure(background=themecolour)
window.overrideredirect(True)



def weather():
    CITY = "Singapore"
    APIKEY = open('key.api').read()
    url = "http://api.openweathermap.org/data/2.5/weather?appid=" + APIKEY + "&q=" + CITY
    response = requests.get(url).json()
    print(response)

    kelvin = response['main']['temp']
    temp = kelvin - 273.15
    humidity = response['main']['humidity']
    description = response['weather'][0]['description']
    sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
    sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

    Templabel.config(text=(str(round(temp, 2)) + "°C"))
    description_label.config(text=description)
    humiditylabel.config(text="humidity: " + str(humidity) + "%")
    Templabel.after(3600000, weather)
    description_label.after(3600000, weather)
    humiditylabel.after(3600000, weather)

    def weathericons(): #IDK HOW TO GET IT TO WORK BRUHHHHH
        icon_used = response['weather'][0]['icon']
        iconpath = str(directory) + "\icons\\" + icon_used + ".png"
        print(iconpath)
        image = PhotoImage(file=iconpath)
        Label(window, image=image).pack()





description_label = tkinter.Label(window, text="-", font="Helvetica 10", bg=themecolour)
Templabel = tkinter.Label(window, text="0°C", font="Helvetica 10", bg=themecolour)
humiditylabel = tkinter.Label(window, text="0°C", font="Helvetica 10", bg=themecolour)
Templabel.pack()
description_label.pack()
humiditylabel.pack()
Templabel.place(x=30, y=10)
description_label.place(x=300, y=10)
humiditylabel.place(x=600, y=10)
weather()


def digitalclock():
    hours = time.strftime("%I")
    mins = time.strftime("%M")
    secs = time.strftime("%S")
    daynight = time.strftime("%p")
    compiledtime = hours + ":" + mins + ":" + secs + ":" + daynight
    timelabel.config(text=compiledtime)
    timelabel.after(1000, digitalclock)

Font = "Impact 72"
timelabel = tkinter.Label(window, text="00:00:00", font=Font)
timelabel.config(bg=themecolour)
timelabel.pack()
timelabel.place(x=100, y=50)
digitalclock()






def searchbg(*args):
    new_window = Toplevel(window)
    new_window.geometry("250x100")
    new_window.title('Theme')

    def detectcolour():
        dominant_color = ColorThief('000001.jpg').get_color(quality=1)
        themecolour = webcolors.rgb_to_hex(dominant_color)
        print(str(themecolour))
        timelabel.config(bg=themecolour)
        window.configure(background=themecolour)
        Templabel.config(bg=themecolour)
        description_label.config(bg=themecolour)
        humiditylabel.config(bg=themecolour)


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
    timelabel.config(font=('Impact', 80))
    timelabel.place(x=80, y=40)

def button_hover_leave(*args):
    timelabel.config(font=('Impact', 72))
    timelabel.place(x=100, y=50)



timelabel.bind("<Button-1>", searchbg)
timelabel.bind("<Enter>", button_hover)
timelabel.bind("<Leave>", button_hover_leave)

window.mainloop()