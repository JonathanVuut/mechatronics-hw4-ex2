from pathlib import Path
import sys
import csv
import numpy as np

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class IceCreamDataWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.temperatures = []
        self.revenues = []
        self.selected_file = ""

        self.setWindowTitle("Ice Cream Data Visualizer")
        self.resize(900, 650)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        header = QWidget(central_widget)
        header.setObjectName("headerCard")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 16, 20, 16)
        header_layout.setSpacing(4)

        heading = QLabel(
            '<span style="color: #ffc9b8">Ice</span> '
            '<span style="color: #fff0a8">Cream</span> '
            '<span style="color: #bff3dd">Data</span> '
            '<span style="color: #c7e9ff">Visualizer</span>',
            header,
        )
        heading.setObjectName("heading")
        heading.setTextFormat(Qt.TextFormat.RichText)
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(heading)

        subtitle = QLabel("A little sunshine in every data point", header)
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle)
        layout.addWidget(header)

        plot_card = QWidget(central_widget)
        plot_card.setObjectName("plotCard")
        plot_layout = QVBoxLayout(plot_card)
        plot_layout.setContentsMargins(12, 12, 12, 12)
        plot_layout.setSpacing(8)

        self.figure = Figure(facecolor="#ffffff")
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setParent(plot_card)
        self.toolbar = NavigationToolbar2QT(self.canvas, plot_card)
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas, stretch=1)
        layout.addWidget(plot_card, stretch=1)

        actions = QHBoxLayout()
        actions.setSpacing(12)
        self.load_button = QPushButton("Load Data File", central_widget)
        self.load_button.setObjectName("loadButton")
        self.load_button.clicked.connect(self.open_data_file)
        actions.addWidget(self.load_button, stretch=1)

        self.about_button = QPushButton("About", central_widget)
        self.about_button.setObjectName("aboutButton")
        self.about_button.clicked.connect(self.show_about)
        actions.addWidget(self.about_button)
        layout.addLayout(actions)

        self.plot_data()

    def open_data_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Data File",
            "",
            "CSV files (*.csv)",
        )
        if file_path:
            self.selected_file = file_path
            self.read_csv_data()

    def show_about(self) -> None:
        message = QMessageBox(self)
        message.setWindowTitle("About")
        message.setTextFormat(Qt.TextFormat.RichText)
        message.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        message.setText(
            "Name: Jonathan Freedman<br>"
            "Course: Introduction to Mechatronics<br>"
            'GitHub: <a href="https://github.com/JonathanVuut/mechatronics-hw4-ex2">'
            "JonathanVuut/mechatronics-hw4-ex2</a>"
        )
        message.exec()

    def read_csv_data(self) -> None:
        self.temperatures=[]
        self.revenues=[]

        with open(self.selected_file, 'r') as f:
            reader=csv.reader(f)
            next(reader)
            for row in reader:
                if row:
                    self.temperatures.append(float(row[0]))
                    self.revenues.append(float(row[1]))
                    
        self.plot_data()


    def plot_data(self) -> None:
        self.axes.clear()
        self.axes.set_facecolor("#ffffff")
        self.axes.plot(
            [0, 1, 2],
            [0, 1, 0],
            marker="o",
            markersize=8,
            linewidth=2.5,
            color="#f97366",
            markerfacecolor="#fbba74",
            markeredgecolor="#ffffff",
            markeredgewidth=1.5,
        )
        self.axes.set_title("Your sales story starts here", color="#24324b", pad=14)
        self.axes.set_xlabel("X", color="#53627a")
        self.axes.set_ylabel("Y", color="#53627a")
        self.axes.tick_params(colors="#53627a")
        self.axes.grid(True, color="#edf1f7", linewidth=0.8)
        self.axes.set_axisbelow(True)
        for spine in self.axes.spines.values():
            spine.set_color("#e2e8f0")
        self.figure.tight_layout(pad=2)
        self.canvas.draw_idle()


def main() -> None:
    app = QApplication(sys.argv)
    stylesheet = Path(__file__).with_name("style.qss")
    app.setStyleSheet(stylesheet.read_text(encoding="utf-8"))

    window = IceCreamDataWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
