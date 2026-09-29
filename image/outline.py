import numpy as np
from PIL import Image, ImageOps

class ImageOutliner:
    @staticmethod
    def add_outline(img, outline_width=5, outline_color=(255, 255, 255, 255)):
        """
        Görselin etrafına sticker tarzı kalın bir dış çizgi (kontur) ekler.
        """
        # Genişletilmiş versiyonu oluşturmak için alfa kanalını kullanacağız
        arr = np.array(img)
        alpha = arr[:, :, 3]
        
        # Piksel taşmaları için basit bir dilation mantığı yerine Pillow filtreleri de kullanılabilir
        # Şimdilik temel bir taslak bırakıyoruz:
        return img