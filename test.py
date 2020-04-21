class Test:

    def __init__(self):
        self.path = ""
        self.lol()

    def lol(self):
        print(self.rep())
        self.path = "meep"
        print(self.rep())
        self.lolazo()
        
    def lolazo(self):
        print(self.rep())
        self.path = "boo"
        print(self.rep())
        
    def rep(self):
        return self.path

A = Test()