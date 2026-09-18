import os
import subprocess
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Local Video Transcoder")

UPLOAD_DIR = "temp_uploads"
OUTPUT_DIR = "temp_outputs"
FFMPEG_PATH = os.path.join("bin", "ffmpeg.exe")  # Menunjuk ke folder bin/ffmpeg.exe

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.post("/api/transcode")
async def transcode_video(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    output_filename = f"transcoded_{file_id}.mp4"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    try:
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal menyimpan file: {str(e)}")

    ffmpeg_cmd = [
        FFMPEG_PATH,
        "-y",
        "-i", input_path,
        "-vf", "format=yuv420p",    # Memastikan format warna kompatibel dengan semua medsos
        "-c:v", "libx264",
        "-preset", "slow",          # Hasil kompresi lebih rapi
        "-crf", "18",               # Mempertahankan ketajaman kualitas asli dari aplikasi edit
        "-c:a", "aac",
        "-b:a", "192k",             # Kualitas audio tetap jernih
        "-movflags", "+faststart",  # Agar video lancar saat di-stream / diunggah
        output_path
    ]

    try:
        process = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if process.returncode != 0:
            print("FFmpeg Error:", process.stderr)
            raise HTTPException(status_code=500, detail="Gagal mentranscode video.")
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

    response = FileResponse(
        path=output_path,
        media_type="video/mp4",
        filename=output_filename
    )
    response.headers["X-Output-Filename"] = output_filename
    return response


@app.delete("/api/delete")
async def delete_video(filename: str = Query(...)):
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(OUTPUT_DIR, safe_filename)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return {"status": "success", "message": f"File {safe_filename} berhasil dihapus."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gagal menghapus file: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail="File tidak ditemukan.")


# Melayani semua file di folder static (termasuk index.html)
app.mount("/", StaticFiles(directory="static", html=True), name="static")