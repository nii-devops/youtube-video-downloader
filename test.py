from datetime import datetime


today = datetime.today().replace(microsecond=0)

print(today)

from tkinter.filedialog import askdirectory
dl_path = askdirectory()


#print(dl_path)

def print_directory():
    DL_PATH = askdirectory()
    return DL_PATH

new_folder = print_directory()

print(new_folder)



