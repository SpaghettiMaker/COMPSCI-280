class A:
    def __init__(self):
        A.state = 'CHAT'

    def method1(self):
        A.state = 'SEND'

    def printer(self):
        print(A.state)


class B(A):
    def method2(self):
        self.method1()
        print(B.state)

ob_B = B()
ob_A = A()
ob_B.method2()
ob_A.printer()
