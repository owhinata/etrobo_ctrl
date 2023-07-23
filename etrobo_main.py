import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import time
import sys
import os
import argparse
from PIL import Image, ImageTk

SELECT_CONTROL_LIST = ['Stop','Line Trace']
SELECT_COURSE_LIST = ['course_L.png','course_R.png','sample_course.png']
IMAGE_DIR = os.path.dirname(os.path.abspath(__file__))+'/image/'

class etroboCtrl(tk.Frame):
    def __init__(self, master, hostname):
        super().__init__(master)
        self.master = master
        print(hostname)
        if os.name != 'nt':
            import etrobo_grpc
            self.client = etrobo_grpc.EtRoboClient(hostname)

        # Window create
        self.master.title("Vehicle control app")
        self.topframe = ttk.Frame(self.master)
        self.topframe.grid(row=0, column=0, sticky='nswe')

        # Check the resolution of the Monitor
        self.monitor_w = self.winfo_screenwidth()   # Monitor width
        self.monitor_h = self.winfo_screenheight()  # Monitor height
        print(self.monitor_w, self.monitor_h)

        #
        self.read_parameters()

        #
        self.adjust_width = self.width
        self.adjust_height = self.height

        # Style
        style = ttk.Style()
        if self.is_large_monitor():
            # create style for Buttons in 'Control' group
            style.configure('Control.TButton', font='Helvetica 14 bold')
            # create style for CheckButtons in 'Control' group
            style.configure('Control.TCheckbutton', font='Helvetica 14 bold')
            # change font for labelframe
            style.configure('TLabelframe.Label', font='Helvetica 14')
        else:
            style.configure('Control.TButton')
            style.configure('Control.TCheckbutton')

        # ---------------------------------------------------------
        # Menubar
        # ---------------------------------------------------------
        self.create_menubar()

        # ---------------------------------------------------------
        # Widget
        # ---------------------------------------------------------
        self.create_widgets()

        self.canvas1_id = None

    def is_large_monitor(self):
        return self.monitor_h > 480

#
# Read Parameters from settings file(.json)
#
    def read_parameters(self):
        self.width = 480
        self.height = 640
        self.speed = 0
        self.threshold = 0
        self.steer = 0
        self.listarray = SELECT_CONTROL_LIST

#
# Creating menubar
#
    def create_menubar(self):
        # menubar
        menubar = tk.Menu(self.master)

        # File
        menu_file = tk.Menu(menubar)
        menu_file.add_command(label='Open',
                              command=self.menu_file_open_click,
                              accelerator='Ctrl+O')
        menu_file.add_command(label='Save As',
                              command=self.menu_file_saveas_click,
                              accelerator='Ctrl+S')
        menu_file.add_separator()  # border line
        menu_file.add_command(label='Exit', command=self.menu_file_exit_click)
        # shortcut key
        menu_file.bind_all('<Control-o>', self.menu_file_open_click)
        menu_file.bind_all('<Control-s>', self.menu_file_saveas_click)

        # Control
        menu_control = tk.Menu(menubar)
        for i, label in enumerate(SELECT_CONTROL_LIST):
            menu_control.add_command(label=label,
                                     command=self.control_menu_click(i))

        # Course
        menu_course = tk.Menu(menubar)
        for i, label in enumerate(SELECT_COURSE_LIST):
            menu_course.add_command(label=label,
                                     command=self.course_menu_click(i))

        # menu
        menubar.add_cascade(label='Settings File', menu=menu_file)
        menubar.add_cascade(label='Control', menu=menu_control)
        menubar.add_cascade(label='Course', menu=menu_course)

        self.master.config(menu=menubar)

#
# File: Open
#
    def menu_file_open_click(self, event=None):
        del event
        print('Select Open')
        f_type = [('json', '*.json')]
        filename = tkinter.filedialog.askopenfilename(
            title='Open',
            filetypes=f_type,
            initialdir='./'  # own directory
            )
        print(filename)
        if filename:
            self.param_file = filename
            self.reset_parameters()

