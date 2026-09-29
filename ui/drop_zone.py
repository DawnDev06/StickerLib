from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, Signal

class DropZone(QWidget):
    files_dropped = Signal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        
        layout = QVBoxLayout()
        self.label = QLabel("Resimleri Buraya Sürükleyin\n(Toplu ekleme yapabilirsiniz)")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                font-size: 16px;
                color: #666;
                background-color: #f9f9f9;
            }
        """)
        
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setMinimumHeight(200)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.label.setStyleSheet("""
                QLabel {
                    border: 2px dashed #4CAF50;
                    border-radius: 10px;
                    font-size: 16px;
                    color: #4CAF50;
                    background-color: #e8f5e9;
                }
            """)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        # Fare alandan çıkınca stili sıfırla
        self.label.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                font-size: 16px;
                color: #666;
                background-color: #f9f9f9;
            }
        """)

    def dropEvent(self, event):
        self.dragLeaveEvent(event)
        urls = event.mimeData().urls()
        
        # Sadece desteklenen dosya türlerini filtrele
        file_paths = []
        for url in urls:
            if url.isLocalFile():
                path = url.toLocalFile()
                if path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    file_paths.append(path)
        
        if file_paths:
            self.files_dropped.emit(file_paths)