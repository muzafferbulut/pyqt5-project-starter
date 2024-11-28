from PyQt5.QtWidgets import QFileDialog
import shutil
import os

class FileManager:
    
    def __init__(self):
        pass

    def selectDirectory(self):
            directory = QFileDialog.getExistingDirectory(None, "Projenin oluşturulacağı dizini seçiniz.")
            if directory:
                return directory
            else:
                return False

    def selectFile(self, extension):
        file_path, _ = QFileDialog.getOpenFileName(None, "Lütfen dosya seçiniz", "", f"{extension} Files (*.{extension});;All Files (*)")
        if file_path:
            return file_path
        else:
            return False

    def deleteFile(self, filepath):
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            return e

    def copyFile(self, fromPath, toPath):
        try:
            shutil.copy2(fromPath, toPath)
        except Exception as e:
            return e

    def moveFile(self, fromPath, toPath):
        try:
            shutil.move(fromPath, toPath)
        except Exception as e:
            return e

    def rename(self, file, newName):
        try:
            directory = os.path.dirname(file)
            newPath = os.path.join(directory, newName)
            
            os.rename(file, newPath)
        except FileNotFoundError:
            print(f"'{file}' bulunamadı. Ad değiştirme başarısız.")
            raise
        except PermissionError:
            print(f"'{file}' için izin hatası. Ad değiştirme başarısız.")
            raise
        except Exception as e:
            print(f"Beklenmeyen bir hata oluştu: {e}")
            raise

    def createProjectFolder(self, directory, folderName):
        folderPath = os.path.join(directory, folderName)
        imgPath = os.path.join(folderPath, "img")
        uiPath = os.path.join(folderPath, "ui")
        try:
            if not os.path.exists(folderPath):
                os.makedirs(folderPath)
                os.makedirs(imgPath)
                os.makedirs(uiPath)
        except Exception as e:
            print(f"{e}")