import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import tkinter.filedialog
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from algorithm import single_stop

#grid (-column, -columnspan, -in, -ipadx, -ipady, -padx, -pady, -row, -rowspan, or -sticky)
#pack (-after, -anchor, -before, -expand, -fill, -in, -ipadx, -ipady, -padx, -pady, or -side)

class App(ttk.Frame):
    def __init__(self,master=None):
        super().__init__(master)

        self.dataset_filename = None
        self.label_filename = None

        self.master = master
        self.master.title("异构数据融合")
        self.master.geometry("1000x650+50+20")
        self.pack(fill=tk.BOTH,expand=1)
        
        
        #添加菜单
        menubar = tk.Menu(self.master)
        self.master.config(menu = menubar)

        menu_button_main = tk.Menu(menubar)
        menu_button_main.add_command(label="Exit",command=self.__exit_app)
        menu_button_help = tk.Menu(menubar)
        menu_button_help.add_command(label="Website")
        menubar.add_cascade(label="Main",menu=menu_button_main)
        menubar.add_cascade(label="Help",menu=menu_button_help)


        #分块
        self.left_panel = ttk.Frame(self)
        self.left_panel.grid(row=0,column=0)
        self.right_panel = ttk.Frame(self)
        self.right_panel.grid(row=0,column=1,columnspan=3)

        self.initial_app()


    def initial_app(self): 

#---------布局: 分为4个大板块（左三右一） ----------        
        style = ttk.Style()
        style.configure("UP.TButton",height=5, width=13)
        style.configure("OU.TLabel",font=('Helvetica', 20))
        style.configure("SE.TLabel",font=('Helvetica', 15))
        style.configure("SE.TEntry",width=10)
        
        self.choose_panel = ttk.Frame(self.left_panel,borderwidt=30)
        self.choose_panel.pack(fill=tk.BOTH,expand=1,side=tk.TOP)
        upload_panel = ttk.Frame(self.left_panel,borderwidt=30)
        upload_panel.pack(fill=tk.BOTH,expand=1)
        control_panel = ttk.Frame(self.left_panel,borderwidt=30)
        control_panel.pack(fill=tk.BOTH,expand=1,side=tk.BOTTOM)
        
        
#--------------- 左1------------------
        ttk.Label(self.choose_panel,text="Select your algorithm",style="SE.TLabel").grid(row=0,column=0,padx=10,sticky=tk.W)

        var = tk.StringVar(self.choose_panel)
        option_menu = ttk.OptionMenu(self.choose_panel, var, "RIFS","RIFS","BEST K FIRST","COMPLETED",command = lambda x: self.__generate_para(var))
        option_menu.grid(row=0,column = 1,columnspan = 3,sticky=tk.W)
        

#--------------- 左2------------------
        dataset_panel = tk.Canvas(upload_panel)
        dataset_panel.grid(columnspan = 2)
        ttk.Button(upload_panel,text="Upload dataset file",style="UP.TButton",command = self.load_dataset).grid(row=3,column=0,sticky=tk.W)
        ttk.Button(upload_panel,text="Upload label file",style="UP.TButton",command = self.load_label).grid(row=3,column=1,sticky=tk.W)
        
#--------------- 左3------------------

        ttk.Button(control_panel,text="Start",command = self.start_algorithm).grid(row=0,column=0,pady=30,padx=35,sticky=tk.E)
        ttk.Button(control_panel,text="Stop",command = self.__exit_app).grid(row=0,column=1,pady=30,sticky=tk.W)


#--------------- 右---------------
        ttk.Label(self.right_panel,text="OUTPUT",style="OU.TLabel").grid(row=0,rowspan=3,pady=20,padx=20)    
        output_panel = tk.Canvas(self.right_panel, width=550, height=550)
        output_panel.grid(row=3,padx=20)
    

    def __exit_app(self):
        exit()

    def __generate_para(self,variable):
        if variable.get() == "RIFS":
            ttk.Label(self.choose_panel,text="Input percent").grid(row=1,column=0,padx=10,sticky=tk.W)
            ttk.Entry(self.choose_panel,style="SE.TEntry").grid(row=1,column=1)
            ttk.Label(self.choose_panel,text="Input Stop").grid(row=2,column=0,padx=10,sticky=tk.W)
            ttk.Entry(self.choose_panel,style="SE.TEntry").grid(row=2,column=1)



    def load_dataset(self):
        try:
            file_name = askopenfilename(filetypes=(("TXT Files", "*.txt"),("CSV Files", "*.csv")))
            self.dataset_filename = file_name
        except:
            messagebox.showerror("ERROR!","Load file unsuccessful!")

    def load_label(self):
        try:
            file_name = askopenfilename(filetypes=(("TXT Files", "*.txt"),("CSV Files", "*.csv")))
            self.dataset_filename = file_name
        except:
            messagebox.showerror("ERROR!","Load file unsuccessful!")        

         
    def start_algorithm(self):
        if self.dataset_filename is not None and self.label_filename is not None:
            print("starting the calculate {}".format(self.dataset_filename.split(".")[0]))
            single_stop(self.dataset_filename,self.label_filename,1)
        else:
            messagebox.showerror("ERROR!","You have not load the dataset!")
                


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.master.mainloop()
