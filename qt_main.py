
from PyQt4 import QtCore, QtGui
from ui_test import Ui_Form
import sys
class Ui(QtGui.QWidget):
	def __init__(self, parent=None):
		super(Ui, self).__init__(parent)
		self.ui = Ui_Form()
		self.ui.setupUi(self)

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = Ui()
	window.show()
	sys.exit(app.exec_())