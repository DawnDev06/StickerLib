import numpy as np
import cv2
from PIL import Image

class BackgroundRemover:
    @staticmethod
    def remove_white_background(img, threshold=240):
        """
        Sadece dış kenarlara bağlı olan beyaz pikselleri şeffaf yapar.
        Böylece iç kısımlardaki (gözler, beyaz detaylar vb.) beyazlar korunur.
        """
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            
        arr = np.array(img)
        rows, cols, _ = arr.shape
        
        # 1. Beyaz piksellerin ham maskesini çıkar
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        white_mask = (r >= threshold) & (g >= threshold) & (b >= threshold)
        
        # 2. Bağlı bileşenleri (Connected Components) bul
        mask_uint8 = white_mask.astype(np.uint8)
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask_uint8, connectivity=8)
        
        # 3. Sadece resmin dış kenarlarına temas eden bileşenleri arka plan kabul et
        bg_mask = np.zeros_like(white_mask, dtype=bool)
        
        for i in range(1, num_labels):  # 0 arkaplandır, 1'den başlar
            left = stats[i, cv2.CC_STAT_LEFT]
            top = stats[i, cv2.CC_STAT_TOP]
            width = stats[i, cv2.CC_STAT_WIDTH]
            height = stats[i, cv2.CC_STAT_HEIGHT]
            
            # Bileşen resmin sınırlarına (sol, üst, sağ, alt) dokunuyor mu?
            touches_border = (
                left == 0 or 
                top == 0 or 
                (left + width) >= cols or 
                (top + height) >= rows
            )
            
            if touches_border:
                bg_mask[labels == i] = True
        
        # 4. Sadece dış arkaplana ait beyaz pikselleri şeffaf yap
        arr[bg_mask, 3] = 0
        
        return Image.fromarray(arr, 'RGBA')