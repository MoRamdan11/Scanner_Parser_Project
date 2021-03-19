from pydotplus import *
from graphviz import Graph

class Parser:
    def __init__(self, scanner_token, scanner_tokenType):
        self.token = scanner_token
        self.tokenType = scanner_tokenType
        self.index = 0
        self.g = Graph()

    def match(self, val):
        if self.token[self.index] == val:
            self.index = self.index + 1
            return True
        else:
            return False

    def addop(self):
        if self.token[self.index] == '+' or self.token[self.index] == '-':
            self.index = self.index + 1
            return True
        else:
            return False

    def mulop(self):
        if self.token[self.index] == '*' or self.token[self.index] == '/':
            self.index = self.index + 1
            return True
        else:
            return False

    def compop(self):
        if self.token[self.index] == '>' or self.token[self.index] == '=' or self.token[self.index] == '<':
            self.index = self.index + 1
            return True
        else:
            return False

    def stmt_seq(self):#stmt{;stmt}
        if self.stmt() == False:
            return False
        while self.stmt() == True:
            self.index = self.index
        return True

    def stmt(self):
        #Read Stmt
        if self.token[self.index] == 'read':
            if self.read() == False:
                print('Syntax Error')
                return False
            print('read-stmt')
            return True # stmt is correct
        #Write Stmt
        elif self.token[self.index] == 'write':
            if self.write() == False:
                print('Syntax Error')
                return False
            print('Write-stmt')
            return True # stmt is correct
        #Assign Stmt
        elif self.tokenType[self.index] == 'Identifier':
            if self.assign() == False:
                print('Syntax Error')
                return False
            print('Assignment stmt')
            return True # stmt is correct
        #If Stmt
        elif self.token[self.index] == 'if':
            if self.if_stmt() == False:
                print('Syntax Error')
                return False
            print('If-stmt')
            return True  # stmt is correct
        #Repeat Stmt
        elif self.token[self.index] == 'repeat':
            if self.repeat() == False:
                print('Syntax Error')
                return False
            print('Repeat-stmt')
            return True  # stmt is correct
        else:
            return False

    def exp(self):
        if self.simple_exp() == False: #simple_exp [com_op simple_exp]
            return False
        if self.token[self.index] == '>' or self.token[self.index] == '=' or self.token[self.index] == '<': # [com_op simple_exp]
            if self.compop() == False:
                return False
            if self.simple_exp() == False:
                return False
        return True

    def simple_exp(self):
        if self.term() == True:#term{addop term}
            while self.token[self.index] == '+' or self.token[self.index] == '-':
                if self.addop() == False:
                    return False
                if self.term() == False:
                    return False
        else:
            return False
        return True

    def if_stmt(self): # if_stmt --> if exp then stmt_seq [else stmt_seq] end
        if self.match('if') == False:
            return False
        if self.exp() == False:# condition
            return False
        if self.match('then') == False:
            return False
        if self.stmt_seq() == False:
            return False
        if self.match('else') == True:
            if self.stmt_seq() == False:
                return False
        if self.match('end') == False:
            return False
        return True

    def repeat(self):#repeat stmt_seq until exp
        if self.match('repeat') == False:
            return False
        if self.stmt_seq() == False:
            return False
        if self.match('until') == False:
            return False
        if self.exp() == False:
            return False
        if self.match(';') == False:
            return False
        return True

    def factor(self):
        if self.tokenType[self.index] == 'Number' or self.tokenType[self.index] == 'Identifier':
            self.index = self.index + 1
            return True
        elif self.token[self.index] == '(':
            if self.match('(') == False:
                return False
            if self.simple_exp() == False:
                return False
            if self.match(')') == False:
                return False
            return True
        else:
            return False # can't find number or (simple_exp)
    def term(self):
        if self.factor() == True:# factor{mulop factor}
            while self.token[self.index] == '*' or self.token[self.index] == '/':
                if self.mulop() == False:
                    return False
                if self.factor() == False:
                    return False
        else:
            return False
        return True

    def read(self):
        if self.match('read') == False:
            return False
        if self.tokenType[self.index] == 'Identifier' or self.tokenType[self.index] == 'Number':
            self.index = self.index
        else:
            return False
        #self.s.push(self.g.node('r', 'read\n(' + str(self.token[self.index]) + ')', shape='rectangle'))
        self.index = self.index + 1
        if self.match(';') == False:
            return False
        return True

    def write(self):
        if self.match('write') == False: # Match write
            return False
        if self.simple_exp() == False:
            return False
        return True

    def assign(self):
        if self.token[self.index + 1] != ':=':
            return False
        if self.tokenType[self.index] != 'Identifier':
            return False
        id = self.token[self.index]
        self.index = self.index + 1
        if self.match(':=') == False:
            return False
        if self.simple_exp() == False:
            return False
        '''if self.match(';') == False:
            return False'''
        self.g.node('a', 'assign\n(' + str(id) + ')', shape='rectangle')
        return True

    def program(self):
        self.g = Graph()
        self.g.format = 'png'
        self.index = 0
        while self.index < len(self.token):
            if self.stmt() == False:
                return False
        self.g.view()