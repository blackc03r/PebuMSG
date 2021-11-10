import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
app = QApplication(sys.argv)
window  = QWidget()
window.setWindowTitle('PebuMSG Desktop Client')
window.setGeometry(100,100,280,80)
window.move(60,15)
loginMsg = QLabel("<h1/>PebuMSG</h1>",parent=window)
loginMsg.move(60,15)
window.show()
