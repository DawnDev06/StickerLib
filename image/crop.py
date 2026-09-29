from PIL import Image

class ImageCropper:
    @staticmethod
    def auto_crop(img):
        """
        Şeffaf veya düz arka plan sınırlarına göre görseli kırpar.
        """
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            
        # Alfa kanalına göre bbox (sınır kutusu) bulma
        bbox = img.getbbox()
        if bbox:
            return img.crop(bbox)
        return img