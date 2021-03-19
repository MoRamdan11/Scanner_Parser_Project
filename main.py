from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from Design import Ui_MainWindow
from parser import Parser
from pydotplus import *

global scanner_token
global scanner_tokenType

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.pushButton.clicked.connect(self.upload)

    def is_reserved(self, scanner_token):
        reservedwords = ['if', 'then', 'else', 'end', 'repeat',
                         'until', 'read', 'write', 'false',
                         'true', 'while', 'do', 'end', 'while',
                         'not', 'case', 'of', 'accept', 'error'
                         'advance', 'int', 'double']
        for i in reservedwords:
            if scanner_token == i:
                return True
        return False

    def is_sympol(self, scanner_token):
        symbols = ['+', '-', '*', '/', '=', '<', '(', ')', ';', ':=',
                   ':', ',', '>', '>=', '<=', '==']
        for i in symbols:
            if scanner_token == i:
                return True
        return False

    def upload(self):
        try:
            global scanner_token
            global scanner_tokenType
            lines = []  # lines of our files
            scanner_token = []
            scanner_tokenType = []
            filename = QFileDialog.getOpenFileName()
            self.textEdit.clear()
            self.tableWidget.clear()
            self.tableWidget.insertRow(0)
            path = filename[0]
            with open(path, "r", encoding='utf-8') as f:
                file = f.read()
            self.textEdit.insertPlainText(file)
            for i in file.splitlines():
                lines.append(i)
            index = 0  # not the global variable index
            comment = 0
            while index < len(lines):  # Make program loop for all lines
                for i in lines[index].split():
                    i = i.lower()
                    if i.__contains__('(('):
                        i = i.replace('(', '')
                        scanner_token.append('(')
                        scanner_token.append('(')
                        scanner_token.append(i)
                        continue
                    if i.__contains__(',') and i.__contains__('('):
                        i = i.replace('(', '')
                        i = i.replace(',', '')
                        scanner_token.append('(')
                        scanner_token.append(i)
                        scanner_token.append(',')
                        continue
                    if i.__contains__(','):
                        i, m = i.split(',')
                        scanner_token.append(i)
                        scanner_token.append(",")
                        continue
                    if i.__contains__('('):
                        i = i.replace('(', '')
                        scanner_token.append('(')
                        scanner_token.append(i)
                        continue
                    if i.__contains__('))'):
                        i, m = i.split('))')
                        scanner_token.append(i)
                        scanner_token.append(')')
                        scanner_token.append(')')
                        if m != '':
                            scanner_token.append(m)
                        continue
                    if i.__contains__(')'):
                        i, m = i.split(')')
                        scanner_token.append(i)
                        scanner_token.append(')')
                        if m == ';':
                            scanner_token.append(';')
                        continue
                    if i.__contains__('{') == False and comment == 0:
                        if i.__contains__(';'):
                            i, m = i.split(';')
                            scanner_token.append(i)
                            scanner_token.append(";")
                            continue
                        else:
                            scanner_token.append(i)
                            continue
                    if i.__contains__('{'):
                        comment = 1  # start of comment
                    elif i.__contains__('}'):
                        comment = 0  # end of comment
                index = index + 1  # index of lines
            for i in scanner_token:
                if self.is_reserved(i):
                    scanner_tokenType.append('Reserved')
                elif self.is_sympol(i):
                    scanner_tokenType.append('Symbol')
                else:
                    try:  # check it's number or string
                        x = int(i)
                        scanner_tokenType.append('Number')
                    except:
                        if i[0] == '"':
                            scanner_tokenType.append('String')
                        else:
                            scanner_tokenType.append('Identifier')
            for i in range(scanner_token.__len__()):
                self.tableWidget.setRowCount(i)
                self.tableWidget.insertRow(i)
                self.tableWidget.setItem(i, 0, QTableWidgetItem(scanner_token[i]))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(scanner_tokenType[i]))
            self.parse()
        except:
            print('Error\nplease try to upload file again')
    def parse(self):
        p = Parser(scanner_token, scanner_tokenType)
        p.program()

def main():
    app = QApplication(sys.argv)
    window = Main()
    window.setWindowTitle('Scanner')
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
