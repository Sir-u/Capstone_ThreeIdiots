import sys
from PyQt5.QtWidgets import *

class Main(QDialog):
   def __init__(self):
      super().__init__()
      self.init_ui()
   
   def init_ui(self):
      main_layout = QVBoxLayout()

      layout_sample = QHBoxLayout()

      main_layout.addWidget(layout_sample)

      self.setLayout(main_layout)
      self.show()

if __name__ == '__main__':
   app = QApplication(sys.argv)
   main = Main()
   sys.exit(app.exec_())