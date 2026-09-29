from PySide6.QtWidgets import QWidget, QGridLayout, QScrollArea, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

class StickerGrid(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        
        # İçeriği tutacak ana widget ve layout
        self.content_widget = QWidget()
        self.grid_layout = QGridLayout(self.content_widget)
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        self.setWidget(self.content_widget)
        self.cards = []

    def update_grid(self, stickers):
        # Önce mevcut kartları temizle
        for card in self.cards:
            card.setParent(None)
        self.cards.clear()

        row, col = 0, 0
        max_cols = 4  # Yan yana kaç tane sticker görüneceği

        for sticker in stickers:
            card = StickerCard(sticker)
            self.grid_layout.addWidget(card, row, col)
            self.cards.append(card)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

class StickerCard(QWidget):
    def __init__(self, sticker):
        super().__init__()
        self.sticker = sticker
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Görsel önizlemesi için QLabel
        self.image_label = QLabel()
        self.image_label.setFixedSize(100, 100)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                border: 1px solid #ccc;
                border-radius: 8px;
                background-color: #fff;
            }
        """)
        
        # Önizleme yükleme
        self.load_thumbnail()
        
        # Dosya adı etiketi
        name = sticker.filename
        if len(name) > 12:
            name = name[:9] + "..."
        self.name_label = QLabel(name)
        self.name_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.image_label)
        layout.addWidget(self.name_label)
        self.setLayout(layout)

    def load_thumbnail(self):
        path = self.sticker.processed_path if self.sticker.is_processed else self.sticker.original_path
        if path:
            pixmap = QPixmap(path)
            scaled_pixmap = pixmap.scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)