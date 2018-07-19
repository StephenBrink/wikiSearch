import sys, io, urllib3, certifi, re
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from bs4 import BeautifulSoup

class App(QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = 'Wiki Search'
        
        self.bName = QLabel()
        self.bName.setFont(QFont("Arial", 28))
        self.bDescription = QLabel()
        self.bDescription.setFont(QFont("Arial", 12))
        self.bDescription.setWordWrap(True);
        self.left = 20
        self.top = 20
        self.width = 750
        self.height = 250
        
        self.initUI()
        
    def getCode(self):
        text, okPressed = QInputDialog.getText(self, "Wiki Search","Enter the word:", QLineEdit.Normal, "")
        if okPressed and text != '':
            self.word = text
        
    def webScrape(self):
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())
        response = http.request('GET', 'https://en.wikipedia.org/wiki/' + self.word)
        soup = BeautifulSoup(response.data, 'html.parser')

        title_box = soup.find('h1',{'id': 'firstHeading'})
        title = title_box.text.strip()
        
        description_box = soup.find('div',{'class': 'mw-parser-output'}).find_all('p')
        for ps in description_box:
            if ps.find(text=re.compile(self.word)):
                description_box = ps
                break
        description = description_box.text.strip()
            
        self.bName.setText(title)
        self.bDescription.setText(description)
        print(title)
        print(description)
        
    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(self.bName)
        layout.addWidget(self.bDescription)
        self.setLayout(layout)
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.getCode()
        self.webScrape()
        
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    