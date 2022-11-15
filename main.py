import threading
import tkinter
from tkinter import *
from tkinter import messagebox
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





#Window properties
window = tkinter.Tk()
window.title('OfTheEssence')
window.geometry("550x250")
themecolour = 'white'
window.configure(background=themecolour)
window.overrideredirect(True)


#Getting weather forecast from OPENWEATHERMAP api
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
    print(sunset_time, sunrise_time)
    print(dt.datetime.now())
    if sunset_time == dt.datetime.now:
        print("Its sunset")

    Templabel.config(text=(str(round(temp, 2)) + "°C"))
    description_label.config(text=description)
    humiditylabel.config(text="humidity: " + str(humidity) + "%")
    Templabel.after(3600000, weather)
    description_label.after(3600000, weather)
    humiditylabel.after(3600000, weather)

    def weathericons():
        icon_used = response['weather'][0]['icon']
        iconpath = str(directory) + "\icons\\" + icon_used + ".png"
        print(iconpath)
        Image1 = Image.open(iconpath)
        Image2 = Image1.resize((70,70))
        weatherimage = ImageTk.PhotoImage(Image2)
        iconlabel.configure(bg=themecolour, image=weatherimage)
        iconlabel.image = weatherimage
        iconlabel.pack()
        iconlabel.place(relx=0.5, rely=0.2, anchor='center')
    weathericons()



#Creating labels for weather forecast
iconlabel = tkinter.Label(window, bg=themecolour)
description_label = tkinter.Label(window, text="-", font="Helvetica 10 bold", bg=themecolour)
Templabel = tkinter.Label(window, text="0°C", font="Helvetica 10 bold", bg=themecolour)
humiditylabel = tkinter.Label(window, text="0°C", font="Helvetica 10 bold", bg=themecolour)
Templabel.pack()
description_label.pack()
humiditylabel.pack()
Templabel.place(relx=0, rely=0, anchor='nw')
description_label.place(relx=0.5, rely=0.05, anchor='center')
humiditylabel.place(relx=1.0, rely=0, anchor='ne')
weather()

#For clock
def digitalclock():
    hrs = time.strftime("%I")
    mins = time.strftime("%M")
    secs = time.strftime("%S")
    daynight = time.strftime("%p")
    global compiledtime
    compiledtime = hrs + ":" + mins + ":" + secs + ":" + daynight
    timelabel.config(text=compiledtime)
    timelabel.after(1000, digitalclock)

Font = "Impact 72"
timelabel = tkinter.Label(window, text="00:00:00", font=Font)
timelabel.config(bg=themecolour)
timelabel.pack()
timelabel.place(relx=0.5, rely=0.6, anchor='center')
digitalclock()





#Downloading and detecting colour of background based off keyword search
def searchbg(*args):
    new_window = Toplevel(window)
    new_window.geometry("250x100")
    new_window.title('Theme')


    def detectcolour():
        if os.path.exists("000001.jpg"):
            dominant_color = ColorThief('000001.jpg').get_color(quality=1)
        else:
            dominant_color = ColorThief('000001.png').get_color(quality=1)
        global themecolour
        themecolour = webcolors.rgb_to_hex(dominant_color)
        print(str(themecolour))
        timelabel.config(bg=themecolour)
        window.configure(background=themecolour)
        Templabel.config(bg=themecolour)
        description_label.config(bg=themecolour)
        humiditylabel.config(bg=themecolour)
        iconlabel.config(bg=themecolour)
        Timerbutton.config(bg=themecolour)
        Alarmbutton.config(bg=themecolour)



    def setbg():
        url = (textbox.get() + " HD background")

        if os.path.exists("000001.jpg"):
            os.remove("000001.jpg")
            print("jpg removed")
        else:
            print("The file does not exist")
        if os.path.exists("000001.png"):
            os.remove("000001.png")
            print("png removed")
        else:
            print("The file does not exist")

        google_Crawler = GoogleImageCrawler(storage={'root_dir': directory})
        google_Crawler.crawl(keyword=url, max_num=1)

        SPI_SETDESKWALLPAPER = 20

        if os.path.exists("000001.jpg"):
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, directory + '/000001.jpg', 0)
        else:
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, directory + '/000001.png', 0)

        detectcolour()



    textbox = Entry(new_window,width=30)
    textbox.pack()
    searchbutton = Button(new_window, text="Search Theme", padx=10, pady=5, command=setbg)
    searchbutton.pack()


