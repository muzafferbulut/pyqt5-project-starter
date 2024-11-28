import subprocess

class QtFileManager:

    def __init__(self):
        pass

    def openWithQtDesigner(self, qtDesignerPath, uiPath):
        try:
            subprocess.Popen([qtDesignerPath, uiPath])
        except FileNotFoundError:
            print(f"Qt Designer not found at {qtDesignerPath}. Please check the path.")
        except Exception as e:
            print(f"An error occurred: {e}")


    def setMainWindowProperties(self, uiPath, title, iconPath):
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