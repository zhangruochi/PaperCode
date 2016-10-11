def test1():
    a,b = [],[]
    def test2():
        print(a)
        test3()
    test2()

def test3():
    print("fuck!")        

if __name__ == '__main__':
    test1()        
