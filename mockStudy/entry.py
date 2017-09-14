
class InnerClass():

    def run(self):
        print("inner,real method run")


class OutClass():
    def __init__(self):
        self.inner = InnerClass()

    def run_inn(self):
        self.inner.run()