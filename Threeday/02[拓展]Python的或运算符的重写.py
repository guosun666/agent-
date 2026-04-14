class Test(object):
    def __init__(self, name):
        self.name = name
    def __or__(self,other):
        # return [self,other]   如果只有a|b的话，返回[a,b]，但是a|b|c的话，前面是list类，是没有这种方法
        return MySeq(self,other)
    def __str__(self):
        return self.name 
        # 如果不想让print输出对象的地址，可以重写__str__方法。返回Name的值

class MySeq(object):
    def __init__(self, *args):
        self.sequence = []
        for arg in args:
            self.sequence.append(arg)
    def __or__(self,other):
        self.sequence.append(other)
        return self
    def run(self):
        for item in self.sequence:
            print(item)


if __name__ == "__main__":
    a = Test("a")  #""只是代表一个字符串，并不是内容
    b = Test("b")
    c = Test("c")

    d = a | b | c
    d.run()
    print(type(d))