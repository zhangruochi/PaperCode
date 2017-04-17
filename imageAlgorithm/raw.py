def test():
    a = 0
    def test2():
        b = a
        print(b)
    test2()

test()        