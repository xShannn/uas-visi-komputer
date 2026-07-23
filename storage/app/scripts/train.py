import os
import glob
import cv2
import numpy as np
import joblib
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from skimage.feature import graycomatrix, graycoprops
import math

# ==============================================================================
# 1. PASTE FUNGSI KAMU DI SINI
# Silakan copy-paste fungsi msds_pipeline() dan extract_features() 
# dari file detect.py milikmu ke sini agar persis sama.
# ==============================================================================

def extract_features(roi, x, y, w, h, gray_img):
    # ---------------------------------------------------------
    # 1. Geometrical Features (Fitur Geometri)
    # ---------------------------------------------------------
    saliency_area = w * h
    length = h 
    width = w
    # Menghindari error pembagian dengan nol
    ratio = length / width if width > 0 else 0 

    # ---------------------------------------------------------
    # 2. Intensity Features (Fitur Intensitas Kecerahan)
    # ---------------------------------------------------------
    gray_mean = np.mean(roi)
    gray_var = np.var(roi)

    # Menghitung mean dan varians background (Area selain kotak cacat)
    # Kita buat duplikat gambar abu-abu, lalu "hapus" area cacatnya
    mask = np.ones(gray_img.shape, dtype=bool)
    mask[y:y+h, x:x+w] = False
    background_pixels = gray_img[mask]
    
    bg_mean = np.mean(background_pixels)
    bg_var = np.var(background_pixels)

    # ---------------------------------------------------------
    # 3. Texture Features (Fitur Tekstur menggunakan GLCM)
    # ---------------------------------------------------------
    # GLCM butuh format angka bulat (0-255)
    roi_uint = roi.astype(np.uint8)
    
    # Hitung matriks GLCM
    glcm = graycomatrix(roi_uint, distances=[1], angles=[0], levels=256, symmetric=True, normed=True)
    
    contrast = graycoprops(glcm, 'contrast')[0, 0]
    homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
    asm = graycoprops(glcm, 'ASM')[0, 0]
    energy = graycoprops(glcm, 'energy')[0, 0]
    
    # Rumus Entropy manual dari probabilitas GLCM: E = -\sum p \log_2 p
    p = glcm[:, :, 0, 0]
    p_non_zero = p[p > 0]
    entropy = -np.sum(p_non_zero * np.log2(p_non_zero))

    # Kembalikan 13 fitur tepat seperti urutan Tabel 1 di Paper
    return [
        saliency_area, length, width, ratio,
        gray_mean, gray_var, bg_mean, bg_var,
        contrast, homogeneity, asm, energy, entropy
    ]
    pass 

def calculate_saliency_map(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image.copy()
    hist, _ = np.histogram(gray.flatten(), bins=256, range=[0,256])
    hist = hist / hist.sum()
    saliency_values = np.zeros(256)
    for k in range(256):
        saliency_values[k] = np.sum(hist * np.abs(np.arange(256) - k))
    return saliency_values[gray]

def msds_pipeline(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    S_1 = calculate_saliency_map(image)
    S_1_norm = cv2.normalize(S_1, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    # Disederhanakan untuk kecepatan API
    mu, sigma = np.mean(S_1_norm), np.std(S_1_norm)
    sal_map = np.zeros_like(S_1_norm)
    sal_map[(S_1_norm < mu - (3 * sigma)) | (S_1_norm > mu + (3 * sigma))] = 255
    return sal_map, gray
    pass

# ==============================================================================
# 2. LOGIKA UTAMA TRAINING
# ==============================================================================
def main():
    # Folder data latih dan folder tempat menyimpan "otak/ingatan" model
    train_dir = "C:/laragon/www/deteksi-cacat-kain-laravel/storage/app/dataset_fabric/train"
    model_dir = "C:/laragon/www/deteksi-cacat-kain-laravel/storage/app/models"
    
    # Buat folder models jika belum ada
    os.makedirs(model_dir, exist_ok=True)

    # Ambil semua file gambar
    semua_gambar = glob.glob(os.path.join(train_dir, "*.jpg")) + \
                   glob.glob(os.path.join(train_dir, "*.png"))

    if not semua_gambar:
        print("Waduh, tidak ada gambar di folder train!")
        return

    all_features = []
    file_sources = [] 

    print(f"Mulai mengekstrak fitur dari {len(semua_gambar)} gambar latih. Tunggu sebentar...")

    # Looping semua gambar untuk diekstrak fiturnya
    for idx, img_path in enumerate(semua_gambar):
        img = cv2.imread(img_path)
        if img is None: continue

        img_blurred = cv2.GaussianBlur(img, (9,9), 0)
        saliency_map, gray_img = msds_pipeline(img_blurred)
        contours, _ = cv2.findContours(saliency_map, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        img_h, img_w = img.shape[:2]
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if (w * h < 100) or (x < 10 or y < 10 or x+w > img_w-10 or y+h > img_h-10): continue

            roi = gray_img[y:y+h, x:x+w]
            fitur = extract_features(roi, x, y, w, h, gray_img)

            all_features.append(fitur)
            # Simpan nama file asal (contoh: hole_05.jpg) untuk dianalisis nanti
            file_sources.append(os.path.basename(img_path)) 

        if (idx+1) % 20 == 0:
            print(f"Proses: {idx+1}/{len(semua_gambar)} gambar selesai...")

    if len(all_features) == 0:
        print("Gagal! Tidak ada satupun kandidat cacat yang ditemukan di dataset train.")
        return

    print(f"\nSelesai ekstraksi! Total {len(all_features)} ROI (kandidat cacat) ditemukan.")
    print("Mesin sedang belajar mengelompokkan (Training K-Means)...")

    X = np.array(all_features)

    # 3. Skala Data (WAJIB DISIMPAN JUGA)
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # 4. Training K-Means
    # random_state=42 memastikan hasil training ini paten dan tidak berubah-ubah
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    kmeans.fit(X_scaled)

    # 5. Simpan Model Ingatan (.pkl)
    joblib.dump(scaler, os.path.join(model_dir, "scaler.pkl"))
    joblib.dump(kmeans, os.path.join(model_dir, "kmeans_model.pkl"))

    print("\n=== MODEL BERHASIL DISIMPAN! ===")
    print(f"Lokasi: {model_dir}")
    
    # 6. Analisis Pemetaan Label (Rahasia mengetahui Keranjang 0-4)
    print("\n[PEMETAAN LABEL CLUSTER]")
    labels = kmeans.labels_
    for i in range(5):
        print(f"\nCluster {i} mayoritas berisi gambar dari kategori:")
        anggota = [file_sources[j] for j in range(len(labels)) if labels[j] == i]
        
        kategori_count = {}
        for nama in anggota:
            # Mengambil kata depan dari nama file (misal: "stain" dari "stain_01.jpg")
            kategori_asli = nama.split('_')[0]
            if nama.startswith("defect_free"): kategori_asli = "defect_free"
            elif nama.startswith("Broken"): kategori_asli = "Broken_Yarn"
            kategori_count[kategori_asli] = kategori_count.get(kategori_asli, 0) + 1

        # Tampilkan urutan dari yang paling banyak
        kategori_sorted = sorted(kategori_count.items(), key=lambda x: x[1], reverse=True)
        for kat, jumlah in kategori_sorted:
            print(f"  - {kat}: {jumlah} temuan kotak")

if __name__ == "__main__":
    main()