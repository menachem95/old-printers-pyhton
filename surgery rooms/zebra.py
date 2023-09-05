from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from threading import Timer
import os


# colors
GREEN = "#09E810"
RED = "#E90A0A"

explorer = "C:/Program Files/Internet Explorer/iexplore.exe"
chrome = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"


def open_web_page(address):
    os.system(f'"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe" {address}')
    print(f"open {address} in chrome browser...")
    print("-----------------------------")


def get_ping(address):
    """
    the func send one ping to the address arg
    :param address: ip address or node name of a printer
    :return: True if the address received the ping else False
    """
    response = os.popen(f"ping -n 1 {address}").read()
    if "Received = 1" in response:
        print(f"\033[1;32mping -n 1 {address}  ----  online!\033[0;0m")
        print("-----------------------------")
        return True
    else:
        print(f"\033[2;31mping -n 1 {address}  ----  offline!\033[0;0m")
        print("-----------------------------")
        return False


def click_btn(btn_address, btn_color):
    if btn_color == GREEN:
        open_web_page(btn_address)
    else:
        messagebox.showerror("error", f"{btn_address} אין רשת ")


def keep_flat(event):
    event.widget.config(relief=FLAT)


printers = {}
print("importing file...")
with open(r"\\ism\nur\printers\surgery rooms\printers.txt", "r", encoding='utf8') as f:
    while True:
        one_line = f.readline().replace('"', "").replace("[", "").replace("]", "").replace("\n", "").split(":")
        if len(one_line) < 2:
            break
        kay = one_line[0]
        value = one_line[1].split(",")
        printers[one_line[0]] = value


class Zebra(Frame):

    def __init__(self, master, room, address, line, pag, c, r, online_printer):
        super().__init__()
        self.master = master
        self.room = room
        self.address = address
        self.line = line
        self.pag = pag
        self.color = GREEN if self.address in online_printer else RED

        self.main_frame = Frame(self.master,
                                bg=self.color,
                                height=1,
                                width=6,
                                )

        self.main_frame.grid(column=c, row=r, padx=20, pady=15, sticky="nsew")

        self.address_button = Button(self.main_frame,
                                     bg=self.color,
                                     text=f"{self.address}\n{self.line}",
                                     font=30,
                                     anchor='n',
                                     relief='flat',
                                     activebackground=self.color,
                                     command=lambda: click_btn(self.address, self.color)
                                     )
        self.address_button.grid(row=1)

        self.room_button = Button(self.main_frame,
                                  bg=self.color,
                                  height=1,
                                  width=6,
                                  anchor='s',
                                  text=f"{self.room}",
                                  font=("Narkisim", 40),
                                  relief='flat',
                                  activebackground=self.color,
                                  command=lambda: click_btn(self.address, self.color)
                                  )
        self.room_button.grid(row=0)


root = Tk()
root.geometry("700x600-200-200")
root.resizable(0, 0)
root.title("זברות חדרי ניתוח")

main_label = Label(root,
                   text="זברות חדרי ניתוח",
                   font=("Tahoma", 48)
                   ).pack()

second_label = Label(root,
                     text="דוידסון -4",
                     font=("Tahoma", 28)
                     ).pack()


total_status = LabelFrame(root,
                          text=f' סה"כ מדפסות - {len(printers)}',
                          font=("Tahoma", 20),
                          labelanchor="n"
                          )
total_status.pack()

main_frame = LabelFrame(root)
main_frame.pack(fill=BOTH, expand="yes", padx=10, pady=10)

my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand="yes")

my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

my_canvas.configure(yscrollcommand=my_scrollbar.set)

my_canvas.bind("<Configure>", lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))


my_frame = Frame(my_canvas)

my_canvas.create_window((0, 0), window=my_frame)

root.bind('<Button-1>', keep_flat)


def main():

    online_printer = [i[0] for i in printers.values() if get_ping(i[0])]

    Label(total_status,
          text="  מדפסות תקינות " + str(len(online_printer)) + "   |   "
               + "מדפסות לא תקינות " + str(len(printers) - len(online_printer)) + "  ",
          font=("Tahoma", 12),
          ).grid(row=1, column=1)

    c_num = 0
    r_num = 0
    if c_num == 3:
        r_num += 1
        c_num = 0

    for printer in printers.items():
        if c_num == 3:
            r_num += 1
            c_num = 0

        Zebra(my_frame, printer[0], printer[1][0], printer[1][1], printer[1][2], c_num, r_num, online_printer)
        c_num += 1


laps = 0


def timer():
    global laps
    print(f"laps number {laps}\n")
    laps += 1
    main()
    Timer(5, timer).start()
    print("...............................................")


timer()
root.mainloop()
