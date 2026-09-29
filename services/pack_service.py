import os
from core import sticker
from core.pack import StickerPack
from core.processor import StickerProcessor
from image.loader import ImageLoader
from image.crop import ImageCropper
from image.resize import ImageResizer
from image.background import BackgroundRemover
from config.settings import STICKER_SIZE
from image.background import BackgroundRemover

class PackService:
    def __init__(self, pack_name="InstagramStickers"):
        self.pack = StickerPack(name=pack_name)
        self.processor = StickerProcessor()

    def add_files(self, file_paths):
        added_stickers = []
        for path in file_paths:
            sticker = self.pack.add_sticker(path)
            if sticker:
                added_stickers.append(sticker)
        return added_stickers

    def process_all_stickers(self, progress_callback=None):
        """
        Paketteki tüm sticker'ları sırayla işler.
        progress_callback: Arayüzde ilerleme çubuğunu (progress bar) güncellemek için kullanılabilir.
        """
        total = len(self.pack.stickers)
        for index, sticker in enumerate(self.pack.stickers):
            try:
                # 1. Görseli yükle
                img = ImageLoader.load_image(sticker.original_path)

                # 2. Otomatik kırp (fazla boşlukları at)
                img = ImageCropper.auto_crop(img)

                # 3. Beyaz arka planı sil (Şeffaf yap)
                img = BackgroundRemover.remove_white_background(img, threshold=230)

                # 4. Standart boyuta getir (Padding ile)
                img = ImageResizer.resize_with_padding(img, target_size=STICKER_SIZE)
                
                # 5. İşlenmiş dosyayı çıktı dizinine kaydet
                filename, _ = os.path.splitext(sticker.filename)
                from config.settings import OUTPUT_DIR
                if not os.path.exists(OUTPUT_DIR):
                    os.makedirs(OUTPUT_DIR)
                    
                processed_filename = f"{filename}_sticker.png"
                processed_path = os.path.join(OUTPUT_DIR, processed_filename)
                
                img.save(processed_path, "PNG")
                
                # Sticker modelini güncelle
                sticker.processed_path = processed_path
                sticker.is_processed = True
                
            except Exception as e:
                sticker.error = str(e)
                sticker.is_processed = False

            if progress_callback:
                progress_callback(index + 1, total)

        return self.pack