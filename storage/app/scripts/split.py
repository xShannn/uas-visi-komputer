import os
import glob
import shutil
from sklearn.model_selection import train_test_split

def main():
    base_dir = "C:/laragon/www/deteksi-cacat-kain-laravel/storage/app/dataset_fabric"
    
    raw_dir = os.path.join(base_dir, "raw")
    train_dir = os.path.join(base_dir, "train")
    test_dir = os.path.join(base_dir, "test")

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    print(f"Mencari gambar di dalam sub-folder {raw_dir}...")

    # Mencari gambar masuk ke dalam sub-folder (recursive)
    semua_gambar = []
    for ext in ('**/*.jpg', '**/*.jpeg', '**/*.png'):
        semua_gambar.extend(glob.glob(os.path.join(raw_dir, ext), recursive=True))
    
    total_gambar = len(semua_gambar)
    if total_gambar == 0:
        print("Waduh! Tidak ada gambar yang ditemukan. Pastikan 6 folder tadi ada di dalam 'raw'.")
        return
        
    print(f"Total gambar ditemukan: {total_gambar}")

    # Bagi dataset (60% Train, 40% Test)
    train_files, test_files = train_test_split(semua_gambar, train_size=0.6, random_state=42)

    # Fungsi khusus untuk copy dan ganti nama file
    def copy_and_rename(file_list, target_folder):
        for f in file_list:
            # Ambil nama folder asal (misal: 'hole' atau 'stain')
            kategori = os.path.basename(os.path.dirname(f))
            # Ambil nama file aslinya (misal: '01.jpg')
            nama_file = os.path.basename(f)
            
            # Gabungkan jadi nama baru (ganti spasi jadi garis bawah)
            kategori_bersih = kategori.replace(" ", "_")
            nama_baru = f"{kategori_bersih}_{nama_file}"
            
            shutil.copy(f, os.path.join(target_folder, nama_baru))

    print(f"Menyalin {len(train_files)} gambar ke folder Train...")
    copy_and_rename(train_files, train_dir)

    print(f"Menyalin {len(test_files)} gambar ke folder Test...")
    copy_and_rename(test_files, test_dir)

    print("\n=== PEMBAGIAN DATASET SELESAI ===")

if __name__ == "__main__":
    main()