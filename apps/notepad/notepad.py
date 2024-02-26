from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog
from PyQt5.QtCore import Qt
import sys
import os

class Notepad(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.width = 752
        self.height = 526
        self.x = 593
        self.y = 289
        self.initialize_ui()

    def initialize_ui(self):
        self.setWindowTitle("Untitled - Notepad")
        self.setGeometry(self.x, self.y, self.width, self.height)

        # Disable the title bar (minimize, maximize, close window)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint) 


        # Create text area
        self.text_area = QTextEdit()
        self.setCentralWidget(self.text_area)

        # Create menu bar
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')

        new_action = QAction('New', self)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu('Edit')

        cut_action = QAction('Cut', self)
        cut_action.triggered.connect(self.text_area.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction('Copy', self)
        copy_action.triggered.connect(self.text_area.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction('Paste', self)
        paste_action.triggered.connect(self.text_area.paste)
        edit_menu.addAction(paste_action)

    def new_file(self):
        self.setWindowTitle("Untitled - Notepad")
        self.text_area.clear()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*.*);;Text Documents (*.txt)')
        if file_path:
            with open(file_path, 'r') as file:
                self.setWindowTitle(os.path.basename(file_path) + " - Notepad")
                self.text_area.setText(file.read())

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'All Files (*.*);;Text Documents (*.txt)')
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.toPlainText())
                self.setWindowTitle(os.path.basename(file_path) + " - Notepad")

    # Capture the notepad closing event and perform an action
    def closeEvent(self, event):
        for window in self.parent().open_windows:
            if window.name == 'Notepad':
                self.parent().remove_app_action(app_name=window.name)
                self.parent().open_windows.remove(window)
    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    notepad = Notepad()
    notepad.show()
    sys.exit(app.exec_())
