from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from utilities.py.FileManager import FileManager
from utilities.py.GitManager import GitManager
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from PyQt5.uic import loadUi
import sys
import os

class PyqtProjectGenerator(QMainWindow):

    def __init__(self):
        super(PyqtProjectGenerator, self).__init__()
        loadUi("utilities/ui/pyqt_project_generator.ui", self)

        self.fileManager = FileManager()
        self.gitManager = GitManager()

        self.selectProjectDirectoryButton.clicked.connect(self.selectProjectDirectory)
        self.selectMainWindowIconButton.clicked.connect(self.selectMainWindowIcon)
        self.generateProjectButton.clicked.connect(self.generateProject)
        validator = QRegExpValidator(QRegExp("^[A-Za-z]*$"), self.projectNameLineEdit)
        self.projectNameLineEdit.setValidator(validator)

    def generateProject(self):
        self.projectDirectory = self.projectDirectoryLineEdit.text()
        self.projectName = self.projectNameLineEdit.text()
        self.mainWindowIconPath = self.windowIconLineEdit.text()
        self.mainWindowTitle = self.windowTitleLineEdit.text()

        self.fileManager.createProjectFolder(self.projectDirectory, self.projectName)

        # ui file
        self.fileManager.copyFile("utilities/ui/sample.ui", f"{os.path.join(self.projectDirectory, self.projectName)}/ui/")
        self.fileManager.rename(f"{os.path.join(self.projectDirectory, self.projectName)}/ui/sample.ui", f"{self.projectName}.ui")

        # icon file
        self.fileManager.copyFile(self.mainWindowIconPath, f"{os.path.join(self.projectDirectory, self.projectName)}/img/")
        self.fileManager.rename(f"{os.path.join(self.projectDirectory, self.projectName)}/img/{self.mainWindowIconPath.split("/")[-1]}", f"{self.projectName}_icon.png")

        # set paths
        self.mainWindowIconPath = f"{os.path.join(self.projectDirectory, self.projectName)}/img/{self.projectName}_icon.png"
        self.uiPath = f"{os.path.join(self.projectDirectory, self.projectName)}/ui/{self.projectName}.ui"
        
        # generate file
        self.fileManager.setMainWindowProperties(self.uiPath, self.mainWindowTitle, self.mainWindowIconPath)
        self.fileManager.generateMainPy(self.projectName, self.uiPath, os.path.join(self.projectDirectory, self.projectName))


        QMessageBox.information(self, "Info", "The process was successfull!")

    def selectMainWindowIcon(self):
        try:
            self.windowIconPath = self.fileManager.selectFile("PNG")
            self.windowIconLineEdit.setText(self.windowIconPath)
        except Exception as e:
            QMessageBox.warning(self, "Uyarı", "Lütfen ikon dosyasını seçtiğinizden emin olun!")

    def selectProjectDirectory(self):
        try:
            self.projectDirectory = self.fileManager.selectDirectory()
            self.projectDirectoryLineEdit.setText(self.projectDirectory)
        except Exception as e:
            QMessageBox.warning(self, "Uyarı", "Dizin seçilemedi!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    report = PyqtProjectGenerator()
    report.show()
    sys.exit(app.exec_())