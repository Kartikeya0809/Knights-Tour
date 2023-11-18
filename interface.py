from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QGridLayout, QLabel
from PyQt6.QtCore import QSize, QPoint, QPropertyAnimation, QEasingCurve, Qt, QRunnable, QThreadPool, pyqtSlot, QObject, pyqtSignal
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtGui import QFont, QPainter, QColor
from Backtracking import get_path
from Warnsdorff import warnsdorff_path
from DnC import divide_and_conquer
import ctypes

class SolverSignals(QObject):
    finished = pyqtSignal(list)

class Solver(QRunnable):
    def __init__(self, m, n):
        super().__init__()
        self.m = m
        self.n = n
        self.signals = SolverSignals()

    @pyqtSlot()
    def run(self):
        # path = get_path(m, n)
        # path = warnsdorff_path(m, n)
        path = divide_and_conquer(n)
        # print(path)
        self.signals.finished.emit(path)

class AnnotationLayer(QWidget):
    def __init__(self, parent, path, rows, cols, square_side, color, opacity):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.square_side = square_side
        self.color = color
        self.path = path
        self.progress = 0
        self.opacity = opacity
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(self.opacity)
        painter.setPen(QColor(self.color))
        if self.progress != 0:
            painter.drawLine(
                int(self.square_side * 0.5),
                int(self.square_side * 0.5),
                int(self.square_side * (self.path[0][0] + 0.5)),
                int(self.square_side * (self.path[0][1] + 0.5)),
            )
            for i in range(self.progress-1):
                painter.drawLine(
                    int(self.square_side * (self.path[i][0] + 0.5)),
                    int(self.square_side * (self.path[i][1] + 0.5)),
                    int(self.square_side * (self.path[i+1][0] + 0.5)),
                    int(self.square_side * (self.path[i+1][1] + 0.5))
                )
        self.update()

    def update_progress(self, progress):
        self.progress = progress

class Chessboard(QMainWindow):
    def __init__(self, rows, cols, square_side, animation_length, board_colors, visited_color, line_color, line_opacity):
        super().__init__()
        self.threadpool = QThreadPool()
        self.m = rows
        self.n = cols
        self.cell = None
        self.square_side = square_side
        self.animation_length = animation_length
        self.board_colors = board_colors
        self.visited_color = visited_color
        self.line_color = line_color
        self.line_opacity = line_opacity
        self.setWindowTitle(f"Chessboard ({rows}x{cols})")
        self.setFixedSize(QSize(cols*self.square_side, rows*self.square_side))
        self.progress = 0
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)
        for i in range(rows):
            for j in range(cols):
                square = QWidget()
                square.setFixedSize(self.square_side, self.square_side)
                square.setStyleSheet("background-color: " + self.board_colors[(i+j) % 2])
                self.grid.addWidget(square, i+1, j+1)

        board = QWidget()
        board.setLayout(self.grid)
        self.setCentralWidget(board)
    
    def move_knight(self, i, j, and_then=None):
        point = QPoint(i*self.square_side, j*self.square_side)
        prev_cell = self.cell
        self.cell = (i, j)
        if not prev_cell:
            self.knight = QSvgWidget('images/ndt.svg', self)
            self.knight.setFixedSize(QSize(self.square_side, self.square_side))
            self.knight.move(point)
            if and_then:
                and_then()
                return
        else:
            self.mark_visited(prev_cell[0], prev_cell[1])
            self.animation = QPropertyAnimation(self.knight, b"pos")
            self.animation.setDuration(self.animation_length)
            self.animation.setEndValue(point)
            self.animation.setEasingCurve(QEasingCurve(QEasingCurve.Type.OutExpo))
            if and_then:
                self.animation.finished.connect(and_then)
            self.animation.start()
    
    def show_label(self, text, darken=False):
        if darken:
            self.label_widget = QWidget(self)
            self.label_widget.setFixedSize(QSize(self.n*self.square_side, self.m*self.square_side))
            self.label_widget.setStyleSheet("background-color: rgba(0, 0, 0, 0.2);")
            self.label_widget.show()
        label = QLabel(self)
        label.setFixedSize(QSize(self.n*self.square_side, self.m*self.square_side))
        label.setText(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if darken:
            try:
                label.destroyed.connect(lambda: self.label_widget.deleteLater())
            except:
                pass
        font = QFont()
        font.setBold(True)
        font.setPointSize(50)
        label.setFont(font)
        label.show()
        return label
    
    def advance(self):
        if (self.progress == len(self.path)):
            self.mark_visited(self.cell[0], self.cell[1])
            self.show_label("Done")
            return
        cell = self.path[self.progress]
        # print(cell)
        self.progress += 1
        self.annotation_layer.update_progress(self.progress)
        self.move_knight(cell[0], cell[1], self.advance)
    
    def mark_visited(self, i, j):
        marker = QWidget(self)
        marker.setStyleSheet(f'background-color: {self.visited_color};')
        marker.setGeometry(i*self.square_side, j*self.square_side, self.square_side, self.square_side)
        marker.updateGeometry()
        marker.show()
        marker.update()
    
    def showEvent(self, event):
        super().showEvent(event)
        self.label = self.show_label("Finding path...", darken=True)
        solver = Solver(self.m, self.n)
        solver.signals.finished.connect(self.show_path)
        self.threadpool.start(solver)
    
    def show_path(self, path):
        self.path = path[1:]
        if len(set(self.path)) == self.m * self.n - 1 and len(self.path) == self.m * self.n - 1:
            self.visited_color = 'rgba(2, 201, 81, 0.4)'
        self.label.deleteLater()
        self.progress = 0
        if self.path:
            self.annotation_layer = AnnotationLayer(self, self.path, self.m, self.n, self.square_side, self.line_color, self.line_opacity)
            self.annotation_layer.setFixedSize(QSize(self.n*self.square_side, self.m*self.square_side))
            self.annotation_layer.raise_()
            self.annotation_layer.show()
            self.advance()
        else:
            self.show_label("No solution", darken=True)


app = QApplication([])
m, n = 23, 23
SQUARE_SIZE = 75
MOVE_DURATION = 10
BOARD_COLORS = ['#ffd599','#b16e41']
VISITED_COLOR = 'rgba(255, 0, 0, 0.4)'
LINE_COLOR = 'rgb(0, 0, 0)'
LINE_OPACITY = 0.5

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
while SQUARE_SIZE * n >= screensize[1] - 300 and SQUARE_SIZE >= 5:
    SQUARE_SIZE -= 1
while SQUARE_SIZE * m >= screensize[0] - 300 and SQUARE_SIZE >= 5:
    SQUARE_SIZE -= 1

board = Chessboard(n, m, square_side=SQUARE_SIZE, animation_length=MOVE_DURATION, board_colors=BOARD_COLORS, visited_color=VISITED_COLOR, line_color=LINE_COLOR, line_opacity=LINE_OPACITY)
board.move_knight(0, 0)
board.show()
app.exec()