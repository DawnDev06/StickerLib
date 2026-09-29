from PIL import Image
import os

class ImageLoader:
    @staticmethod
    def load_image(file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")
        try:
            img = Image.open(file_path)
            # RGBA moduna çevirmek şeffaflık işlemleri için hayat kurtarır
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            return img
        except Exception as e:
            raise ValueError(f"Görsel yüklenirken hata oluştu ({file_path}): {e}")