#
# File: Save As
#
    def menu_file_saveas_click(self, event=None):
        del event
        print('Select Save As')
        f_type = [('json', '*.json')]
        filename = tkinter.filedialog.asksaveasfilename(
            title='Save As',
            filetypes=f_type,
            initialdir='./'  # own directory
            )
        print(filename)
        if filename:
            self.write_parameters(filename)

#
# File: Exit
#
    def menu_file_exit_click(self, event=None):
        del event
        self.master.destroy()

#
# Creating a widget
#
    def create_widgets(self):

        # Frame for etrobo course
        self.etroboCourse_frame = ttk.LabelFrame(self.topframe)
        self.etroboCourse_frame.grid(row=0, column=2, rowspan=2, sticky='nw')

        # Canvas1 for etrobo course
        self.canvas1 = tk.Canvas(self.etroboCourse_frame, bg='lightgreen',
                                 highlightthickness=0,
                                 width=self.adjust_width,
                                 height=self.adjust_height)
        self.canvas1.grid(row=0, column=0)

        # Settings Bar / Settings Notebook
        settings_notebook = None
        if not self.is_large_monitor():
            settings_notebook = ttk.Notebook(self.topframe)
            settings_notebook.grid(row=2, column=0, columnspan=2, sticky='nwe')
        else:
            settings_frame = ttk.Frame(self.topframe)
            settings_frame.grid(row=0, column=0, columnspan=2, sticky='nwe')

        frames = {}
        for i, label in enumerate(['Settings',
                                   'Edge']):
            if settings_notebook:
                frames[label] = ttk.Frame(settings_notebook)
                settings_notebook.add(frames[label], text=label)
            else:
                frames[label] = ttk.LabelFrame(settings_frame, text=label,
                                               padding=4)
                frames[label].grid(row=0, column=i, sticky='nsw', padx=2)

        frame = frames['Settings']

        # Speed
        self.speed_scale_var = tk.IntVar(value=self.speed)
        tk.Scale(frame, label='Speed',
                 variable=self.speed_scale_var,
                 command=self.speed_slider_scroll,
                 orient=tk.HORIZONTAL,
                 length=200, width=20, sliderlength=20,
                 from_=-100, to=100, tickinterval=100).\
            grid(row=0, column=0, sticky='e')

        # Threshold
        self.threshold_scale_var = tk.IntVar(value=self.threshold)
        tk.Scale(frame, label='Threshold',
                 variable=self.threshold_scale_var,
                 command=self.threshold_slider_scroll,
                 orient=tk.HORIZONTAL,
                 length=200, width=20, sliderlength=20,
                 from_=0, to=255, tickinterval=255).\
            grid(row=0, column=1, sticky='e')

        # Steer
        self.steer_scale_var = tk.IntVar(value=self.steer)
        tk.Scale(frame, label='Steer',
                 variable=self.steer_scale_var,
                 command=self.steer_slider_scroll,
                 orient=tk.HORIZONTAL,
                 length=200, width=20, sliderlength=20,
                 from_=-100, to=100, tickinterval=100).\
            grid(row=0, column=2, sticky='e')

        frame = frames['Edge']
        # Radiobutton for Edge
        self.select_edge = tk.IntVar()
        ttk.Radiobutton(frame, text='Left',
                        variable=self.select_edge,
                        command=self.select_edge_click, value=0).\
            grid(row=0, column=0, stick='nw')
        ttk.Radiobutton(frame, text='Right',
                        variable=self.select_edge,
                        command=self.select_edge_click, value=1).\
            grid(row=1, column=0, stick='nw')

        # Frame for Control list box
        controls_frame = ttk.Frame(self.topframe)
        controls_frame.grid(row=1, column=0, columnspan=2, sticky='nsw')
        controls = ttk.LabelFrame(controls_frame, text='Control',
                                  padding=4)
        controls.grid(row=1, column=0, columnspan=2, sticky='w')
        self.select_command = tk.StringVar(value=self.listarray)
        self.lbox = tk.Listbox(controls, listvariable=self.select_command, selectmode='single', width=12, height=0)
        self.lbox.grid(row=0, column=0, columnspan=2, sticky='w')
        # Button
        button1 = ttk.Button(controls_frame, text='Send', command=self.select_control_box_click)
        button1.grid(row=2, column=0, columnspan=2)

        #
        for child in self.topframe.winfo_children():
            child.grid_configure(padx=4, pady=4)
        self.topframe.grid_rowconfigure(1, weight=1)
        self.topframe.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

