<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\DefectController;

// Rute untuk menampilkan halaman web (tampilan depan)
Route::get('/', function () {
    return view('welcome');
});

// Rute untuk memproses gambar ke Python
Route::post('/api/analyze-fabric', [DefectController::class, 'analyze'])->name('analyze.fabric');