#To animate clock on hover
def button_hover(*args):
    timelabel.config(font=('Impact', 80))

def button_hover_leave(*args):
    timelabel.config(font=('Impact', 72))




timelabel.bind("<Button-1>", searchbg)
timelabel.bind("<Enter>", button_hover)
timelabel.bind("<Leave>", button_hover_leave)

#Load back icon
OpenImageBack = Image.open(directory + "/icons/back.png")
ResizedImageBack = OpenImageBack.resize((30, 30))
Backimage = ImageTk.PhotoImage(ResizedImageBack)




#For the timer
OpenImageTimer = Image.open(directory +"/icons/stopwatch.png")
ResizedImageTimer = OpenImageTimer.resize((30, 30))
Timerimage = ImageTk.PhotoImage(ResizedImageTimer)
Timerbutton = tkinter.Label(bg=themecolour, image=Timerimage)
Timerbutton.image = Timerimage
Timerbutton.pack()
Timerbutton.place(relx=0, rely=1, anchor='sw')

seconds = 00
minutes = 00
hours = 00
timerrunning = True


def Timerwindow(*args):
    window.withdraw()
    Timerwindow = tkinter.Toplevel()
    Timerwindow.geometry("550x250")
    Timerwindow.configure(background=themecolour)
    Timerwindow.overrideredirect(True)
    Timerlabel = tkinter.Label(Timerwindow, text="00:00:00", font=Font, bg=themecolour)
    Timerlabel.pack()
    Timerlabel.place(relx=0.5, rely=0.5, anchor='center')

    def timer():
        global seconds, minutes, hours
        time.sleep(1)
        seconds += 1
        if seconds == 60:
            seconds = 00
            minutes += 1
        if minutes == 60:
            minutes = 00
            hours += 1
        if hours == 24:
            seconds = 00
            minutes = 00
            hours = 00
        if hours > 9:
            timer_hour_string = f'{hours}'
        else:
            timer_hour_string = f'0{hours}'
        if minutes > 9:
            timer_minute_string = f'{minutes}'
        else:
            timer_minute_string = f'0{minutes}'

        if seconds > 9:
            timer_second_string = f'{seconds}'
        else:
            timer_second_string = f'0{seconds}'

        Timerlabel.config(text=timer_hour_string + ":" + timer_minute_string + ":" + timer_second_string)
        global update
        update = Timerlabel.after(1000, start_timer)

    def reset_timer():
        global timerrunning, hours, minutes, seconds
        timerrunning = False
        hours, minutes, seconds = 0, 0, 0
        Timerlabel.config(text="00:00:00")

    def start_timer():
        global timerrunning
        timerrunning = True
        if timerrunning:
            startbutton.config(text="Pause", command=pause_timer)
            timer()

    def pause_timer():
        global timerrunning
        if timerrunning:
            Timerlabel.after_cancel(update)
            startbutton.config(text="Start", command=start_timer)
            timerrunning = False



    startbutton = Button(Timerwindow, text="Start", padx=10, pady=5, command=start_timer)
    startbutton.pack()
    startbutton.place(relx=0, rely=1, anchor='sw')
    stopbutton = Button(Timerwindow, text="Reset", padx=10, pady=5, command=reset_timer)
    stopbutton.pack()
    stopbutton.place(relx=1, rely=1, anchor='se')



    Backbutton = tkinter.Label(Timerwindow, bg=themecolour, image=Backimage)
    Backbutton.image = Backimage
    Backbutton.pack()
    Backbutton.place(relx=0, rely=0, anchor='nw')

    def back_from_timer(*args):
        Timerwindow.withdraw()
        window.deiconify()




    Backbutton.bind("<Button-1>", back_from_timer)



Timerbutton.bind("<Button-1>", Timerwindow)


#For alarm

OpenImageAlarm = Image.open(directory +"/icons/alarm.png")
ResizedImageAlarm = OpenImageAlarm.resize((28, 28))
Alarmimage = ImageTk.PhotoImage(ResizedImageAlarm)
Alarmbutton = tkinter.Label(bg=themecolour, image=Alarmimage)
Alarmbutton.image = Alarmimage
Alarmbutton.pack()
Alarmbutton.place(relx=0.08, rely=1, anchor='sw')
alarmhour = 0
alarmminute = 0
alarmsecond = 0
alarmhourstring = f'{alarmhour}'
alarmminutestring = f'{alarmminute}'
alarmsecondstring = f'{alarmsecond}'
alarmAMPM = 1
alarmdaynight = "AM"


