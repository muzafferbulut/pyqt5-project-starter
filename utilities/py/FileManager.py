from PyQt5.QtWidgets import QFileDialog
import shutil
import os

class FileManager:
    
    def __init__(self):
        pass

    @staticmethod
    def selectDirectory():
            directory = QFileDialog.getExistingDirectory(None, "Projenin oluşturulacağı dizini seçiniz.")
            if directory:
                return directory
            else:
                return False

    @staticmethod
    def selectFile(extension):
        file_path, _ = QFileDialog.getOpenFileName(None, "Lütfen dosya seçiniz", "", f"{extension} Files (*.{extension});;All Files (*)")
        if file_path:
            return file_path
        else:
            return False

    @staticmethod
    def deleteFile(filepath):
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            return f"Dosya silinemedi: {e}"

    @staticmethod
    def copyFile(fromPath, toPath):
        try:
            shutil.copy2(fromPath, toPath)
        except Exception as e:
            return f"Dosya kopyalanamadı: {e}"

    @staticmethod
    def moveFile(fromPath, toPath):
        try:
            shutil.move(fromPath, toPath)
        except Exception as e:
            return f"Dosya taşınamadı: {e}"

    @staticmethod
    def rename(file, newName):
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

    @staticmethod
    def createProjectFolder(directory, folderName):
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