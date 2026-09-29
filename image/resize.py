from PIL import Image

class ImageResizer:
    @staticmethod
    def resize_with_padding(img, target_size=(512, 512), background_color=(0, 0, 0, 0)):
        """
        Görselin en boy oranını bozmadan hedef boyuta getirir,
        kalan boşlukları şeffaf (veya belirlenen renk) dolguyla doldurur.
        """
        original_width, original_height = img.size
        target_width, target_height = target_size

        # Oranı koruyarak yeniden boyutlandırma
        ratio = min(target_width / original_width, target_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)

        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Hedef boyutta yeni bir şeffaf tuval oluştur
        new_img = Image.new("RGBA", target_size, background_color)
        
        # Görseli ortala
        paste_x = (target_width - new_width) // 2
        paste_y = (target_height - new_height) // 2
        
        new_img.paste(resized_img, (paste_x, paste_y), resized_img)
        return new_img