import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

class App(ttk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.master.title("异构数据融合")
        self.master.geometry("1000x600+300+200")
        self.pack(fill=tk.BOTH,expand=1)
        self.operation_panel = ttk.Frame(self)
        self.operation_panel.grid(column=0)
        self.output_panel = ttk.Frame(self)
        self.output_panel.grid(column=1)

        self.initial_app()


    def initial_app(self): 
        

        style = ttk.Style()
        style.configure("OR.TLabel", foreground="black", background="wite")
        
        
        #选择标签

        var_gene = tk.IntVar()
        var_image = tk.IntVar()
        var_eec = tk.IntVar()    
        ttk.Checkbutton(self.operation_panel,text="gene",variable = var_gene).grid(row=0,column=0,sticky=tk.W)
        ttk.Checkbutton(self.operation_panel,text="image",variable = var_image).grid(row=1,column=0,sticky=tk.W)
        ttk.Checkbutton(self.operation_panel,text="eec",variable = var_eec).grid(row=3,column=0,sticky=tk.W)

        ttk.Button(self.operation_panel,text="confirm",command= lambda: self.generate_button(var_gene,var_image,var_eec)).grid(row=4,column=0,sticky=tk.W)
        ttk.Button(self.operation_panel,text="clear").grid(row=4,column=1,sticky=tk.W)


    
    def generate_button(self,var_gene,var_image,var_eec):
        if var_gene.get() == 1 and var_image.get() == 0 and var_eec.get() == 0:
            ttk.Button(self.operation_panel,text="upload gene dataset").grid(row=6,column=0,sticky=tk.W)
            ttk.Button(self.operation_panel,text="upload gene label").grid(row=6,column=1,sticky=tk.W)
        elif var_gene.get() == 0 and var_image.get() == 1 and var_eec.get() == 0:
            ttk.Button(self.operation_panel,text="upload image dataset").grid(row=7,column=0,sticky=tk.W)
            ttk.Button(self.operation_panel,text="upload image label").grid(row=7,column=1,sticky=tk.W)
        elif var_gene.get() == 0 and var_image.get() == 0 and var_eec.get() == 1:
            ttk.Button(self.operation_panel,text="upload EEC dataset").grid(row=8,column=0,sticky=tk.W)
            ttk.Button(self.operation_panel,text="upload EEC label").grid(row=8,column=1,sticky=tk.W)

        elif var_gene.get() == 1 and var_image.get() == 1 and var_eec.get() == 0:
            ttk.Button(self.operation_panel,text="upload gene dataset").grid(row=6,column=0,sticky=tk.W)
            ttk.Button(self.operation_panel,text="upload gene label").grid(row=6,column=1,sticky=tk.W)
            ttk.Button(self.operation_panel,text="upload image dataset").grid(row=7,column=0,sticky=tk.W)
            ttk.Button(self.operation_panel,text="upload image label").grid(row=7,column=1,sticky=tk.W) 
        elif var_gene.get() == 1 and var_image.get() == 0 and var_eec.get() == 1:
            ttk.Button(self.operation_panel,text="upload gene dataset").grid(row=6,column=0,sticky=tk.W)
            ttk.Button(self.operation_panel,text="upload gene label").grid(row=6,column=1,sticky=tk.W)
            ttk.Button(self.operation_panel,text="upload EEC dataset").grid(row=7,column=0,sticky=tk.W)
            ttk.Button(self.operation_panel,text="upload EEC label").grid(row=7,column=1,sticky=tk.W)

        elif var_gene.get() == 0 and var_image.get() == 1 and var_eec.get() == 1:
            ttk.Button(self.operation_panel,text="upload image dataset").grid(row=6,column=0,sticky=tk.W)
            ttk.Button(self.operation_panel,text="upload image label").grid(row=6,column=1,sticky=tk.W)
            ttk.Button(self.operation_panel,text="upload EEC dataset").grid(row=7,column=0,sticky=tk.W)
            ttk.Button(self.operation_panel,text="upload EEC label").grid(row=7,column=1,sticky=tk.W)
        elif var_gene.get() == 1 and var_image.get() == 1 and var_eec.get() == 1:  
            ttk.Button(self.operation_panel,text="upload gene dataset").grid(row=6,column=0,sticky=tk.W)
            ttk.Button(self.operation_panel,text="upload gene label").grid(row=6,column=1,sticky=tk.W)
            ttk.Button(self.operation_panel,text="upload image dataset").grid(row=7,column=0,sticky=tk.W)
            ttk.Button(self.operation_panel,text="upload image label").grid(row=7,column=1,sticky=tk.W)  
            ttk.Button(self.operation_panel,text="upload EEC dataset").grid(row=8,column=0,sticky=tk.W)
            ttk.Button(self.operation_panel,text="upload EEC label").grid(row=8,column=1,sticky=tk.W)
        else: 
            messagebox.showwarning("error","you have not choose a kind of dataset!") 

    """
    def getGene(self,var):
        return var.get()

    def getImage(self,var):
        return var.get()

    def getEec(self,var):
        return var.get()  
    """          

        


        


        




if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.master.mainloop()
