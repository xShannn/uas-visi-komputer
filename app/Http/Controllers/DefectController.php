<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Symfony\Component\Process\Process;

class DefectController extends Controller
{
    public function analyze(Request $request)
    {
        // 1. Validasi gambar yang di-upload
        $request->validate([
            'image' => 'required|image|mimes:jpeg,png,jpg|max:10240',
        ]);

        // 2. Simpan gambar sementara ke storage/app/temp_images
        $path = $request->file('image')->store('temp_images');
        $fullImagePath = storage_path('app/private/' . $path); // Laravel 11/12 biasanya menaruh di folder private
        if (!file_exists($fullImagePath)) {
            $fullImagePath = storage_path('app/' . $path); // Fallback jika tidak ada folder private
        }

        $scriptPath = storage_path('app/scripts/detect.py');

        // 3. Eksekusi Python (Pastikan 'python' bisa dipanggil dari CMD komputermu)
        $env = getenv();
        $env['SystemRoot'] = 'C:\\Windows';
        $env['SystemDrive'] = 'C:';

        $process = new Process(
            ['C:/Users/ACER/AppData/Local/Programs/Python/Python312/python.exe', $scriptPath, $fullImagePath],
            null,
            $env
        );
        $process->run();

        // 4. Hapus gambar sementara agar storage tidak penuh
        Storage::delete($path);

        // 5. Cek apakah ada error pada script Python
        if (!$process->isSuccessful()) {
            return response()->json([
                'status' => 'error',
                'message' => 'Python execution failed',
                'debug' => $process->getErrorOutput()
            ], 500);
        }

        // 6. Kembalikan output JSON dari Python ke Frontend
        $output = json_decode($process->getOutput(), true);
        return response()->json($output);
    }
}
