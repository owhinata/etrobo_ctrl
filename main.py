import sys
from tkinter import *
from tkinter import ttk
import etrobo_grpc

def show_selection():
    pass

def send_selection():
    for i in lb.curselection():
        client.set(mode=i)

def change_speed(speed):
    client.set(speed=speed)

if __name__ == '__main__':
    hostname='localhost'

    if len(sys.argv) == 2:
        hostname=sys.argv[1]

    client = etrobo_grpc.EtRoboClient(hostname)

    root = Tk()
    root.geometry('640x480')
    root.title('走行体制御')

    frame = ttk.Frame(root, padding=10)
    frame.grid()

    currencies = ['静止', 'ライントレース']
    v = StringVar(value=currencies)
    lb = Listbox(
            frame, listvariable=v,
            selectmode='single', width=12, height=0)
    lb.bind(
            '<<ListboxSelect>>',
            lambda e: show_selection())
    lb.grid(row=0, column=0)

    button1 = ttk.Button(
            frame, text='Send', width=8,
            command=lambda: send_selection())
    button1.grid(row=1, column=0)

    speed = IntVar()
    sc = ttk.Scale(
            frame, variable=speed,
            orient=HORIZONTAL,
            from_=-100, to=100,
            command=lambda e: change_speed(speed.get()))
    sc.grid(row=0, column=1, sticky=(N, E, S, W))

    root.mainloop()
