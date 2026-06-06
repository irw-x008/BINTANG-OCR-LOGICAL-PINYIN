@echo off
title Build BINTANG OCR LOGICAL PINYIN
echo =======================================================
echo Membangun Aplikasi BINTANG OCR LOGICAL PINYIN (.exe)
echo Target: Windows 7 ^& Windows 11 Compatibility
echo =======================================================
echo.
echo Memastikan dependensi terinstal...
pip install -r requirements.txt

echo.
echo Mulai kompilasi menggunakan Nuitka...
echo (Proses ini mungkin memakan waktu beberapa menit tergantung CPU)

python -m nuitka --onefile --windows-disable-console --output-dir=build main.py

echo.
echo =======================================================
echo Kompilasi selesai! 
echo Silakan cek folder 'build' untuk file main.exe
echo =======================================================
pause
