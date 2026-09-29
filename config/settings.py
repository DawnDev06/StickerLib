import os

# Dizin ayarları
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# Çıkartma (Sticker) Ayarları - Instagram/WhatsApp için genelde 512x512 ve PNG/WebP istenir
STICKER_SIZE = (512, 512)
SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '.webp')