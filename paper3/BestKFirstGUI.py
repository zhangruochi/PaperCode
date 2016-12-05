import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import commondialog
import tkinter.filedialog
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename

from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from rifs import *

#grid (-column, -columnspan, -in, -ipadx, -ipady, -padx, -pady, -row, -rowspan, or -sticky)
#pack (-after, -anchor, -before, -expand, -fill, -in, -ipadx, -ipady, -padx, -pady, or -side)

class App(ttk.Frame):
    def __init__(self,master=None):
        super().__init__(master)

        #rifs
        self.percent = 0.4
        self.stop = 3

        #lasso
        self.alpha = 1.0
        self.max_iter = 1000

        #randomforest
        self.n_estimators = 10   #The number of trees in the forest
        self.max_features = "auto"   #sqrt log2
        self.min_samples_leaf = 1  # int float
        self.max_depth = None
        self.min_samples_split = 2 #int float
        self.n_jobs = 1  


        self.algorithm = "RIFS"

        self.dataset_filename = None
        self.label_filename = None

        self.dataset = None
        self.labels = None

        self.estimator_list = [0,1,2,3,4]

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
        
        choose_panel = ttk.Frame(self.left_panel,borderwidt=30)
        choose_panel.pack(fill=tk.BOTH,expand=1,side=tk.TOP)
        upload_panel = ttk.Frame(self.left_panel,borderwidt=30)
        upload_panel.pack(fill=tk.BOTH,expand=1,side = tk.BOTTOM)
        
        
#--------------- 左1------------------
        ttk.Label(choose_panel,text="Select the algorithm: ",style="SE.TLabel").grid(row = 0,column = 0,columnspan = 2, pady = 20,sticky=tk.N)

        v_algorithm = tk.StringVar()
        option_menu = ttk.OptionMenu(choose_panel, v_algorithm, "RIFS","RIFS","T test","Lasso","Random Forest",command = lambda x: self.__generate_para(v_algorithm))
        option_menu.grid(row = 0,column = 2,sticky=tk.E)
        
#--------------- 左2------------------
        self.dataset_panel = tk.Text(upload_panel,width = 50,)
        self.dataset_panel.grid(row = 0,column = 0,columnspan = 2, sticky = tk.W)
        ttk.Button(upload_panel,text="Upload dataset file",style="UP.TButton",command = self.load_dataset).grid(row = 1,column=0,pady = 10,sticky = tk.S)
        ttk.Button(upload_panel,text="Upload label file",style="UP.TButton",command = self.load_label).grid(row = 1,pady = 10,column=1,sticky = tk.S)
        ttk.Button(upload_panel,text="Confirm",command = self.__check_file).grid(row=2,column=0,columnspan=2,pady=15)


