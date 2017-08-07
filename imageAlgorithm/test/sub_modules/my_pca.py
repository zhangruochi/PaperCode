from sklearn.decomposition import PCA

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser 


def implement_pca(dataset):
    cf = ConfigParser.ConfigParser()
    cf.read('config.cof')

    option_dict = dict()
    for key,value in cf.items("PCA"):
        option_dict[key] = eval(value)
    
    pca = PCA(**option_dict)
    dataset = pca.fit_transform(dataset)
    return dataset