# ---------------------------------------------------------
# create course image
# ---------------------------------------------------------
    def create_course_image(self, index):
        # PillowのPIL.Imageで画像ファイルを開く（対応しているファイルフォーマットはPGM、PPM、GIF、PNG）
        pil_image = Image.open(IMAGE_DIR+SELECT_COURSE_LIST[index])

        # PIL.ImageからPhotoImageへ変換する
        self.photo_image = ImageTk.PhotoImage(image=pil_image)
        
        # キャンバスのサイズを取得
        canvas_width = self.adjust_width
        canvas_height = self.adjust_height
        #print(canvas_width, canvas_height)

        # 画像の描画
        if not self.canvas1_id is None:
            self.canvas1.delete(self.canvas1_id)
        self.canvas1_id = self.canvas1.create_image(
                canvas_width / 2,       # 画像表示位置(Canvasの中心)
                canvas_height / 2,                   
                image=self.photo_image  # 表示画像データ
                )

        # print('id:{}'.format(self.canvas1.find_all()))
#
# Control menu click 
#
    def control_menu_click(self, index):
        def inner():
            if os.name != 'nt':
                self.client.set(mode=index)
            print('mode:{}'.format(index))
        return inner

#
# Course menu click 
#
    def course_menu_click(self, index):
        def inner():
            # ---------------------------------------------------------
            # create course image
            # ---------------------------------------------------------
            self.create_course_image(index)
        return inner

#
# Speed scale slider
#
    def speed_slider_scroll(self, event=None):
        del event
        speed = self.speed_scale_var.get()
        if os.name != 'nt':
            self.client.set(speed=speed)
        print('speed:{}'.format(speed))

#
# Threshold scale slider
#
    def threshold_slider_scroll(self, event=None):
        del event
        threshold = self.threshold_scale_var.get()
        if os.name != 'nt':
            self.client.set(threshold=threshold)
        print('threshold:{}'.format(threshold))

#
# Steer scale slider
#
    def steer_slider_scroll(self, event=None):
        del event
        steer = self.steer_scale_var.get()
        if os.name != 'nt':
            self.client.set(steer=steer)
        print('steer:{}'.format(steer))

#
# Edge mode select
#
    def select_edge_click(self):
        edge = self.select_edge.get()
        if os.name != 'nt':
            self.client.set(edge=edge)
        print('edge:{}'.format(edge))

#
# Control mode select
#
    def select_control_box_click(self):
        for i in self.lbox.curselection():
            if os.name != 'nt':
                self.client.set(mode=i)
            print(self.lbox.get(i))
            print('mode:{}'.format(i))

#
# main
#
def main(hostname):
    root = tk.Tk()
    root.option_add('*tearOff', False)
    if (hostname is None):
        hostname = 'localhost'
    # Inherit
    app = etroboCtrl(master=root, hostname=hostname)

    app = root.mainloop()

if __name__ == '__main__':
    # parserとしてArgumentParserオブジェクトを作成する
    parser = argparse.ArgumentParser(
        prog='etrobo_control',
        usage='python3 etrobo.py',
        description='description: etrobo control application',
        epilog='end',  # 引数のヘルプの後で表示
        add_help=True  # -h/-help オプションの追加
    )

    # add_argumentメソッドを使って、コマンドラインから引数を受け取る処
    # 理を作成する
    parser.add_argument('-H', '--hostname',
                        help='hostname')

    # 引数を解析する
    args = parser.parse_args()
    print(args.hostname)

    main(args.hostname)