def Alarmwindow(*args):
    window.withdraw()
    Alarmwindow = tkinter.Toplevel()
    Alarmwindow.geometry("550x250")
    Alarmwindow.configure(background=themecolour)
    Alarmwindow.overrideredirect(True)
    Hourlabel = tkinter.Label(Alarmwindow, text="00", font=Font, bg=themecolour)
    Hourlabel.pack()
    Hourlabel.place(relx=0.1, rely=0.5, anchor='center')
    Minlabel = tkinter.Label(Alarmwindow, text=":00", font=Font, bg=themecolour)
    Minlabel.pack()
    Minlabel.place(relx=0.35, rely=0.5, anchor='center')
    Seclabel = tkinter.Label(Alarmwindow, text=":00", font=Font, bg=themecolour)
    Seclabel.pack()
    Seclabel.place(relx=0.6, rely=0.5, anchor='center')
    AMPMlabel = tkinter.Label(Alarmwindow, text="AM", font=Font, bg=themecolour)
    AMPMlabel.pack()
    AMPMlabel.place(relx=0.89, rely=0.5, anchor='center')




    def upchangealarm(*args):
        global alarmhour, alarmminute, alarmsecond, Alarmselect

        if Alarmselect == 1:
            alarmhour += 1
            if alarmhour < 10:
                Hourlabel.config(text="0"+str(alarmhour))
            else:
                Hourlabel.config(text=alarmhour)
            if alarmhour == 24:
                alarmhour = 0
                Hourlabel.config(text="00")



        if Alarmselect == 2:
            alarmminute += 1
            if alarmminute < 10:
                Minlabel.config(text=":0"+str(alarmminute))
            else:
                Minlabel.config(text=":"+str(alarmminute))
            if alarmminute == 60:
                alarmminute = 0
                alarmhour += 1
                Minlabel.config(text=":00")
                if alarmhour < 10:
                    Hourlabel.config(text="0" + str(alarmhour))
                else:
                    Hourlabel.config(text=alarmhour)



        if Alarmselect == 3:
            alarmsecond += 1
            if alarmsecond < 10:
                Seclabel.config(text=":0"+str(alarmsecond))
            else:
                Seclabel.config(text=":"+str(alarmsecond))
            if alarmsecond == 60:
                alarmsecond = 0
                alarmminute += 1
                Seclabel.config(text=":00")
                if alarmminute < 10:
                    Minlabel.config(text=":0" + str(alarmminute))
                else:
                    Minlabel.config(text=alarmminute)


    def downchangealarm(*args):
        global alarmhour, alarmminute, alarmsecond, Alarmselect
        if Alarmselect == 1:
            alarmhour -= 1
            if alarmhour < 10:
                Hourlabel.config(text="0"+str(alarmhour))
            else:
                Hourlabel.config(text=alarmhour)
            if alarmhour < 1:
                alarmhour = 0
                Hourlabel.config(text="00")

        if Alarmselect == 2:
            alarmminute -= 1
            if alarmminute < 10:
                Minlabel.config(text=":0"+str(alarmminute))
            else:
                Minlabel.config(text=":"+str(alarmminute))
            if alarmminute < 1:
                alarmminute = 59
                Minlabel.config(text=":59 ")

        if Alarmselect == 3:
            alarmsecond -= 1
            if alarmsecond < 10:
                Seclabel.config(text=":0"+str(alarmsecond))
            else:
                Seclabel.config(text=":"+str(alarmsecond))
            if alarmsecond < 1:
                alarmsecond = 59
                Seclabel.config(text=":59")

    def th():
        t1 = threading.Thread(target=alarmloop, args=())
        t1.start()

    def setalarm(*args):
        if alarmhour < 9:
            alarmhourstring = "0"+f'{alarmhour}'
        else:
            alarmhourstring = alarmhour
        if alarmminute < 9:
            alarmminutestring = ":0"+f'{alarmminute}'
        else:
            alarmminutestring = ":"+f'{alarmminute}'
        if alarmsecond < 9:
            alarmsecondstring = ":0"+f'{alarmsecond}'
        else:
            alarmsecondstring = ":"+f'{alarmsecond}'
        global alarmset
        alarmset = f'{alarmhourstring}' + f'{alarmminutestring}' + f'{alarmsecondstring}' + ":" +str(alarmdaynight)
        if alarmset == "00:00:00:AM" or alarmset == "00:00:00:PM" or alarmhourstring == "00":
            tkinter.messagebox.showerror(title="Error", message="Please select a time")
        else:
            tkinter.messagebox.showinfo(title="Alarm", message="Alarm set for " + alarmset)
            th()


    def alarmloop():
        global alarmset, compiledtime
        print(alarmset, compiledtime)
        if alarmset == compiledtime:
            tkinter.messagebox.showinfo(title="Alarm", message="It is currently "+alarmset)
        th()

    upbutton = Button(Alarmwindow, text="↑", padx=20, pady=10, command=upchangealarm)
    downbutton = Button(Alarmwindow, text="↓", padx=20, pady=10, command=downchangealarm)
    setalarmbutton = Button(Alarmwindow, text="Set Alarm", padx=10, pady=10, command=setalarm)
    setalarmbutton.pack()
    setalarmbutton.place(relx=1, rely=1, anchor='se')
    Alarmselect = 0




    def hourchangealarm(*args):
        global Alarmselect
        Hourlabel.config(fg='black')
        Minlabel.config(fg='grey')
        Seclabel.config(fg='grey')
        Alarmselect = 1
        upbutton.pack()
        upbutton.place(relx=0.5, rely=0.2, anchor='center')
        downbutton.pack()
        downbutton.place(relx=0.5, rely=0.8, anchor='center')



    def minchangealarm(*args):
        global Alarmselect
        Minlabel.config(fg='black')
        Hourlabel.config(fg='grey')
        Seclabel.config(fg='grey')
        Alarmselect = 2
        upbutton.pack()
        upbutton.place(relx=0.5, rely=0.2, anchor='center')
        downbutton.pack()
        downbutton.place(relx=0.5, rely=0.8, anchor='center')

    def secchangealarm(*args):
        global Alarmselect
        Minlabel.config(fg='grey')
        Hourlabel.config(fg='grey')
        Seclabel.config(fg='black')
        Alarmselect = 3
        upbutton.pack()
        upbutton.place(relx=0.5, rely=0.2, anchor='center')
        downbutton.pack()
        downbutton.place(relx=0.5, rely=0.8, anchor='center')

    def AMchangealarm(*args):
        global alarmAMPM, alarmdaynight
        alarmAMPM += 1
        if (alarmAMPM % 2) == 0:
            AMPMlabel.config(text="PM")
            alarmdaynight = "PM"
        else:
            AMPMlabel.config(text="AM")
            alarmdaynight = "AM"









    Hourlabel.bind("<Button-1>", hourchangealarm)
    Minlabel.bind("<Button-1>", minchangealarm)
    Seclabel.bind("<Button-1>", secchangealarm)
    AMPMlabel.bind("<Button-1>", AMchangealarm)
    Backbutton2 = tkinter.Label(Alarmwindow, bg=themecolour, image=Backimage)
    Backbutton2.image = Backimage
    Backbutton2.pack()
    Backbutton2.place(relx=0, rely=0, anchor='nw')

    def back_from_timer(*args):
        Alarmwindow.withdraw()
        window.deiconify()

    Backbutton2.bind("<Button-1>", back_from_timer)


