from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from utilities.py.PythonFileManager import PythonFileManager
from utilities.py.QtFileManager import QtFileManager
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

        self.selectProjectDirectoryButton.clicked.connect(self.selectProjectDirectory)
        self.selectMainWindowIconButton.clicked.connect(self.selectMainWindowIcon)
        self.generateProjectButton.clicked.connect(self.generateProject)
        validator = QRegExpValidator(QRegExp("^[A-Za-z]*$"), self.projectNameLineEdit)
        self.projectNameLineEdit.setValidator(validator)
        self.qtDesignerPath = "C:\\Program Files\\QGIS 3.34.0\\apps\\qt5\\bin\\designer.exe"

    def generateProject(self):
        self.projectDirectory = self.projectDirectoryLineEdit.text()
        self.projectName = self.projectNameLineEdit.text()
        self.mainWindowIconPath = self.windowIconLineEdit.text()
        self.mainWindowTitle = self.windowTitleLineEdit.text()

        FileManager.createProjectFolder(self.projectDirectory, self.projectName)

        # ui file
        FileManager.copyFile("utilities/ui/sample.ui", f"{os.path.join(self.projectDirectory, self.projectName)}/ui/")
        FileManager.rename(f"{os.path.join(self.projectDirectory, self.projectName)}/ui/sample.ui", f"{self.projectName.lower()}.ui")

        # icon file
        FileManager.copyFile(self.mainWindowIconPath, f"{os.path.join(self.projectDirectory, self.projectName)}/img/")
        FileManager.rename(f"{os.path.join(self.projectDirectory, self.projectName)}/img/{self.mainWindowIconPath.split("/")[-1]}", f"{self.projectName.lower()}_icon.png")

        # set paths
        self.mainWindowIconPath = f"{os.path.join(self.projectDirectory, self.projectName)}/img/{self.projectName}_icon.png"
        self.uiPath = f"{os.path.join(self.projectDirectory, self.projectName)}/ui/{self.projectName.lower()}.ui"
        
        # open with qt designer
        QtFileManager.setMainWindowProperties(self.uiPath, self.mainWindowTitle, self.mainWindowIconPath)
        PythonFileManager.generateMainPy(self.projectName, os.path.join(self.projectDirectory, self.projectName))

        if self.addFileManagerCheck.isChecked():
            FileManager.copyFile("utilities/py/FileManager.py", f"{os.path.join(self.projectDirectory, self.projectName)}/")
        
        if self.addDatabaseManagerCheck.isChecked():
            FileManager.copyFile("utilities/py/DatabaseManager.py", f"{os.path.join(self.projectDirectory, self.projectName)}/")

        if self.createGitRepo.isChecked():
            GitManager.createARepository(self.projectDirectory)
        
        if self.editWithQtDesignerCheck.isChecked():
            QtFileManager.openWithQtDesigner(self.qtDesignerPath, self.uiPath)

        print(f"The {self.projectName} project is being launched.")

    def selectMainWindowIcon(self):
        try:
            self.windowIconPath = FileManager.selectFile("PNG")
            self.windowIconLineEdit.setText(self.windowIconPath)
        except Exception as e:
            QMessageBox.warning(self, "Uyarı", "Lütfen ikon dosyasını seçtiğinizden emin olun!")

    def selectProjectDirectory(self):
        try:
            self.projectDirectory = FileManager.selectDirectory()
            self.projectDirectoryLineEdit.setText(self.projectDirectory)
        except Exception as e:
            QMessageBox.warning(self, "Uyarı", "Dizin seçilemedi!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    report = PyqtProjectGenerator()
    report.show()
    sys.exit(app.exec_())