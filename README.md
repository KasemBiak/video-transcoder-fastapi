# Local Video Transcoder for Social Media

Aplikasi web sederhana berbasis **FastAPI** dan **FFmpeg** native untuk melakukan transcoding video secara lokal. Didesain khusus untuk mengoptimalkan video hasil editan (termasuk rekaman kamera tinggi seperti Samsung Ultra/Edge) agar siap diunggah ke **TikTok, Instagram Reels, dan WhatsApp Story** tanpa pecah atau patah-patah.

## Teknologi yang Digunakan
- **Backend:** Python, FastAPI, Uvicorn
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
- **Processing:** FFmpeg Native Binary

## Struktur Proyek
```text
project-sederhana/
├── bin/
│   └── ffmpeg.exe       # Native FFmpeg executable
├── static/
│   ├── index.html       # Antarmuka Web UI
│   ├── script.js        # Logika Unggah, Cancel, & Hapus File
│   └── style.css        # Styling CSS (Neobrutalism Design)
├── .gitignore           # File pengabaian Git
├── main.py              # Server FastAPI & Integrasi FFmpeg
├── README.md            # Dokumentasi Proyek
└── requirements.txt     # Dependensi Python
