import os
import shutil
from config.settings import OUTPUT_DIR

class PackExporter:
    @staticmethod
    def export_to_folder(pack, export_dir_name=None):
        # Eğer özel bir isim verilmediyse paketin adını kullan
        folder_name = export_dir_name if export_dir_name else pack.name
        target_dir = os.path.join(OUTPUT_DIR, folder_name)
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        exported_files = []
        for sticker in pack.stickers:
            if sticker.is_processed and sticker.processed_path and os.path.exists(sticker.processed_path):
                dest_path = os.path.join(target_dir, os.path.basename(sticker.processed_path))
                shutil.copy2(sticker.processed_path, dest_path)
                exported_files.append(dest_path)
                
        return target_dir, exported_files