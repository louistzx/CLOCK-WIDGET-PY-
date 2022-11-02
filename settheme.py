import requests # request img from web
import shutil # save img locally
import ctypes
import os


directory = os.getcwd()

f = open("url.txt", "r")
if f.mode == 'r':
    url: str = f.read()

file_name = "bg.jpg" #prompt user for file_name

res = requests.get(url, stream=True)
open('url.txt', 'w').close()





if res.status_code == 200:
    with open(file_name,'wb') as f:
        shutil.copyfileobj(res.raw, f)
    print('Image sucessfully Downloaded: ',file_name)

    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, directory + '/bg.jpg', 0)
    f = open('url.txt', 'r+')
    f.truncate(0)
    f.close()
    print("txtfile cleared")

else:
    print('Image Couldn\'t be retrieved')



