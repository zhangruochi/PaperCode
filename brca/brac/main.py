'''
python3

Required packages
- pandas
- numpy
- sklearn
- scipy


Info
- name   : "zhangruochi"
- email  : "zrc720@gmail.com"
- date   : "2017.5.1"
- Version : 2.0.0

Description
    brac
'''

import numpy as np
import scipy as sp
from single_main_six import single
import os
import pickle
from sklearn.model_selection import StratifiedKFold
from sklearn.multiclass import OneVsOneClassifier
from prepare import load_dataset
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from operator import itemgetter
from sklearn.linear_model import Ridge
from sklearn.metrics import confusion_matrix
import csv
from sklearn.linear_model import Lasso

import warnings
warnings.filterwarnings(action="ignore", module="scipy",
                        message="^internal gelsd")


# 得到特征并集
def get_feature_set(dataset_filename, json_filename, alpha, dataset, labels, estimator_list):
    if os.path.exists("result.txt"):
        os.remove("result.txt")

    """    
    classes_list = [[[1],[2]],[[1],[3]],[[1],[4]],[[2],[3]],[[2],[4]],[[3],[4]],\
        [[1,2],[3]],[[1,2],[4]],[[1,3],[2]],[[1,3],[4]],[[1,4],[2]],[[1,4],[3]],\
        [[2,3],[1]],[[2,3],[4]],[[2,4],[1]],[[2,4],[3]],[[3,4],[1]],[[3,4],[2]],\
        [[1],[2,3,4]],[[2],[1,3,4]],[[3],[1,2,4]],[[4],[1,2,3]],[[1,2],[3,4]],\
        [[1,3],[2,4]],[[1,4],[2,3]]]
    """
    classes_list = [[[1], [2]], [[1], [3]], [[2], [3]],
                    [[1, 2], [3]], [[1, 3], [2]], [[2, 3], [1]]]

    feature_set = set()
    for classes in classes_list:
        feature_names = single(
            dataset_filename, json_filename, classes=classes)
        macc, r2 = test_acc(
            dataset.loc[feature_names, :].T, labels, estimator_list)
        print("for classes {},\n the macc is: {},\n the r2 is: {},\n the opt is: {},\n the feature length is: {}\n".format(
            classes, macc, r2, r2 * macc, len(feature_names)))

        feature_set = feature_set.union(feature_names)

    with open("feature_set.pkl", "wb") as f:
        pickle.dump(feature_set, f)

    print("the feature set is: ")
    print(feature_set)
    print("the feature_set length is {}".format(len(feature_set)))

    return feature_set


# 选择分类器 D-tree,SVM,NBayes,KNN
def select_estimator(case):

    if case == "SVM":
        estimator = SVC()
    elif case == "KNN":
        estimator = KNeighborsClassifier()
    elif case == "DT":
        estimator = DecisionTreeClassifier()
    elif case == "NB":
        estimator = GaussianNB()
    elif case == "LG":
        estimator = LogisticRegression()
    elif case == "LSVM":
        estimator = LinearSVC()

    return estimator


# 采用 K-Fold 交叉验证 得到 aac
def get_acc(estimator, X, y, skf):
    scores = []
    cm = np.zeros((3, 3))

    for train_index, test_index in skf.split(X, y):
        X_train, X_test = X.ix[train_index], X.ix[test_index]
        y_train, y_test = y[train_index], y[test_index]
        estimator.fit(X_train, y_train)
        scores.append(estimator.score(X_test, y_test))
        cm += confusion_matrix(y_test, estimator.predict(X_test))
    return np.mean(scores), cm


# 删除最不重要的 N 个特征
def delete_feature(coefs, feature_name, k=2):

    index_coefs = [(a, abs(coef)) for a, coef in zip(feature_name, coefs)]
    sorted_index_coefs = sorted(index_coefs, key=itemgetter(1), reverse=True)

    for item in sorted_index_coefs[-k:]:
        feature_name.remove(item[0])

    return feature_name


# 均方误差根
def rmse(y_test, y):
    return sp.sqrt(sp.mean((y_test - y) ** 2))


