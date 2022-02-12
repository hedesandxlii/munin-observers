from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget

import munin as mn


class ButtonModel(mn.ObservableMixin):
    def __init__(self):
        super().__init__()
        self.number_of_presses: int = 0

    @mn.notify
    def increase(self):
        self.number_of_presses += 1


class PushButton(QPushButton):  # implements the Observer[ButtonModel]-Protocol
    def __init__(self, text: str, parent: QWidget, model: ButtonModel):
        super().__init__(text, parent)

        model.add_observer(self)
        self.clicked.connect(model.increase)

    def update(self, observable: ButtonModel):
        self.setText(str(observable.number_of_presses))


class MainWindow(QMainWindow):
    def __init__(self, model: ButtonModel):
        super().__init__()

        self.setWindowTitle("My App")
        self.button = PushButton("Press me!", self, model)
        self.setFixedSize(400, 300)
        self.setCentralWidget(self.button)


def main():
    app = QApplication([])

    model = ButtonModel()
    window = MainWindow(model)
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
