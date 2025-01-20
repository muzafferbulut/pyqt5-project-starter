import subprocess

class QtFileManager:

    def __init__(self):
        pass

    @staticmethod
    def openWithQtDesigner(qtDesignerPath, uiPath):
        try:
            subprocess.run([qtDesignerPath, uiPath], check=True)
        except subprocess.CalledProcessError as e:
            return f"Error opening {uiPath} with Qt Designer: {e}"
    
    @staticmethod
    def setMainWindowProperties(uiPath, title, iconPath):
        try:
            with open(uiPath, "r", encoding="utf-8") as file:
                lines = file.readlines()
            if len(lines) >= 14:
                lines[13] = f'    <string>{title}</string>\n'
            if len(lines) >= 18:
                lines[17] = f'    <normaloff>{iconPath}</normaloff>{iconPath}\n'
            with open(uiPath, "w", encoding="utf-8") as file:
                file.writelines(lines)

        except Exception as e:
            print(f"Hata oluştu: {e}")