# 优化目标
def optimization(acc, r2):
    return acc * r2


# 循环删除
def recursive_elimination(dataset, labels):
    feature_name = dataset.columns.tolist()
    clf = Ridge(random_state=7)
    skf = StratifiedKFold(n_splits=10, random_state=7)

    OPT = []
    ACC = []
    R2 = []
    NUM = []
    k = 5

    while True:
        try:
            #print("current_length: "+ str(len(feature_name)))
            clf.fit(dataset, labels)
            y_pre = clf.predict(dataset)

            acc = four_class_acc(
                dataset.loc[:, feature_name], labels, ["LG"], skf)
            r2 = r2_score(labels, y_pre)
            #r22 = rmse(labels,y_pre)
            opt = optimization(acc, r2)

            OPT.append(opt)
            ACC.append(acc)
            R2.append(r2)
            NUM.append(len(feature_name))
            print(len(feature_name), opt, acc, r2)

            feature_name = delete_feature(clf.coef_, feature_name, k=k)
            dataset = dataset.loc[:, feature_name]
        except:
            break

    with open("result_{}.csv".format(k), "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([" "] + NUM)
        writer.writerow(["opt"] + OPT)
        writer.writerow(["acc"] + ACC)
        writer.writerow(["r_2"] + R2)

    return feature_name


# 四分类的准确性
def four_class_acc(dataset, labels, estimator_list, skf):
    max_estimator_aac = 0
    for estimator in estimator_list:
        estimator_aac, cm = get_acc(OneVsOneClassifier(
            select_estimator(estimator)), dataset, labels, skf)
        #print("the acc for {}: {}".format(estimator,estimator_aac))
        if estimator_aac > max_estimator_aac:
            max_estimator_aac = estimator_aac  # 记录对于 k 个 特征 用五个个estimator 得到的最大值
    # print("-"*20)
    #print("the macc is: {}\n".format(max_estimator_aac))
    # print(cm)
    return max_estimator_aac


def test_acc(X, y, estimator_list):
    """
    df = pd.read_csv("eggs.csv")
    y = df.values[0]
    estimator = OneVsOneClassifier(LogisticRegression())
    """

    skf = StratifiedKFold(n_splits=10)
    clf = Ridge()

    macc = four_class_acc(X, y, estimator_list, skf)
    clf.fit(X, y)
    r2 = clf.score(X, y)

    return macc, r2


# 主函数
def main(dataset_filename, json_filename, n_splits=10, estimator_list=["SVM", "KNN", "DT", "NB", "LG"], alpha=0.01):

    skf = StratifiedKFold(n_splits=n_splits)
    filtered_dataset, labels = load_dataset(dataset_filename, json_filename)
    labels = np.array(labels)

    if os.path.exists("feature_set.pkl"):
        with open("feature_set.pkl", "rb") as f:
            feature_set = pickle.load(f)
    else:
        feature_set = get_feature_set(
            dataset_filename, json_filename, alpha, filtered_dataset, labels, estimator_list)

    dataset = filtered_dataset.loc[feature_set, :].T

    feature_set = set(dataset.columns.tolist())
    print("the union set length: " + str(len(feature_set)))
    current_length = len(feature_set)
    acc, r2 = test_acc(dataset, labels, estimator_list)

    print("the acc is: {},\n the r2 is: {},\n the opt is: {},\n the feature length is: {}\n".format(
        acc, r2, acc * r2, current_length))

    print("\nafter recursive elimination......\n")

    if not os.path.exists("feature_list.pkl"):
        feature_list = recursive_elimination(dataset, labels)
        with open("feature_list.pkl", "wb") as f:
            pickle.dump(feature_list, f)
    else:
        with open("feature_list.pkl", "rb") as f:
            feature_list = pickle.load(f)


if __name__ == '__main__':
    #get_feature_set("matrix_data.tsv","clinical.project-TCGA-BRCA.2017-04-20T02_01_20.302397.json",feature_range = 20)
    main("matrix_data.tsv", "clinical.project-TCGA-BRCA.2017-04-20T02_01_20.302397.json", n_splits=10,
         estimator_list=["LG"])
