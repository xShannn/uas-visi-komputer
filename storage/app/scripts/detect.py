import time
import sys
import json
import cv2
import joblib
import numpy as np
from skimage.feature import graycomatrix, graycoprops
from sklearn.preprocessing import MinMaxScaler
import warnings

warnings.filterwarnings('ignore')

# --- MODUL 1 & 2: Saliency & Ekstraksi Fitur (Diringkas) ---
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
    # sal_map[(S_1_norm < mu - (3 * sigma)) | (S_1_norm > mu + (3 * sigma))] = 255
    # Turunkan batas sigma menjadi 1.5 agar lebih sensitif terhadap garis blur
    sal_map[(S_1_norm < mu - (2.5 * sigma)) | (S_1_norm > mu + (2.5 * sigma))] = 255

    return sal_map, gray

# def extract_features(roi):
#     glcm = graycomatrix(roi, distances=[1], angles=[0], levels=256, symmetric=True, normed=True)
#     contrast = graycoprops(glcm, 'contrast')[0, 0]
#     non_zero_glcm = glcm[glcm > 0]
#     entropy = -np.sum(non_zero_glcm * np.log2(non_zero_glcm))
#     return [contrast, entropy]

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

# --- MODUL 3: K-Means Sederhana untuk API ---
def affc_clustering(X, K=3, T=50):
    N, D = X.shape
    centroids = X[np.random.choice(N, min(K, N), replace=False)]
    labels = np.zeros(N)
    for _ in range(T):
        for i in range(N):
            labels[i] = np.argmin(np.sum((X[i] - centroids)**2, axis=1))
        for k in range(len(centroids)):
            if np.sum(labels == k) > 0:
                centroids[k] = np.mean(X[labels == k], axis=0)
    return labels

# --- EKSEKUSI UTAMA ---
def main():

    # Catat waktu mulai (START)
    start_time = time.time()

    # Tangkap path gambar dari parameter terminal (dikirim oleh Laravel)
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Path gambar tidak diberikan"}))
        sys.exit(1)
        
    image_path = sys.argv[1]
    img = cv2.imread(image_path)
    
    if img is None:
        print(json.dumps({"error": "Gagal membaca gambar dari direktori storage"}))
        sys.exit(1)

    img_blurred = cv2.GaussianBlur(img, (9,9), 0)
    saliency_map, gray_img = msds_pipeline(img_blurred)
    contours, _ = cv2.findContours(saliency_map, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    features, valid_boxes = [], []
    img_h, img_w = img.shape[:2]
    
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # if (w * h < 100) or (x < 10 or y < 10 or x+w > img_w-10 or y+h > img_h-10): continue
        # Cukup buang yang ukurannya terlalu kecil (noise), jangan buang yang di tepi
        if (w * h < 150): continue
        roi = gray_img[y:y+h, x:x+w]
        fitur_lengkap = extract_features(roi, x, y, w, h, gray_img)
        features.append(fitur_lengkap)
        # features.append(extract_features(roi))
        valid_boxes.append((x, y, w, h))
        
    results = []
    if len(features) > 0:
        # 1. Buka File Ingatan Otak (Sesuaikan path-nya jika perlu)
        model_dir = "C:/laragon/www/deteksi-cacat-kain-laravel/storage/app/models"
        scaler = joblib.load(f"{model_dir}/scaler.pkl")
        kmeans = joblib.load(f"{model_dir}/kmeans_model.pkl")

        # 2. Skalakan fitur gambar baru, lalu suruh K-Means menebak berdasarkan ingatan
        features_scaled = scaler.transform(np.array(features))
        labels = kmeans.predict(features_scaled)
        
        # Kamus kategori dari Colab (dengan tambahan kode Hex untuk Frontend)
        cluster_info = {
            0: {"name": "Normal", "color_hex": "#ffffff"},      
            1: {"name": "Stain", "color_hex": "#00ff00"},        
            2: {"name": "Normal", "color_hex": "#ffffff"},       
            3: {"name": "Hole", "color_hex": "#ff0000"}, 
            4: {"name": "Broken Yarn", "color_hex": "#ff00ff"}      
        }
        
        for i, box in enumerate(valid_boxes):
            x, y, w, h = box
            label_idx = int(labels[i])

            # 1. POTONG AREA KOTAK UNTUK DIANALISIS MANUAL
            # Asumsinya 'gray_image' adalah variabel gambar hitam-putih aslimu di detect.py
            roi = gray_img[y:y+h, x:x+w]
            
            # Hitung rata-rata kecerahan piksel di dalam kotak tersebut
            # 0 = Hitam pekat (lubang dalam), 255 = Putih terang
            mean_intensity = cv2.mean(roi)[0]

            # Hitung Aspect Ratio (Cegah pembagian dengan nol)
            safe_h = max(h, 1)
            safe_w = max(w, 1)
            aspect_ratio = max(safe_w / safe_h, safe_h / safe_w)

            # ==========================================
            # 2. LOGIKA BYPASS (SATPAM LAPIS KEDUA)
            # ==========================================
            # KASUS C: Benang Putus / Garis (Salah tebak jadi Stain atau Normal)
            # Jika kotaknya sangat memanjang (panjangnya > 3x lipat dari lebarnya)
            if aspect_ratio > 3.0:
                label_idx = 4  # Paksa jadi Broken Yarn

            # # KASUS A: Lubang Hitam Pekat.  Jika AI menebak ini Normal (0 atau 2), TAPI warnanya sangat gelap (misal di bawah 45)
            # if label_idx in [0, 2] and 
            elif mean_intensity < 85:
                label_idx = 3 
 
            # KASUS B: Lubang Putih Terang (Salah tebak jadi Stain)
            # Jika tebakannya Stain (1), TAPI warnanya sangat putih/terang (> 210)
            # elif label_idx == 1 and 
            elif mean_intensity > 210:
                label_idx = 3  # Paksa jadi Hole (Merah)

            if label_idx in [0, 2]:
                continue
            # Ambil info dari kamus, jika meleset fallback ke merah
            info = cluster_info.get(label_idx, {"name": "Unknown", "color_hex": "#000000"})
            
            results.append({
                "label": info["name"],
                "color": info["color_hex"], # Kirim warna ke Laravel
                "box": {"x": x, "y": y, "w": w, "h": h}
            })

    # Catat waktu selesai dan hitung durasi
    end_time = time.time()
    execution_time = round(end_time - start_time, 3)

    # Cetak hasil akhir berupa format JSON murni
    print(json.dumps({
        "status": "success", 
        "total_defects": len(results), 
        "execution_time_seconds": execution_time,
        "data": results
    }))

if __name__ == "__main__":
    main()