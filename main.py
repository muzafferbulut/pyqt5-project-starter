from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from utilities.py.PythonFileManager import PythonFileManager
from utilities.py.QtFileManager import QtFileManager
from utilities.py.FileManager import FileManager
from utilities.py.GitManager import GitManager
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from PyQt5.uic import loadUi
import json
import sys
import os

class PyqtProjectGenerator(QMainWindow):

    def __init__(self):
        super(PyqtProjectGenerator, self).__init__()
        loadUi("utilities/ui/pyqt_project_generator.ui", self)

        self.fileManager = FileManager()
        self.gitManager = GitManager()
        self.qtManager = QtFileManager()
        self.pyManager = PythonFileManager()

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
        self.fileManager.rename(f"{os.path.join(self.projectDirectory, self.projectName)}/img/{self.mainWindowIconPath.split("/")[-1]}", f"{self.projectName.lower()}_icon.png")

        # set paths
        self.mainWindowIconPath = f"{os.path.join(self.projectDirectory, self.projectName)}/img/{self.projectName}_icon.png"
        self.uiPath = f"{os.path.join(self.projectDirectory, self.projectName)}/ui/{self.projectName.lower()}.ui"
        
        # generate file
        self.qtManager.setMainWindowProperties(self.uiPath, self.mainWindowTitle, self.mainWindowIconPath)
        self.pyManager.generateMainPy(self.projectName, os.path.join(self.projectDirectory, self.projectName))

        if self.addFileManagerCheck.isChecked():
            self.fileManager.copyFile("utilities/py/FileManager.py", f"{os.path.join(self.projectDirectory, self.projectName)}/")
        
        if self.addDatabaseManagerCheck.isChecked():
            self.fileManager.copyFile("utilities/py/DatabaseManager.py", f"{os.path.join(self.projectDirectory, self.projectName)}/")

        if self.createGitRepo.isChecked():
            self.gitManager.createARepository()

        if self.createFirstCommit.isChecked():
            self.gitManager.createFirstCommit("Initial commit with pyqt5 project starter.")

        if self.addDefaultGitignoreFile.isChecked():
            self.fileManager.copyFile("files/.gitignore", f"{os.path.join(self.projectDirectory, self.projectName)}/")

        if self.addLicense.isChecked():
            self.fileManager.copyFile("files/LICENSE", f"{os.path.join(self.projectDirectory, self.projectName)}/")

        if self.editWithQtDesignerCheck.isChecked():
            with open("utilities/files/paths.json", "r") as file:
                data = json.load(file)
            self.qtManager.openWithQtDesigner(data["qt_designer_path"])

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