Alarmbutton.bind("<Button-1>", Alarmwindow)

#Animate alarm icon
def alarmbutton_hover(*args):
    ResizedImageAlarm2 = OpenImageAlarm.resize((35, 35))
    Alarmimage2 = ImageTk.PhotoImage(ResizedImageAlarm2)
    Alarmbutton.config(bg=themecolour, image=Alarmimage2)
    Alarmbutton.image = Alarmimage2

def alarmbutton_hover_leave(*args):
    Alarmbutton.config(bg=themecolour, image=Alarmimage)
    Alarmbutton.image = Alarmimage


Alarmbutton.bind("<Enter>", alarmbutton_hover)
Alarmbutton.bind("<Leave>", alarmbutton_hover_leave)




#Animate timer icon
def timerbutton_hover(*args):
    ResizedImageTimer2 = OpenImageTimer.resize((40, 40))
    Timerimage2 = ImageTk.PhotoImage(ResizedImageTimer2)
    Timerbutton.config(bg=themecolour, image=Timerimage2)
    Timerbutton.image = Timerimage2

def timerbutton_hover_leave(*args):
    Timerbutton.config(bg=themecolour, image=Timerimage)
    Timerbutton.image = Timerimage


Timerbutton.bind("<Enter>", timerbutton_hover)
Timerbutton.bind("<Leave>", timerbutton_hover_leave)




window.mainloop()