#--------------- 右---------------
        ttk.Label(self.right_panel,text="OUTPUT",style="OU.TLabel").grid(row=0,column = 0,columnspan=3,pady=10,padx=10)    
        self.output_panel = tk.Text(self.right_panel,width = 70, height = 30)
        self.output_panel.grid(row = 1,columnspan = 2, pady = 20)

        ttk.Button(self.right_panel,text="Start",command = self.start_algorithm).grid(row=2,column=0,pady=10,padx=35,sticky=tk.W)
        ttk.Button(self.right_panel,text="Stop",command = self.__exit_app).grid(row=2,column=1,pady=10,sticky=tk.W)
    

    def __exit_app(self):
        exit()

    def __check_file(self):
        if self.dataset_filename == None or self.label_filename == None:
            messagebox.showerror("ERROR!","You have not load the dataset!")
        else:
            self.dataset_panel.insert(tk.END,"loading the dataset and labels......\n")
            self.dataset = load_data(self.dataset_filename)
            self.labels = load_class(self.label_filename)
            self.dataset_panel.insert(tk.END,"the dataset shape is: {}\n".format(self.dataset.shape))
            self.dataset_panel.insert(tk.END,"the label shape is: {}\n\n".format(self.labels.shape))

            self.dataset_panel.insert(tk.END,"the look of dataset: \n\n")
            self.dataset_panel.insert(tk.END,"{}\n\n".format(self.dataset.iloc[0:11,0:9]))

            self.dataset_panel.insert(tk.END,"the look of label: \n\n")
            self.dataset_panel.insert(tk.END,"{}".format(self.labels[0:20].T))


    def __generate_para(self,v_algorithm):
        self.algorithm = v_algorithm.get()
        if  self.algorithm == "RIFS":
            otherFrame = tk.Toplevel()
            #otherFrame.geometry("200x200")
            otherFrame.title("otherFrame")
            
            self.v_percent = tk.StringVar()
            self.v_stop = tk.StringVar()
            tk.Label(otherFrame,text="percent:  ").grid(row=1,column=0,padx=10,sticky=tk.W)
            ttk.Entry(otherFrame,textvariable = self.v_percent,style="SE.TEntry").grid(row=1,column=1)
            tk.Label(otherFrame,text="Stop:  ").grid(row=2,column=0,padx=10,sticky=tk.W)
            ttk.Entry(otherFrame,textvariable = self.v_stop,style="SE.TEntry").grid(row=2,column=1)

            handler = lambda: self.__close_otherFrame(otherFrame)
            ttk.Button(otherFrame, text="Confirm", command=handler).grid(row = 3,column = 0, columnspan = 2,pady = 20)
        
        elif self.algorithm == "T-test":
            pass
        
        elif self.algorithm == "Lasso":
            otherFrame = tk.Toplevel()
            #otherFrame.geometry("200x200")
            otherFrame.title("choose your paramters")
            
            self.v_alpha = tk.StringVar()
            self.v_max_iter = tk.StringVar()
            tk.Label(otherFrame,text="alpha:  ").grid(row=1,column=0,padx=10,sticky=tk.W)
            ttk.Entry(otherFrame,textvariable = self.v_alpha,style="SE.TEntry").grid(row=1,column=1)
            tk.Label(otherFrame,text="max_iter:  ").grid(row=2,column=0,padx=10,sticky=tk.W)
            ttk.Entry(otherFrame,textvariable = self.v_max_iter,style="SE.TEntry").grid(row=2,column=1)

            handler = lambda: self.__close_otherFrame(otherFrame)
            ttk.Button(otherFrame, text="Confirm", command=handler).grid(row = 3,column = 0, columnspan = 2,pady = 20)
        
        elif self.algorithm == "Random Forest":
            otherFrame = tk.Toplevel()
            #otherFrame.geometry("200x200")
            otherFrame.title("choose your paramters")
            
            self.v_n_estimators = tk.StringVar()   #The number of trees in the forest
            self.v_max_features = tk.StringVar()   #sqrt log2
            self.v_min_samples_leaf = tk.StringVar()  # int float
            self.v_max_depth = tk.StringVar()
            self.v_min_samples_split = tk.StringVar() #int float
            self.v_n_jobs = tk.StringVar()  

            tk.Label(otherFrame,text="estimators:  ").grid(row=1,column=0,padx=10,sticky=tk.W)
            ttk.Entry(otherFrame,textvariable = self.v_n_estimators,style="SE.TEntry").grid(row=1,column=1)
            tk.Label(otherFrame,text="max features:  ").grid(row=2,column=0,padx=10,sticky=tk.W)
            ttk.Entry(otherFrame,textvariable = self.v_max_features,style="SE.TEntry").grid(row=2,column=1)
            tk.Label(otherFrame,text="min samples leaf:  ").grid(row=3,column=0,padx=10,sticky=tk.W)
            ttk.Entry(otherFrame,textvariable = self.v_min_samples_leaf,style="SE.TEntry").grid(row=3,column=1)
            tk.Label(otherFrame,text="min samples split:  ").grid(row=4,column=0,padx=10,sticky=tk.W)
            ttk.Entry(otherFrame,textvariable = self.v_min_samples_split,style="SE.TEntry").grid(row=4,column=1)
            tk.Label(otherFrame,text="max depth:  ").grid(row=5,column=0,padx=10,sticky=tk.W)
            ttk.Entry(otherFrame,textvariable = self.v_max_depth,style="SE.TEntry").grid(row=5,column=1)
            tk.Label(otherFrame,text="jobs:  ").grid(row=6,column=0,padx=10,sticky=tk.W)
            ttk.Entry(otherFrame,textvariable = self.v_n_jobs,style="SE.TEntry").grid(row=6,column=1)


            handler = lambda: self.__close_otherFrame(otherFrame)
            ttk.Button(otherFrame, text="Confirm", command=handler).grid(row = 7,column = 0, columnspan = 2,pady = 20)   

    
    def __close_otherFrame(self,otherFrame):
        
        if self.algorithm == "RIFS":
            if len(self.v_percent.get()) != 0:
                self.percent = float(self.v_percent.get())
            if len(self.v_stop.get()) != 0: 
                self.stop = int(self.v_stop.get()) 
            otherFrame.destroy()
        
        elif self.algorithm == "Lasso":
            if len(self.v_alpha.get()) != 0:
                self.alpha = float(self.v_alpha.get())
            if len(self.v_max_iter.get()) != 0: 
                self.max_iter = int(self.v_max_iter.get())
            otherFrame.destroy()

        elif self.algorithm == "Random Forest":
            if len(self.v_n_estimators.get()) != 0:
                self.n_estimators = int(self.v_n_estimators.get())
            if len(self.v_max_features.get()) != 0:
                self.max_features = int(self.v_max_features.get())
            if len(self.v_min_samples_leaf.get()) != 0:
                self.min_samples_leaf = int(self.v_min_samples_leaf.get())    
            if len(self.v_max_depth.get()) != 0:
                self.max_depth = int(self.v_max_depth.get())
            if len(self.v_min_samples_split.get()) != 0:
                self.min_samples_split = int(self.v_min_samples_split.get())
            if len(self.v_n_jobs.get()) != 0:
                self.n_jobs = int(self.v_n_jobs.get())   
            otherFrame.destroy()          

             
    def load_dataset(self):
        try:
            file_name = askopenfilename(filetypes=(("TXT Files", "*.txt"),("CSV Files", "*.csv")))
            self.dataset_filename = file_name
        except:
            messagebox.showerror("ERROR!","Load file unsuccessful!")

    def load_label(self):
        try:
            file_name = askopenfilename(filetypes=(("TXT Files", "*.txt"),("CSV Files", "*.csv")))
            self.label_filename = file_name
        except:
            messagebox.showerror("ERROR!","Load file unsuccessful!")        

         
    def start_algorithm(self):
        if self.algorithm == "RIFS":
            self.output_panel.insert(tk.END,"Starting finding the subfeatures using RIFS:\n\n")
            self.using_rifs(self.dataset,self.labels)
        
        elif self.algorithm == "Lasso":
            self.output_panel.insert(tk.END,"Starting finding the subfeatures using Lasso:\n\n")
            self.using_lasso(self.dataset.T,self.labels)

        elif self.algorithm == "Random Forest":
            self.output_panel.insert(tk.END,"Starting finding the subfeatures using Random Forest:\n\n")
            self.using_random_forest(self.dataset.T,self.labels)

        else:
            commondialog
            messagebox.showerror("ERROR!","You have not load the dataset!")


    def using_lasso(self,X,y):
        estimator = Lasso(alpha = self.alpha, max_iter = self.max_iter)
        skf = StratifiedKFold(n_splits=3)
        scores = []
        for train_index,test_index in skf.split(X,y):
            X_train, X_test = X.ix[train_index], X.ix[test_index]
            y_train, y_test = y[train_index], y[test_index]
            estimator.fit(X_train,y_train)
            scores.append(estimator.score(X_test,y_test))

        number_of_subfeature = np.sum([1 for importance in estimator.coef_ if importance != 0])     
        self.output_panel.insert(tk.END,"                        the report \n\n\n")
        self.output_panel.insert(tk.END,"the number of subfeature: {} \n\n".format(number_of_subfeature))
        self.output_panel.insert(tk.END,"the parameter vector: {} ...... \n\n".format(estimator.coef_[estimator.coef_ != 0][0:2]))
        self.output_panel.insert(tk.END,"the number of iterations: {} \n\n".format(estimator.n_iter_))


        self.output_panel.insert(tk.END,"using the subfeature tor classfier: \n")
        self.output_panel.insert(tk.END,"the accuracy is: \n\n")
        X = X.iloc[:,estimator.coef_ != 0]

        names = ["SVM","KNeighbors","DecisionTree","NaiveBayes","LogisticRegression"]
        index = 0
        for estimator in self.estimator_list:
            clf,estimator_aac = get_aac(select_estimator(estimator),X,y,skf)
            self.output_panel.insert(tk.END,"for {}: {} \n".format(names[index],estimator_aac))
            index += 1

    def using_random_forest(self,X,y):
        estimator = RandomForestClassifier(n_estimators = self.n_estimators,max_features = self.max_features,\
            max_depth = self.max_depth, min_samples_leaf = self.min_samples_leaf,min_samples_split = self.min_samples_split,\
            n_jobs = self.n_jobs)
        skf = StratifiedKFold(n_splits=3)
        scores = []
        for train_index,test_index in skf.split(X,y):
            X_train, X_test = X.ix[train_index], X.ix[test_index]
            y_train, y_test = y[train_index], y[test_index]
            estimator.fit(X_train,y_train)
            scores.append(estimator.score(X_test,y_test))

        number_of_subfeature = np.sum([1 for importance in estimator.feature_importances_ if importance != 0])   
        self.output_panel.insert(tk.END,"                        the report \n\n\n")
        self.output_panel.insert(tk.END,"the number of subfeature: {} \n\n".format(number_of_subfeature))
        self.output_panel.insert(tk.END,"the feature importance: {} ...... \n\n".format(estimator.feature_importances_[estimator.feature_importances_ != 0][0:2]))
        self.output_panel.insert(tk.END,"The collection of fitted sub-estimators:\n {} \n\n".format(estimator.estimators_[0:2]))


        self.output_panel.insert(tk.END,"using the subfeature tor classfier: \n")
        self.output_panel.insert(tk.END,"the accuracy is: \n\n")
        X = X.iloc[:,estimator.feature_importances_ != 0]

        names = ["SVM","KNeighbors","DecisionTree","NaiveBayes","LogisticRegression"]
        index = 0
        for estimator in self.estimator_list:
            clf,estimator_aac = get_aac(select_estimator(estimator),X,y,skf)
            self.output_panel.insert(tk.END,"for {}: {} \n".format(names[index],estimator_aac))
            index += 1

    def using_rifs(self,dataset,labels):
    #------------参数接口---------------    
        seed_number = 7
        skf = StratifiedKFold(n_splits = 3)
        estimator_list = [0,1,2,3,4]
    #----------------------------------    

        start = time.time()
        visual_process = 0
        dataset = rank_t_value(dataset,labels)
        print(self.percent,self.stop)
        loc_of_first_feature = random_num_generator(dataset.shape[1], seed_number, self.percent) # 重启的位置

        max_loc_aac = 0
        max_aac_list = []
        feature_range = dataset.shape[1]


        for loc in loc_of_first_feature:
            num = 0
            max_k_aac = 0 
            count = 0  #记录相等的次数
            best_estimator = -1   
            
            for k in range(feature_range - loc):  # 从 loc位置 开始选取k个特征
                max_estimator_aac = 0
                locs = [i for i in range(loc,loc+k+1)]
                X = dataset.iloc[:,locs]

                for item in estimator_list:
                    clf,estimator_aac = get_aac(select_estimator(item),X,labels,skf)
                    if estimator_aac > max_estimator_aac:
                        max_estimator_aac = estimator_aac   #记录对于 k 个 特征 用四个estimator 得到的最大值
                        best_temp_estimator = item
         
                if max_estimator_aac > max_k_aac:
                    count = 0 
                    max_k_aac = max_estimator_aac   #得到的是从 loc 开始重启的最大值
                    num = k+1
                    best_estimator = best_temp_estimator
                
                else:
                    count += 1
                    if count == self.stop:
                        break
       
            if max_k_aac > max_loc_aac:
                max_loc_aac = max_k_aac
                max_aac_list = []
                max_aac_list.append((loc,num,max_loc_aac,best_estimator))
                with open("result.txt","a") as infor_file:
                    infor_file.write(">: {}\n".format(max_aac_list))

            elif max_k_aac == max_loc_aac:
                max_aac_list.append((loc,num,max_loc_aac,best_estimator))
                with open("result.txt","a") as infor_file:
                    infor_file.write("=: {}\n".format(max_aac_list))

            self.output_panel.insert(tk.END,".")
            self.master.update_idletasks() 
            visual_process += 1
            if visual_process == 50:
                self.output_panel.delete(1.0, tk.END)
                self.output_panel.insert(tk.END,"Starting finding the subfeatures using RIFS:\n\n")
                self.master.update_idletasks()
                visual_process = 0

        end = time.time()
        output = sorted(max_aac_list,key=lambda x:x[1])[0]
        self.output_panel.delete(1.0, tk.END)
        self.output_panel.insert(tk.END,"                        the report \n\n\n")
        self.output_panel.insert(tk.END,"using time: {}\n".format(end-start))  
        self.output_panel.insert(tk.END,"the best output is: {} \n\n".format(output))

        self.output_panel.insert(tk.END,"using the subfeature tor classfier, \n")
        self.output_panel.insert(tk.END,"the accuracy is: \n")

        estimator_list = [0,1,2,3,4]
        skf = StratifiedKFold(n_splits = 3)
        ranked_subfeature_list = [output[0],output[1]]
        feature_list = deal_output(self.dataset,self.labels,ranked_subfeature_list)
        print(feature_list)
        names = ["SVM","KNeighbors","DecisionTree","NaiveBayes","LogisticRegression"]
        index = 0
        for index in estimator_list:
            clf,estimator_aac = get_aac(select_estimator(index),self.dataset.iloc[feature_list,:].T,self.labels,skf)
            self.output_panel.insert(tk.END,"for {}: {} \n".format(names[index],estimator_aac))
            index += 1
                
        

             
                


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.master.mainloop()
