def test1():
    a,b = [],[]
    def test2():
        print(a)
        test3()
    test2()

def test3():
    print("fuck!")   

test1()

import pandas as pd
df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
print(df)
df.rename(2)
print(df)


