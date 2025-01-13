import os

class PythonFileManager:

    def __init__(self):
        pass

    def generateMainPy(self, projectName,directory):
        script = f"""from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
import sys
import os

class {projectName}(QMainWindow):

    def __init__(self):
        super({projectName}, self).__init__()
        loadUi("ui/{projectName.lower()}.ui", self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    project = {projectName}()
    project.show()
    sys.exit(app.exec_())
"""
        mainFile = os.path.join(directory, "main.py")  # Corrected line

        with open(mainFile, "w") as file:
            file.write(script)