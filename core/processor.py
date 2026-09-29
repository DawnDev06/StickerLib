import os
from config.settings import OUTPUT_DIR, STICKER_SIZE

class StickerProcessor:
    def __init__(self):
        # İleride arkaplan silme modeli vs. buraya yüklenebilir
        pass
        
    def process(self, sticker):
        """
        Şimdilik sadece hedef dosya adını belirliyoruz.
        Görüntü işleme (image/ modülleri) hazır olduğunda burayı dolduracağız.
        """
        try:
            filename, _ = os.path.splitext(sticker.filename)
            # Instagram/WhatsApp için webp veya png idealdir
            new_filename = f"{filename}_processed.png" 
            sticker.processed_path = os.path.join(OUTPUT_DIR, new_filename)
            
            # TODO: image/ klasöründeki resize, crop, remove_background fonksiyonları burada çağrılacak
            
            # Şimdilik başarılı sayıyoruz
            sticker.is_processed = True
            
        except Exception as e:
            sticker.error = str(e)
            sticker.is_processed = False
            
        return sticker