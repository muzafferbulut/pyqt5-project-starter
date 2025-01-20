import subprocess
from PyQt5.QtWidgets import QMessageBox

class GitManager:

    def __init__(self):
        pass

    @staticmethod
    def createARepository(directory):
        try:
            subprocess.run(['git', 'init', directory], check=True)
        except subprocess.CalledProcessError as e:
            return f"An error occurred: {e}"