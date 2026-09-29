from core.sticker import Sticker

class StickerPack:
    def __init__(self, name="MyStickerPack"):
        self.name = name
        self.stickers = []

    def add_sticker(self, file_path):
        # Aynı dosyanın tekrar eklenmesini önleyebiliriz (isteğe bağlı)
        if not any(s.original_path == file_path for s in self.stickers):
            sticker = Sticker(file_path)
            self.stickers.append(sticker)
            return sticker
        return None

    def remove_sticker(self, sticker_id):
        self.stickers = [s for s in self.stickers if s.id != sticker_id]

    def clear(self):
        self.stickers.clear()