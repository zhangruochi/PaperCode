import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import tkinter.filedialog
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from algorithm import single_stop

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

#---------布局: 分为五个大板块（左三右二） ----------        
        style = ttk.Style()
        style.configure("UP.TButton", height=5,width=15)
        
        choose_panel = ttk.Frame(self.left_panel,borderwidt=30)
        choose_panel.grid(row=0)
        upload_panel = ttk.Frame(self.left_panel,borderwidt=30)
        upload_panel.grid(row=1)
        control_panel = ttk.Frame(self.left_panel,borderwidt=30)
        control_panel.grid(row=2)

  
        visual_panel = ttk.Frame(self.right_panel,borderwidt=30)
        visual_panel.grid(row=0,rowspan=3)
        
        
#--------------- 左1------------------
        ttk.Label(choose_panel,text="select your mode").grid(row=0,columnspan=2,sticky=tk.W)

        var_gene = tk.IntVar()
        var_image = tk.IntVar()
        var_eec = tk.IntVar()
        
        gene_button = ttk.Checkbutton(choose_panel,text="gene",variable = var_gene)
        image_button = ttk.Checkbutton(choose_panel,text="image",variable = var_image)
        eec_button = ttk.Checkbutton(choose_panel,text="eec",variable = var_eec)
        
        gene_button.grid(row=1,columnspan=2,sticky=tk.W)
        image_button.grid(row=2,columnspan=2,sticky=tk.W)
        eec_button.grid(row=3,columnspan=2,sticky=tk.W)
        

#--------------- 左2------------------

        ttk.Button(upload_panel,text="Upload gene dataset",style="UP.TButton",command = lambda: self.load_gene_dataset(var_gene)).grid(row=0,column=0,sticky=tk.W)
        ttk.Button(upload_panel,text="Upload gene label",style="UP.TButton",command = lambda: self.load_gene_label(var_gene)).grid(row=0,column=1,sticky=tk.W)
        ttk.Button(upload_panel,text="Upload image dataset",style="UP.TButton",command = lambda: self.load_image_dataset(var_image)).grid(row=1,column=0,sticky=tk.W)
        ttk.Button(upload_panel,text="Upload image label",style= "UP.TButton",command = lambda: self.load_image_label(var_image)).grid(row=1,column=1,sticky=tk.W)  
        ttk.Button(upload_panel,text="Upload EEC dataset",style="UP.TButton",command = lambda: self.load_eec_dataset(var_eec)).grid(row=2,column=0,sticky=tk.W)
        ttk.Button(upload_panel,text="Upload EEC label",style="UP.TButton",command = lambda: self.load_eec_label(var_eec)).grid(row=2,column=1,sticky=tk.W)

#--------------- 左3------------------

        ttk.Button(control_panel,text="Start",command = self.start_algorithm).grid(row=0,column=0,sticky=tk.W)
        ttk.Button(control_panel,text="End").grid(row=0,column=1,sticky=tk.W)


#--------------- 右1---------------
        ttk.Label(visual_panel,text="Best \"k\" First ").grid(row=0,column=0,sticky=tk.W)
        variable = tk.StringVar(visual_panel)
        option_menu = ttk.OptionMenu(visual_panel, variable, "1","2","3","4","5","6","7")
        option_menu.grid(row=0,column=1)
        completed_label = ttk.Label(visual_panel,text="进度条")
        completed_label.grid(row=2,columnspan=2,sticky=tk.W)


#--------------- 右2---------------
        output_panel = tk.Canvas(self.right_panel, width=500, height=500)
        output_panel.grid(rowspan=7)
    

    def __exit_app(self):
        exit()


    def load_gene_dataset(self,var):
        if var.get() == 1:
            file_name = askopenfilename(filetypes=(("TXT Files", "*.txt"),("CSV Files", "*.csv")))
            self.dataset_filename = file_name
        else:
            messagebox.showerror("ERROR!","You have not choose the gene")

    def load_gene_label(self,var):
        if var.get() == 1:
            file_name = askopenfilename(filetypes=(("TXT Files", "*.txt"),("CSV Files", "*.csv")))
            self.label_filename = file_name
        else:
            messagebox.showerror("ERROR!","You have not choose the gene")        

    def load_image_dataset(self,var):
        if var.get() == 1:
            print("load_image_dataset")
        else:
            messagebox.showerror("ERROR!","You have not choose the image")

    def load_image_label(self,var):
        if var.get() == 1:
            print("load_image_label")
        else:
            messagebox.showerror("ERROR!","You have not choose the image")        

    def load_eec_dataset(self,var):
        if var.get() == 1:
            print("load_eec_dataset")
        else:
            messagebox.showerror("ERROR!","You have not choose the eec")  

    def load_eec_label(self,var):
        if var.get() == 1:
            print("load_eec_label")
        else:
            messagebox.showerror("ERROR!","You have not choose the eec")          

                    
    def start_algorithm(self):
        if self.dataset_filename is not None and self.label_filename is not None:
            print("starting the calculate {}".format(self.dataset_filename.split(".")[0]))
            single_stop(self.dataset_filename,self.label_filename,1)

        
        


        




if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.master.mainloop()
