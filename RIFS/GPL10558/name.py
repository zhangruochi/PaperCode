import pickle

with open("name_index.pkl","rb") as f:
    name_dict = pickle.load(f)
print(name_dict)