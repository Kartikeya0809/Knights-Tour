from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtSvgWidgets import *
from PyQt6.QtGui import *

import sys

class SolverSignals(QObject):
    finished = pyqtSignal(list)

class Solver(QRunnable):
    def __init__(self, m, n, module):
        super().__init__()
        self.m = m
        self.n = n
        self.module = module
        self.signals = SolverSignals()

    @pyqtSlot()
    def run(self):
        import importlib
        path = importlib.import_module(self.module).get_path(self.m, self.n)
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
            for i in range(self.progress - 1):
                painter.drawLine(
                    int(self.square_side * (self.path[i][0] + 0.5)),
                    int(self.square_side * (self.path[i][1] + 0.5)),
                    int(self.square_side * (self.path[i + 1][0] + 0.5)),
                    int(self.square_side * (self.path[i + 1][1] + 0.5)),
                )
        self.update()

    def update_progress(self, progress):
        self.progress = progress


class Chessboard(QMainWindow):
    def __init__(
        self,
        rows,
        cols,
        square_side,
        animation_length,
        board_colors,
        visited_colors,
        line_color,
        line_opacity,
        previous,
        module
    ):
        super().__init__()
        if previous:
            previous.close()
        self.threadpool = QThreadPool()
        self.m = rows
        self.n = cols
        self.cell = None
        self.square_side = square_side
        self.animation_length = animation_length
        self.board_colors = board_colors
        self.visited_colors = visited_colors
        self.line_color = line_color
        self.line_opacity = line_opacity
        self.module = module
        self.setWindowTitle(f"Chessboard ({rows}x{cols})")
        self.setFixedSize(QSize(cols * self.square_side, rows * self.square_side))
        self.progress = 0
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)
        self.squares = {row: dict() for row in range(rows)}
        for i in range(rows):
            for j in range(cols):
                square = QWidget()
                square.setFixedSize(self.square_side, self.square_side)
                square.setStyleSheet(
                    "background-color: " + self.board_colors[(i + j) % 2]
                )
                self.grid.addWidget(square, i + 1, j + 1)
                self.squares[j][i] = square

        board = QWidget()
        board.setLayout(self.grid)
        self.setCentralWidget(board)

    def move_knight(self, i, j, and_then=None):
        point = QPoint(i * self.square_side, j * self.square_side)
        prev_cell = self.cell
        self.cell = (i, j)
        if not prev_cell:
            self.knight = QSvgWidget("images/ndt.svg", self)
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
        self.label = self.label_dark = None
        if darken:
            self.label_dark = QWidget(self)
            self.label_dark.setFixedSize(
                QSize(self.n * self.square_side, self.m * self.square_side)
            )
            self.label_dark.setStyleSheet("background-color: rgba(0, 0, 0, 0.2);")
            self.label_dark.show()
        self.label = QLabel(self)
        self.label.setFixedSize(QSize(self.n * self.square_side, self.m * self.square_side))
        self.label.setText(text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if darken:
            # try:
                # label.destroyed.connect(lambda: self.label_widget and self.label_widget.deleteLater())
            # except:
                pass
        font = QFont()
        font.setBold(True)
        font.setPointSize(50)
        self.label.setFont(font)
        self.label.show()

    def advance(self):
        if self.progress == len(self.path):
            self.mark_visited(self.cell[0], self.cell[1])
            self.show_label("Done")
            return
        cell = self.path[self.progress]
        self.progress += 1
        self.annotation_layer.update_progress(self.progress)
        self.move_knight(cell[0], cell[1], self.advance)

    def mark_visited(self, i, j):
        self.squares[i][j].setStyleSheet(f"background-color: {self.visited_colors[(i+j)%2]}")
        self.squares[i][j].update()
        # marker = QWidget(self)
        # marker.setStyleSheet(f"background-color: {self.visited_colors};")
        # marker.setGeometry(
        #     i * self.square_side,
        #     j * self.square_side,
        #     self.square_side,
        #     self.square_side,
        # )
        # marker.updateGeometry()
        # marker.show()
        # marker.update()

    def showEvent(self, event):
        global module
        super().showEvent(event)
        self.show_label("Finding path...", darken=True)
        solver = Solver(self.m, self.n, self.module)
        solver.signals.finished.connect(self.show_path)
        self.threadpool.start(solver)
    
    def closeEvent(self, event):
        self.threadpool.disconnect()

    def show_path(self, path):
        self.path = path[1:]
        if (
            len(set(self.path)) == self.m * self.n - 1
            and len(self.path) == self.m * self.n - 1
        ):
            self.visited_colors = ["#9ad07c", "#6b9247"]
        else:
            self.visited_colors = ["#ff805c", "d04227"]
        self.destroy_label()
        self.progress = 0
        if self.path:
            self.annotation_layer = AnnotationLayer(
                self,
                self.path,
                self.m,
                self.n,
                self.square_side,
                self.line_color,
                self.line_opacity,
            )
            self.annotation_layer.setFixedSize(
                QSize(self.n * self.square_side, self.m * self.square_side)
            )
            self.annotation_layer.raise_()
            self.annotation_layer.show()
            self.advance()
        else:
            self.show_label("No solution", darken=True)

    def destroy_label(self):
        if self.label:
            self.label.deleteLater()
        if self.label_dark:
            self.label_dark.deleteLater()


class Picker(QMainWindow):
    ALGORITHMS = {
        "Backtracking": {
            "module": "Backtracking",
        },
        "Warnsdorff": {
            "module": "Warnsdorff",
        },
        "Divide and conquer": {"module": "DnC", "fix": {"Columns": "Rows"}},
    }

    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback
        self.setFixedSize(400, 220)
        vlayout = QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)

        algorithm_label = QLabel("Choose an algorithm")
        algorithm_label.setContentsMargins(0, 10, 0, 0)
        font = QFont()
        font.setBold(True)
        font.setPointSize(10)
        algorithm_label.setFont(font)
        vlayout.addWidget(algorithm_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        algorithm_layout = QVBoxLayout()
        algorithm_layout.setContentsMargins(110, 0, 30, 20)
        for algorithm in self.ALGORITHMS:
            button = QRadioButton()
            button.setText(algorithm)
            button.clicked.connect(self.choose_algorithm)
            algorithm_layout.addWidget(button)
        vlayout.addLayout(algorithm_layout)

        size_label = QLabel("Choose board dimensions")
        vlayout.addWidget(size_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        size_label.setFont(font)
        size_layout = QVBoxLayout()
        self.dimension_entries = {}
        for dim in ("Rows", "Columns"):
            sub_layout = QHBoxLayout()
            sub_layout.setContentsMargins(150, 0, 150, 0)
            label = QLabel(dim + ":")
            label.setAlignment(Qt.AlignmentFlag.AlignRight)
            entry = QLineEdit()
            entry.setEnabled(False)
            entry.setMaximumWidth(35)
            entry.textChanged.connect(self.validate_text)
            self.dimension_entries[dim] = entry
            sub_layout.addWidget(label)
            sub_layout.addWidget(entry)
            sub_layout.addSpacing(10)
            size_layout.addLayout(sub_layout)
        vlayout.addLayout(size_layout)

        self.solve_button = QPushButton("Solve")
        self.solve_button.setFont(font)
        self.solve_button.setEnabled(False)
        self.solve_button.clicked.connect(self.solve)
        vlayout.addWidget(self.solve_button, Qt.AlignmentFlag.AlignHCenter)

        base = QWidget()
        base.setLayout(vlayout)
        self.setCentralWidget(base)

    def choose_algorithm(self, event):
        option = self.ALGORITHMS[self.sender().text()]
        self.algorithm = option["module"]
        for dimension, entry in self.dimension_entries.items():
            try:
                entry.textEdited.disconnect()
            except:
                pass
            if "fix" in option and dimension in option["fix"]:
                entry.setEnabled(False)
                source = self.dimension_entries[option["fix"][dimension]]
                if source.text():
                    entry.setText(source.text())
                else:
                    source.setText(entry.text())
                source.textEdited.connect(self.create_follower(entry))
            else:
                entry.setEnabled(True)

    def create_follower(self, source):
        def follow(event):
            source.setText(self.sender().text())

        return follow

    def validate_text(self, event):
        self.solve_button.setEnabled(
            all(
                entry.text().isdigit() and int(entry.text()) > 0
                for entry in self.dimension_entries.values()
            )
        )

    def solve(self, event):
        self.rows = int(self.dimension_entries["Rows"].text())
        self.cols = int(self.dimension_entries["Columns"].text())
        self.callback(*self.get_values(), self)

    def get_values(self):
        return self.cols, self.rows, self.algorithm


SQUARE_SIZE = 75
MOVE_DURATION = 1
BOARD_COLORS = ["#ffd599", "#b16e41"]
VISITED_COLORS = ["#9ad07c", "#6b9247"]
# VISITED_COLOR = "rgba(255, 0, 0, 0.4)"
LINE_COLOR = "rgb(0, 0, 0)"
LINE_OPACITY = 0.3

get_path = None
board = None


def create_board(m, n, module, previous=None):
    global board
    global SQUARE_SIZE, MOVE_DURATION, BOARD_COLORS, VISITED_COLOR, LINE_COLOR, LINE_OPACITY
    global get_path
    # get_path = importlib.import_module(module).get_path
    screensize = QApplication.instance().primaryScreen().availableGeometry()
    screensize = (screensize.width(), screensize.height())
    while SQUARE_SIZE * n >= screensize[1] - 300 and SQUARE_SIZE >= 5:
        SQUARE_SIZE -= 1
    while SQUARE_SIZE * m >= screensize[0] - 300 and SQUARE_SIZE >= 5:
        SQUARE_SIZE -= 1
    # print(SQUARE_SIZE)
    board = Chessboard(
        m,
        n,
        square_side=SQUARE_SIZE,
        animation_length=MOVE_DURATION,
        board_colors=BOARD_COLORS,
        visited_colors=VISITED_COLORS,
        line_color=LINE_COLOR,
        line_opacity=LINE_OPACITY,
        previous=previous,
        module=module
    )
    board.setWindowIcon(QIcon("images/ndt.svg"))
    board.setWindowTitle("Knight's tour | Solver")
    board.move_knight(0, 0)
    board.show()


args = sys.argv
if len(args) != 1 and len(args) != 4:
    print(f"Usage: {args[0]} <rows> <cols> <algorithm_module>")
    exit(1)
elif len(args) == 1:
    app = QApplication([])
    picker = Picker(create_board)
    picker.setWindowIcon(QIcon("images/ndt.svg"))
    picker.setWindowTitle("Knight's tour | Generator")
    picker.show()
    # print("Done")
    # app.exec()
    # m, n, module = picker.get_values()
else:
    app = QApplication([])
    m = int(args[1])
    n = int(args[2])
    # print(m, n)
    module = args[3]
    create_board(m, n, module)
app.exec()