import subprocess
from PyQt5.QtWidgets import QMessageBox

class GitManager:

    def __init__(self):
        pass

    def createARepository(self, directory):
        try:
            subprocess.run(['git', 'init', directory], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")