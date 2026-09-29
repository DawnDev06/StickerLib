from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt
from ui.drop_zone import DropZone
from ui.sticker_grid import StickerGrid
from services.pack_service import PackService
from core.exporter import PackExporter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Instagram Sticker Manager")
        self.resize(900, 700)
        
        # Servis katmanını başlat
        self.pack_service = PackService(pack_name="MyInstagramStickers")
        
        # Merkez widget ve ana layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 1. Üst kısım: Sürükle-bırak alanı
        self.drop_zone = DropZone()
        self.drop_zone.files_dropped.connect(self.handle_dropped_files)
        main_layout.addWidget(self.drop_zone)
        
        # 2. Orta kısım: Sticker önizleme grid alanı
        self.sticker_grid = StickerGrid()
        main_layout.addWidget(self.sticker_grid)
        
        # 3. Alt kısım: İlerleme çubuğu (Progress bar) ve Kontrol butonları
        bottom_layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.hide()  # Başlangıçta gizli
        bottom_layout.addWidget(self.progress_bar)
        
        btn_layout = QHBoxLayout()
        
        self.status_label = QLabel("Durum: Bekleniyor (0 dosya)")
        
        self.process_btn = QPushButton("Sticker Paketini İşle")
        self.process_btn.setEnabled(False)
        self.process_btn.setMinimumHeight(40)
        self.process_btn.clicked.connect(self.process_stickers)
        
        self.export_btn = QPushButton("Dışa Aktar (Export)")
        self.export_btn.setEnabled(False)
        self.export_btn.setMinimumHeight(40)
        self.export_btn.clicked.connect(self.export_pack)
        
        btn_layout.addWidget(self.status_label, stretch=2)
        btn_layout.addWidget(self.process_btn, stretch=1)
        btn_layout.addWidget(self.export_btn, stretch=1)
        
        bottom_layout.addLayout(btn_layout)
        main_layout.addLayout(bottom_layout)

    def handle_dropped_files(self, file_paths):
        # Servis üzerinden dosyaları ekle
        added = self.pack_service.add_files(file_paths)
        if added:
            total_count = len(self.pack_service.pack.stickers)
            self.status_label.setText(f"Durum: {total_count} dosya yüklendi.")
            self.process_btn.setEnabled(True)
            
            # Grid alanını güncelle
            self.sticker_grid.update_grid(self.pack_service.pack.stickers)

    def process_stickers(self):
        total = len(self.pack_service.pack.stickers)
        if total == 0:
            return
            
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(total)
        self.progress_bar.show()
        self.process_btn.setEnabled(False)
        self.drop_zone.setEnabled(False)
        
        def update_progress(current, total):
            self.progress_bar.setValue(current)
            self.status_label.setText(f"İşleniyor: {current}/{total} sticker...")

        # Sticker'ları işle
        self.pack_service.process_all_stickers(progress_callback=update_progress)
        
        # Görsel önizlemelerini yenilenen (işlenmiş) halleriyle güncelle
        self.sticker_grid.update_grid(self.pack_service.pack.stickers)
        
        self.progress_bar.hide()
        self.status_label.setText("Durum: İşlem tamamlandı! Dışa aktarabilirsiniz.")
        self.export_btn.setEnabled(True)
        self.process_btn.setEnabled(True)
        self.drop_zone.setEnabled(True)

    def export_pack(self):
        try:
            target_dir, exported_files = PackExporter.export_to_folder(self.pack_service.pack)
            QMessageBox.information(
                self, 
                "Başarılı", 
                f"Sticker paketi başarıyla dışa aktarıldı!\n\nKonum: {target_dir}\nToplam: {len(exported_files)} dosya"
            )
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dışa aktarma sırasında hata oluştu:\n{e}")