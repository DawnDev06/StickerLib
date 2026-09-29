import sys
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from config.settings import OUTPUT_DIR

def ensure_directories():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def main():
    ensure_directories()
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion") 
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()