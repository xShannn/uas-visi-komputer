import os
import random
import shutil

# Path ke folder raw dataset kamu
base_dir = "storage/app/dataset_fabric/raw"
backup_dir = "storage/app/dataset_fabric/raw_backup"

# Kategori yang mau di-diet-kan beserta target jumlahnya
targets = {
    "defect_free": 300,
    "stain": 300
}

if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

for folder, target_count in targets.items():
    folder_path = os.path.join(base_dir, folder)
    backup_folder_path = os.path.join(backup_dir, folder)
    
    if not os.path.exists(folder_path):
        print(f"Folder {folder} tidak ditemukan, lewati...")
        continue
        
    if not os.path.exists(backup_folder_path):
        os.makedirs(backup_folder_path)

    # Ambil semua file gambar di dalam folder
    files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
    
    if len(files) > target_count:
        # Acak urutan file
        random.shuffle(files)
        
        # Pisahkan file yang mau disimpan dan yang mau dibuang ke backup
        files_to_keep = files[:target_count]
        files_to_move = files[target_count:]
        
        print(f"[{folder}] Memindahkan {len(files_to_move)} file ke folder backup...")
        
        for file in files_to_move:
            src = os.path.join(folder_path, file)
            dst = os.path.join(backup_folder_path, file)
            shutil.move(src, dst)
            
        print(f"[{folder}] Selesai! Sekarang hanya tersisa {target_count} gambar.")
    else:
        print(f"[{folder}] Jumlah file ({len(files)}) sudah di bawah target, tidak ada yang dipindah.")

print("PROSES UNDERSAMPLING SELESAI!")