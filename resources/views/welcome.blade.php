<!DOCTYPE html>
<html lang="id">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistem Deteksi Kain Neumorphism</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            background-color: #dedede;
        }

        /* Shadow untuk elemen yang Timbul (Out) */
        .neu-out {
            border-radius: 20px;
            background: #dedede;
            box-shadow: 8px 8px 16px #8e8e8e,
                -8px -8px 16px #ffffff;
        }

        /* Shadow untuk tombol yang lebih kecil */
        .neu-btn {
            border-radius: 28px;
            background: #dedede;
            box-shadow: 4px 4px 8px #8e8e8e,
                -4px -4px 8px #ffffff;
            transition: all 0.2s ease-in-out;
        }

        .neu-btn:active {
            box-shadow: inset 4px 4px 8px #8e8e8e,
                inset -4px -4px 8px #ffffff;
        }

        /* Shadow untuk elemen yang Mencekung (Inset/Ke dalam) */
        .neu-in {
            border-radius: 20px;
            background: #dedede;
            box-shadow: inset 8px 8px 16px #8e8e8e,
                inset -8px -8px 16px #ffffff;
        }
    </style>
</head>

<body class="min-h-screen flex flex-col items-center pb-12 font-sans text-gray-800">

    {{-- <div class="flex gap-4 mt-6 mb-8">
        <button class="neu-btn px-6 py-2 text-sm font-medium text-orange-500">Beranda</button>
        <button class="neu-btn px-6 py-2 text-sm font-medium text-gray-500">Menu</button>
        <button class="neu-btn px-6 py-2 text-sm font-medium text-gray-500">Tentang</button>
    </div> --}}

    <div class="w-full max-w-5xl px-4 mb-8 text-center md:text-left flex flex-col md:items-start items-center"><br><br>
        <h1 class="text-3xl md:text-4xl font-semibold mb-2">Sistem Deteksi Cacat Kain Otomatis</h1>
        <p class="text-gray-600 max-w-2xl text-sm md:text-base">Temukan cacat pada kain dengan cepat menggunakan kecerdasan buatan. Solusi tepat untuk industri tekstil yang mengutamakan kualitas.</p>
    </div>

    <div class="w-full max-w-5xl px-4 mb-12 flex flex-row justify-center items-center gap-4 md:gap-6">
        
        <div class="neu-out w-full max-w-[240px] h-40 p-2">
            <div class="w-full h-full bg-gray-200 rounded-xl relative overflow-hidden flex items-center justify-center">
                <span class="absolute top-2 left-2 bg-red-600 text-white text-xs px-2 py-1 rounded font-bold border border-red-800 z-10">Hole</span>
                <img src="{{ asset('images/hole.svg') }}" alt="Hole Defect" class="w-full h-full object-cover">
            </div>
        </div>

        <div class="neu-out w-full max-w-[240px] h-40 p-2">
            <div class="w-full h-full bg-gray-200 rounded-xl relative overflow-hidden flex items-center justify-center">
                <span class="absolute top-2 left-2 bg-cyan-500 text-white text-xs px-2 py-1 rounded font-bold border border-cyan-700 z-10">Broken Yarn</span>
                <img src="{{ asset('images/broken_yarn.svg') }}" alt="Broken Yarn Defect" class="w-full h-full object-cover">
            </div>
        </div>

        <div class="neu-out w-full max-w-[240px] h-40 p-2">
            <div class="w-full h-full bg-gray-200 rounded-xl relative overflow-hidden flex items-center justify-center">
                <span class="absolute top-2 right-2 bg-purple-600 text-white text-xs px-2 py-1 rounded font-bold border border-purple-800 z-10">End out</span>
                <img src="{{ asset('images/end_out.svg') }}" alt="End Out Defect" class="w-full h-full object-cover">
            </div>
        </div>

        <div class="neu-out w-full max-w-[240px] h-40 p-2">
            <div class="w-full h-full bg-gray-200 rounded-xl relative overflow-hidden flex items-center justify-center">
                <span class="absolute top-2 right-2 bg-green-500 text-white text-xs px-2 py-1 rounded font-bold border border-green-700 z-10">Stain</span>
                <img src="{{ asset('images/stain.svg') }}" alt="Stain Defect" class="w-full h-full object-cover">
            </div>
        </div>

    </div>

    <div class="w-full max-w-5xl px-4 grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
        <div class="neu-out p-8 text-center flex flex-col justify-center">
            <h2 class="text-lg font-bold mb-4">Transformasi Inspeksi Kualitas Kain<br>Berbasis Kecerdasan Buatan</h2>
            <div class="neu-in p-6 text-sm text-gray-600 leading-relaxed">
                Sistem ini hadir sebagai solusi cerdas berbasis web untuk memajukan industri tekstil pada era revolusi industri 4.0. Menggunakan teknologi kecerdasan buatan, aplikasi ini mampu mengenali berbagai jenis kecacatan pada kain dengan cepat dan akurat, membantu meningkatkan efisiensi dengan presisi tinggi.
            </div>
        </div>
        <div class="neu-out p-8 text-center flex flex-col justify-center">
            <h2 class="text-lg font-bold mb-4">Arsitektur &<br>Algoritma di Balik Layar</h2>
            <div class="neu-in p-6 text-sm text-gray-600 leading-relaxed flex flex-col gap-3">
                <p><strong>YOLOv8 (You Only Look Once)</strong><br>Mendeteksi objek dengan cepat dan presisi tinggi secara *real-time*.</p>
                <p><strong>CNN (Convolutional Neural Network)</strong><br>Mengekstraksi fitur visual pada gambar kain untuk membantu pengklasifikasian jenis cacat dengan sangat baik.</p>
            </div>
        </div>
    </div>

    <div class="w-full max-w-4xl px-4 flex flex-col gap-6 items-center">
        
        <div id="dropzone" class="neu-in p-6 w-full max-w-2xl h-64 transition-all duration-300">
            <div class="border-2 border-dashed border-gray-400 rounded-xl w-full h-full flex flex-col items-center justify-center relative">
                <p class="font-medium text-gray-700 mb-1">Drag and Drop your file here</p>
                <p class="text-xs text-gray-500 mb-4">file supported: PNG, JPG</p>
                <p class="text-sm font-bold text-gray-700 mb-4">OR</p>

                <button type="button" id="browseBtn" class="neu-btn px-8 py-2 text-sm font-medium text-gray-700 hover:text-black">
                    Browse File
                </button>

                <p id="selectedFileName" class="text-sm text-blue-600 font-semibold mt-4 hidden"></p>
            </div>
        </div>

        <form id="uploadForm" class="hidden">
            @csrf
            <input type="file" id="imageInput" name="image" accept="image/png, image/jpeg, image/jpg">
        </form>

        <button type="button" id="btnMulai" class="neu-btn px-12 py-3 text-lg font-bold text-gray-800 hover:text-black mb-4">
            Mulai
        </button>

        <div id="loading" class="hidden text-center text-blue-600 font-semibold animate-pulse w-full">
            Sedang menganalisis gambar menggunakan Python...
        </div>

        <div id="resultContainer" class="hidden neu-in p-8 w-full flex flex-col md:flex-row gap-8 items-start justify-center">
            
            <div class="relative inline-block rounded-xl overflow-hidden shadow-lg w-full md:w-2/3">
                <img id="imagePreview" class="w-full h-auto block" />
                <canvas id="overlayCanvas" class="absolute top-0 left-0 w-full h-full"></canvas>
            </div>

            <div class="w-full md:w-1/3 flex flex-col gap-6">
                <div class="neu-out p-6 flex flex-col items-center justify-center text-center">
                    <p class="text-xs font-bold text-gray-500 mb-2">Waktu Eksekusi</p>
                    <p id="waktuText" class="text-2xl font-black text-blue-500">0.000</p>
                    <p class="text-xs text-gray-500 mt-1">detik</p>
                </div>
                <div class="neu-out p-6 flex flex-col items-center justify-center text-center">
                    <p class="text-xs font-bold text-gray-500 mb-2">Ditemukan Cacat</p>
                    <p id="cacatText" class="text-3xl font-black text-red-600">0</p>
                    <p id="statusCacatText" class="text-xs text-gray-500 mt-1">Titik</p>
                </div>
            </div>

        </div>

    </div>

    <script>
        const dropzone = document.getElementById('dropzone');
        const browseBtn = document.getElementById('browseBtn');
        const imageInput = document.getElementById('imageInput');
        const btnMulai = document.getElementById('btnMulai');
        const selectedFileName = document.getElementById('selectedFileName');
        
        const csrfToken = document.querySelector('input[name="_token"]').value;

        const loading = document.getElementById('loading');
        const resultContainer = document.getElementById('resultContainer');
        const imgPreview = document.getElementById('imagePreview');
        const canvas = document.getElementById('overlayCanvas');
        const ctx = canvas.getContext('2d');
        
        const waktuText = document.getElementById('waktuText');
        const cacatText = document.getElementById('cacatText');
        const statusCacatText = document.getElementById('statusCacatText');

        let fileToUpload = null;

        browseBtn.addEventListener('click', () => {
            imageInput.click();
        });

        dropzone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropzone.classList.add('opacity-50', 'scale-[0.98]');
        });

        dropzone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            dropzone.classList.remove('opacity-50', 'scale-[0.98]');
        });

        dropzone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropzone.classList.remove('opacity-50', 'scale-[0.98]');

            if (e.dataTransfer.files.length > 0) {
                siapkanFile(e.dataTransfer.files[0]);
                imageInput.files = e.dataTransfer.files;
            }
        });

        imageInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                siapkanFile(e.target.files[0]);
            }
        });

        function siapkanFile(file) {
            fileToUpload = file;
            selectedFileName.textContent = `File disiapkan: ${file.name}`;
            selectedFileName.classList.remove('hidden');
            resultContainer.classList.add('hidden');
        }

        btnMulai.addEventListener('click', () => {
            if (!fileToUpload) {
                alert('Silakan pilih atau masukkan gambar kain terlebih dahulu!');
                return;
            }
            prosesGambar(fileToUpload);
        });

        async function prosesGambar(file) {
            resultContainer.classList.add('hidden');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            loading.classList.remove('hidden');

            const formData = new FormData();
            formData.append('image', file);
            formData.append('_token', csrfToken);

            try {
                const response = await fetch("{{ route('analyze.fabric') }}", {
                    method: 'POST',
                    headers: { 'Accept': 'application/json' },
                    body: formData
                });

                const data = await response.json();

                if (data.status === 'success') {
                    const reader = new FileReader();
                    reader.onload = function (event) {
                        imgPreview.src = event.target.result;
                        
                        imgPreview.onload = () => {
                            resultContainer.classList.remove('hidden');

                            canvas.width = imgPreview.width;
                            canvas.height = imgPreview.height;

                            const scaleX = imgPreview.width / imgPreview.naturalWidth;
                            const scaleY = imgPreview.height / imgPreview.naturalHeight;

                            waktuText.textContent = data.execution_time_seconds;
                            cacatText.textContent = data.total_defects;

                            if (data.total_defects > 0) {
                                cacatText.classList.replace('text-green-500', 'text-red-600');
                                statusCacatText.textContent = "Titik Cacat";
                            } else {
                                cacatText.classList.replace('text-red-600', 'text-green-500');
                                statusCacatText.textContent = "Kain Normal";
                            }

                            data.data.forEach(defect => {
                                const box = defect.box;
                                const x = box.x * scaleX;
                                const y = box.y * scaleY;
                                const w = box.w * scaleX;
                                const h = box.h * scaleY;

                                ctx.strokeStyle = defect.color;
                                ctx.lineWidth = 3;
                                ctx.strokeRect(x, y, w, h);

                                ctx.fillStyle = defect.color;
                                ctx.fillRect(x, y - 25, ctx.measureText(defect.label).width + 20, 25);

                                ctx.fillStyle = (defect.label === 'Normal' || defect.label === 'Broken Yarn') ? 'black' : 'white';
                                ctx.font = '14px Arial';
                                ctx.fillText(defect.label, x + 5, y - 7);
                            });
                        };
                    };
                    reader.readAsDataURL(file);

                } else {
                    alert("Error Python: " + data.message + "\n\n" + (data.debug || ""));
                }
            } catch (error) {
                console.error(error);
                alert("Terjadi kesalahan jaringan.");
            } finally {
                loading.classList.add('hidden');
            }
        }
    </script>
</body>

</html>