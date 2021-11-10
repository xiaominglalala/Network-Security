class Human(object):
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
    def get_info(self):
        print("my name is %s,age is %s"%(self.name, self.age))
man1 = Human("李四", 22, "man")
list1 = [1, 2, 3]
dict1 = {"name":"张三", "age":12}

flag = True
try:
    man1.get_info1()
    print(flag)
except:
    flag = False
    print(flag)




