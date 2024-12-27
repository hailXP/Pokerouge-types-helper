import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QColor

class ScreenOverlay(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        self.screen_width = screen_size.width()
        self.screen_height = screen_size.height()
        
        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        
        self.top    = int(0.10 * self.screen_height)
        self.left   = 0
        self.right  = int(0.70 * self.screen_width)
        self.bottom = int(0.65 * self.screen_height)
        
        self.show()
    
    def paintEvent(self, event):
        """
        This is where we do the custom drawing. We draw a rectangle
        on the transparent widget.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        pen = QPen(QColor(0, 255, 0), 2)
        painter.setPen(pen)
        
        
        rect_width = self.right - self.left
        rect_height = self.bottom - self.top
        
        painter.drawRect(self.left, self.top, rect_width, rect_height)
        
    def keyPressEvent(self, event):
        """
        Press 'Esc' to close the overlay.
        """
        if event.key() == Qt.Key_Escape:
            self.close()

def main():
    app = QApplication(sys.argv)
    overlay = ScreenOverlay()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
