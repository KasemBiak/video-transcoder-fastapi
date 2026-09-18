const inputEl = document.getElementById('video-input');
const cancelInputBtn = document.getElementById('cancel-input-btn');
const btnEl = document.getElementById('convert-btn');
const statusEl = document.getElementById('status-text');
const videoEl = document.getElementById('output-video');

// Event saat pengguna memilih file video
inputEl.addEventListener('change', () => {
  if (inputEl.files.length > 0) {
    btnEl.disabled = false;
    cancelInputBtn.style.display = 'inline-block'; // Tampilkan tombol batal
    statusEl.innerText = 'File siap diproses.';
  } else {
    resetFileInput();
  }
});

// Event saat tombol "Batal Pilih File" diklik
cancelInputBtn.addEventListener('click', () => {
  resetFileInput();
});

// Fungsi untuk membersihkan pilihan file
function resetFileInput() {
  inputEl.value = ''; // Kosongkan file yang dipilih
  btnEl.disabled = true; // Matikan tombol proses
  cancelInputBtn.style.display = 'none'; // Sembunyikan tombol batal
  statusEl.innerText = 'Silakan pilih file video terlebih dahulu...';
  
  // Sembunyikan & bersihkan pemutar video jika ada
  videoEl.pause();
  videoEl.src = '';
  videoEl.style.display = 'none';
}

// Event saat tombol "Proses Video" diklik
btnEl.addEventListener('click', async () => {
  const file = inputEl.files[0];
  if (!file) return;

  btnEl.disabled = true;
  cancelInputBtn.style.display = 'none';
  statusEl.innerText = 'Mengirim video ke server Python & memproses... (mohon tunggu)';
  videoEl.style.display = 'none';

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('/api/transcode', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error('Gagal memproses video di server.');
    }

    const videoBlob = await response.blob();
    const videoUrl = URL.createObjectURL(videoBlob);

    videoEl.src = videoUrl;
    videoEl.style.display = 'block';
    statusEl.innerText = 'Selesai! Video berhasil diproses oleh server Python.';
  } catch (error) {
    statusEl.innerText = 'Terjadi kesalahan saat memproses video.';
    console.error(error);
  } finally {
    btnEl.disabled = false;
    // Tampilkan kembali tombol batal/reset jika file masih terpilih di input
    if (inputEl.files.length > 0) {
      cancelInputBtn.style.display = 'inline-block';
    }
  }
});