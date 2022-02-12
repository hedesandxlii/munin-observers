from munin import ObservableMixin, discretion, notify
from PySide6.QtWidgets import QApplication, QLineEdit


class TextModel(ObservableMixin):
    """
    A model that does not like lower-case letters.
    """
    def __init__(self):
        super().__init__()
        self.text: str = ""

    @notify
    def set_text(self, new_text):
        self.text = new_text.upper()

    def get_text(self):
        return self.text


class LineEdit(QLineEdit):  # implements Observer[TextModel]
    def __init__(self):
        super().__init__()

    def act(self, observable: TextModel):
        print("LineEdit is setting text")
        with discretion:
            self.setText(observable.get_text())


def main():
    app = QApplication()
    model = TextModel()

    root = LineEdit()
    model.add_observer(root)
    root.textChanged.connect(model.set_text)
    root.setFixedSize(200, 50)

    root.show()
    app.exec()

if __name__ == "__main__":
    main()
