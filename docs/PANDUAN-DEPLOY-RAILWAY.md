# Panduan Deploy Hermes Railway — dari awal sampai berhasil

Panduan ringkas untuk mencoba ketiga mode dari repository ini: **Dashboard**, **Railway Variables**, dan **Ubuntu Terminal**.

**Arti tanda:** 🔴 wajib · 🟡 perhatian · 📋 siap salin · ✅ hasil yang benar · 🧰 perbaikan.

## 1. Tentukan cara mencoba

| Mode | Gunanya | Perlu domain publik? | Setup awal |
|---|---|---|---|
| **Dashboard** | Mengelola Hermes lewat web | Ya, target port 8080 | Login Dashboard, lalu atur model/provider |
| **Railway Variables** | Gateway bot Telegram/Discord tanpa Dashboard | Tidak | Isi API key dan token pada Variables |
| **Ubuntu Terminal** | Terminal browser + Hermes CLI + Gateway | Ya, target port 8080 | Jalankan wizard `hermes setup` |

🔴 Jika ingin membandingkan ketiga mode, buat **tiga service terpisah**. Setiap service harus memiliki Volume sendiri di `/opt/data`.

🟡 Jangan jalankan token Telegram/Discord yang sama di lebih dari satu Gateway sekaligus. Saat mencoba mode lain, hentikan service lama atau gunakan token bot berbeda.

## 2. Siapkan repository di Railway

1. Buka Railway dan masuk ke akun.
2. Buat project baru, atau buka project tempat service akan dibandingkan.
3. Klik **New / + Create → GitHub Repo** (nama menu bisa berbeda menurut tampilan Railway).
4. Hubungkan GitHub jika diminta.
5. Pilih repository **`DURIAN-ORGANISASI/hermes-railway`**, branch **`main`**.
6. Tunggu Railway membuat service dan menjalankan build pertama.
7. Beri nama service agar mudah dibedakan: `Hermes-Dashboard`, `Hermes-Variables`, dan `Hermes-Ubuntu`.

📌 Ulangi langkah memilih GitHub Repo untuk setiap service. Ketiganya berasal dari repo yang sama, tetapi konfigurasi deploy-nya berbeda.

### Pengaturan build yang perlu diketahui

- **Dashboard:** gunakan Dockerfile root, yaitu `Dockerfile`.
- **Railway Variables:** gunakan Dockerfile root, yaitu `Dockerfile`.
- **Ubuntu Terminal:** gunakan `ubuntu/Dockerfile`.
- Untuk ketiga mode, **Root Directory harus kosong** agar Railway memakai root repository sebagai build context.

Jangan memasang ketiga mode dalam satu service.

---

# A. Mode 1 — Dashboard

## A1. Atur build

Buka Railway → service **Hermes-Dashboard** → **Settings → Build**:

1. **Root Directory:** kosong.
2. **Dockerfile Path:** `Dockerfile` (atau path root Dockerfile jika terisi otomatis).
3. Simpan perubahan jika Railway menampilkan tombol Save.

## A2. Isi Variables

Buka **Hermes-Dashboard → Variables**. Tambahkan blok berikut melalui editor yang menerima variabel per baris. Ganti semua nilai contoh.

~~~dotenv
DEPLOY_MODE=dashboard
USERNAME=buat_username_login
PASSWORD=ganti_dengan_password_kuat_dan_unik
SECRET=ganti_dengan_secret_acak_minimal_32_karakter
HERMES_HOME=/opt/data
TZ=Asia/Jakarta
PORT=8080
~~~

🔴 Ketentuan:
- `USERNAME`: nama login Dashboard yang akan kamu gunakan.
- `PASSWORD`: password login yang kuat dan unik.
- `SECRET`: minimal 32 karakter; jangan gunakan nilai contoh.
- `PORT=8080`: harus cocok dengan target port domain Railway.

📋 Cara membuat secret acak di terminal Linux/Ubuntu:

~~~bash
openssl rand -hex 32
~~~

Salin hasilnya ke `SECRET`. Jangan taruh password atau secret asli di GitHub.

## A3. Pasang Volume

1. Buka **Hermes-Dashboard → Volumes**.
2. Klik **Add Volume / New Volume**.
3. Set mount path tepat ke:

~~~text
/opt/data
~~~

4. Simpan. Gunakan Volume khusus untuk Dashboard; jangan pakai Volume milik service lain.

## A4. Buat domain dan samakan port

1. Buka **Hermes-Dashboard → Settings → Networking**.
2. Klik **Generate Domain** jika domain belum tersedia.
3. Periksa target port domain: set ke **8080**.
4. Simpan perubahan.

✅ Gunakan domain `*.up.railway.app` yang dibuat Railway untuk tes pertama. Setelah URL ini berfungsi, baru pasang custom domain jika diperlukan.

## A5. Deploy dan login

1. Buka **Deployments**.
2. Jalankan deploy/redeploy jika perubahan Build, Variables, atau Volume belum diterapkan.
3. Tunggu status deployment menjadi **SUCCESS**.
4. Buka **Deploy Logs** dan pastikan tidak ada error startup.
5. Klik domain Railway atau buka URL `https://DOMAIN-KAMU.up.railway.app`.
6. Login menggunakan `USERNAME` dan `PASSWORD` yang kamu isi di Variables.

✅ Jika halaman login terlihat, domain dan layanan web pernah berhasil dijangkau. Setelah login, buka menu Dashboard yang dibutuhkan, misalnya **Models**. Jika ingin membuka halaman model secara langsung, coba `/models?profile=default` setelah domain dan login berfungsi.

🟡 Jangan membuka Dashboard ke internet tanpa proteksi akses yang memadai. Username/password saja bukan pengganti OAuth/OIDC atau access gateway tepercaya.

## A6. Jika Dashboard menampilkan “Application failed to respond”

Screenshot sebelumnya menunjukkan error ini pada domain Railway. Periksa berurutan:

1. Railway → **Hermes-Dashboard → Deployments → View Logs / Deploy Logs**.
2. Jika log menyebut `USERNAME`, `PASSWORD`, atau `SECRET` belum diatur, isi ketiganya lalu redeploy.
3. Jika log menyebut `SECRET must be at least 32 characters`, buat secret baru minimal 32 karakter.
4. Buka **Settings → Build**. Pastikan Root Directory kosong dan Dockerfile root dipakai.
5. Buka **Variables**. Pastikan `PORT=8080`.
6. Buka **Settings → Networking**. Pastikan target port domain juga `8080`.
7. Setelah menyimpan, redeploy dan tes lagi dengan domain `.up.railway.app`.
8. Jika masih gagal, cari **error pertama** pada Deploy Logs. Jangan menebak atau mengubah banyak variabel sekaligus.

🟡 Error **“Application failed to respond”** tidak otomatis berarti URL domain salah. Artinya Railway belum menerima respons aplikasi yang sehat untuk request tersebut; Deploy Logs diperlukan untuk mengetahui penyebab pastinya.

---

# B. Mode 2 — Railway Variables

Mode ini menjalankan Gateway Telegram/Discord tanpa antarmuka web. **Domain publik tidak dibutuhkan** untuk penggunaan bot dengan polling/WebSocket keluar.

## B1. Atur build

Buka **Hermes-Variables → Settings → Build**:

1. **Root Directory:** kosong.
2. **Dockerfile Path:** `Dockerfile` di root repo.
3. Simpan jika ada perubahan.

## B2. Isi seluruh Variables

Buka **Hermes-Variables → Variables**. Tempel blok lengkap berikut, lalu isi hanya provider dan platform yang kamu gunakan.

~~~dotenv
DEPLOY_MODE=variables
HERMES_HOME=/opt/data
TZ=Asia/Jakarta

GROQ_API_KEY=
MISTRAL_API_KEY=
NVIDIA_API_KEY=
GEMINI_API_KEY=
GOOGLE_API_KEY=

TELEGRAM_BOT_TOKEN=
TELEGRAM_ALLOWED_USERS=

DISCORD_BOT_TOKEN=
DISCORD_ALLOWED_USERS=
DISCORD_ALLOWED_CHANNELS=
DISCORD_FREE_RESPONSE_CHANNELS=
DISCORD_AUTO_THREAD=false
~~~

🔴 Wajib: isi **minimal satu API key provider** yang aktif. Jangan biarkan semua API key kosong.

📋 Contoh jika hanya menggunakan NVIDIA:

~~~dotenv
NVIDIA_API_KEY=tempel_api_key_nvidia
~~~

Urutan provider saat beberapa key terisi: **Groq → Mistral → NVIDIA → Gemini**. Jika `GEMINI_API_KEY` kosong, `GOOGLE_API_KEY` dapat dipakai sebagai alias.

### Variabel bot

| Variabel | Isi |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Token dari `@BotFather` |
| `TELEGRAM_ALLOWED_USERS` | ID pengguna Telegram numerik yang diizinkan |
| `DISCORD_BOT_TOKEN` | Token bot dari Discord Developer Portal |
| `DISCORD_ALLOWED_USERS` | ID pengguna Discord yang diizinkan |
| `DISCORD_ALLOWED_CHANNELS` | ID channel yang diizinkan |
| `DISCORD_FREE_RESPONSE_CHANNELS` | ID channel yang boleh dijawab tanpa mention |
| `DISCORD_AUTO_THREAD` | Biarkan `false` untuk menonaktifkan thread otomatis |

Isi allowlist dengan ID yang benar. Jangan masukkan username ketika kolom meminta ID numerik.

## B3. Pasang Volume

1. Buka **Hermes-Variables → Volumes**.
2. Tambahkan Volume baru.
3. Mount path: `/opt/data`.
4. Jangan berbagi Volume ini dengan Dashboard atau Ubuntu.

## B4. Deploy dan cek Gateway

1. Buka **Deployments** → deploy/redeploy service.
2. Tunggu proses startup selesai.
3. Buka **Deploy Logs**.
4. Pastikan tidak ada pesan `No provider API key found`, error autentikasi, atau error konfigurasi.
5. Kirim pesan uji ke bot yang tokennya kamu isi.

✅ Mode Variables menyusun `/opt/data/config.yaml` berdasarkan API key aktif setiap startup. Ubah provider dan token dari Railway Variables, bukan dengan mengandalkan edit manual pada file yang dihasilkan.

🟡 Jangan buat domain publik untuk mode ini kecuali kamu mengetahui bahwa ada endpoint web yang memang perlu dibuka.

### Jika bot tidak membalas

1. Periksa API key, model, dan kuota provider.
2. Periksa token bot dan allowlist.
3. Untuk Telegram, kirim DM dan `/start`.
4. Untuk Discord, aktifkan **Message Content Intent** di Discord Developer Portal; periksa izin channel dan mention bot.
5. Periksa Deploy Logs saat mengirim pesan.
6. Pastikan token bot yang sama tidak dipakai service Gateway lain.

---

# C. Mode 3 — Ubuntu Terminal

Mode ini memberi terminal Ubuntu di browser, Hermes CLI, dan Gateway yang mulai otomatis setelah konfigurasi selesai.

## C1. Atur Dockerfile dengan benar

Buka **Hermes-Ubuntu → Settings → Build**:

1. **Root Directory:** kosong.
2. **Dockerfile Path:** `ubuntu/Dockerfile`.
3. Simpan perubahan.

🔴 Variabel `RAILWAY_DOCKERFILE_PATH` di bawah ini **tidak menggantikan pemeriksaan Dockerfile Path pada Settings**. Pastikan keduanya sesuai.

## C2. Isi Variables

Buka **Hermes-Ubuntu → Variables**, lalu tempel blok berikut. Ganti username dan password contoh.

~~~dotenv
RAILWAY_DOCKERFILE_PATH=/ubuntu/Dockerfile
TERMINAL_USER=ganti_username_terminal
TERMINAL_PASSWORD=ganti_password_acak_minimal_16_karakter
HERMES_HOME=/opt/data
HERMES_RUNTIME_DIR=/usr/local/share/hermes-tools
UV_CACHE_DIR=/tmp/uv-cache
HERMES_AUTOSTART=true
TZ=Asia/Jakarta
PORT=8080
~~~

🔴 Password terminal minimal 16 karakter. Username tidak boleh mengandung titik dua (`:`). Jangan menggunakan password yang sama dengan akun lain.

## C3. Pasang Volume

1. Buka **Hermes-Ubuntu → Volumes**.
2. Tambahkan Volume baru.
3. Mount path tepat ke:

~~~text
/opt/data
~~~

4. Simpan dan jangan menghapus Volume setelah bot berjalan.

Folder `/opt/data` menyimpan konfigurasi serta state Hermes. Folder `/data` untuk file terminal berbeda; tambahkan Volume kedua yang berbeda di `/data` jika file terminal juga harus bertahan setelah redeploy.

## C4. Buat domain terminal

1. Buka **Settings → Networking**.
2. Klik **Generate Domain**.
3. Pastikan target port domain **8080**.
4. Simpan dan tunggu deploy selesai.

Buka domain Railway, lalu login menggunakan `TERMINAL_USER` dan `TERMINAL_PASSWORD`.

🟡 Jika terminal tidak terbuka, periksa status service, target port 8080, dan Deploy Logs.

## C5. Jalankan wizard Hermes

Semua langkah berikut dilakukan **di terminal browser Railway**, bukan di Telegram.

Ketik:

~~~bash
hermes setup
~~~

1. Pilih **Full setup**.
2. Jika menu bergerak, gunakan tombol panah lalu Enter.
3. Jika prompt meminta nomor, ketik nomor di samping pilihan yang sesuai, lalu Enter.
4. Lanjutkan ke pengaturan provider/model.

🔴 Nomor opsi dapat berbeda menurut versi wizard. Ikuti label dan angka yang tampil pada terminalmu.

## C5A. Peta pilihan wizard — pilih yang mana?

Bagian ini menjelaskan **pilihan yang muncul satu per satu**. Nama dan urutan menu bisa berubah mengikuti versi Hermes, jadi cocokkan **labelnya**, bukan menghafal nomor.

### 1. Saat ditanya metode setup

| Pilihan di layar | Yang dilakukan | Alasan |
|---|---|---|
| **Full Setup** | ✅ **PILIH INI** | Bisa memakai API key milik sendiri, lalu memilih tools dan Telegram. |
| Quick Setup / Nous Portal | Jangan pilih untuk setup gratis berbasis API key | Memakai login Nous Portal dan penggunaan mengikuti paket/subscription Portal. |
| Blank Slate | Lewati untuk tutorial ini | Mulai dengan fitur minimal; lebih banyak hal harus diaktifkan manual. |

🔴 Untuk panduan ini, gunakan **Full Setup** agar langkah provider, tools, dan Telegram terlihat.

### 2. Saat menu memilih provider AI muncul

Pada screenshot sebelumnya, pilihan yang terlihat antara lain:

| Label yang terlihat | Pilih kapan? |
|---|---|
| **Google AI Studio** | ✅ **PILIH INI** jika ingin memakai Gemini melalui API key Google AI Studio. Ini contoh yang dipakai pada langkah berikut. |
| **NVIDIA NIM** | Pilih jika ingin model NVIDIA/Nemotron dan sudah menyiapkan NVIDIA API key. |
| **Nous Portal** | Pilih hanya jika memang memiliki akses/subscription Nous Portal. |
| **GitHub Copilot** | Pilih hanya jika akunmu memiliki akses Copilot yang sesuai dan kamu memang ingin memakai login Copilot. |
| Provider lain, misalnya Groq atau Mistral | Pilih jika kamu sengaja memakai provider itu dan sudah menyiapkan API key-nya. |
| **Cancel / X** | Jangan pilih kecuali ingin membatalkan pilihan provider. |

🟡 **Penting untuk screenshot:** angka dalam kurung, misalnya `NVIDIA NIM (82)` atau `Google AI Studio (16)`, adalah jumlah model yang ditampilkan pada katalog di picker tersebut—**bukan nomor pilihan yang harus diketik**. Klik label provider yang diinginkan. Jika tampilan terminal meminta nomor, masukkan nomor yang tertera di menu terminal itu.

### 3. Saat provider meminta cara login atau API key

- Jika memilih **Google AI Studio**, pilih alur **API key / Google AI Studio** jika ditawarkan, lalu tempel Google AI Studio API key di prompt terminal.
- Jika memilih **NVIDIA NIM**, pilih alur API key lalu tempel NVIDIA API key dari akun NVIDIA Developer.
- Jika memilih **Groq/Mistral**, masukkan key dari provider yang sama.
- Jika ditawari OAuth untuk layanan subscription, jangan pilih itu jika kamu hanya ingin memakai API key biasa.
- Jika ditanya Base URL dan kamu tidak memakai endpoint khusus, **tekan Enter untuk memakai default**.

🔴 Tempel API key di prompt terminal browser Railway yang sedang meminta key. **Jangan kirim API key ke chat Telegram/Discord dan jangan tempel ke GitHub.**

### 4. Saat daftar model muncul

| Provider yang dipilih | Model mana yang dipilih? |
|---|---|
| Google AI Studio | Pilih model **Gemini Flash** yang benar-benar tersedia di daftar untuk akunmu, untuk percakapan umum yang cepat. Jika tidak ada Flash, pilih model Gemini general-chat yang tersedia. |
| NVIDIA NIM | Pilih model **chat/instruct/general reasoning** yang dapat diakses oleh API key-mu. Jika ada pilihan gratis, pastikan model tersebut memang tersedia/berkuota pada akunmu. |
| Groq/Mistral | Pilih model **chat/instruct** yang tersedia dan sesuai kebutuhan; jangan memilih model embedding/reranker untuk percakapan. |

- Jika tidak yakin, pilih model chat/instruct yang ditandai default dan tersedia untuk akunmu.
- Jika pengaturan konteks ditampilkan, gunakan **64K token atau lebih** jika tersedia.
- Jika ditanya **Reasoning effort**, pilih `medium` sebagai awal untuk mengikuti instruksi dan tugas umum. Pilih `low` jika mengutamakan kecepatan dan tugasnya sederhana.
- Jangan memaksakan nama model dari tutorial jika tidak muncul pada daftar. Nama dan akses model bisa berubah.

### 5. Saat ditanya tool/fitur apa yang ingin diaktifkan

Gunakan tabel berikut sebagai pilihan praktis untuk **bot pribadi**. Kalau prompt tidak muncul, lewati saja—tidak perlu mencari menu yang tidak ditampilkan.

| Pilihan/fitur | Rekomendasi | Kapan? |
|---|---|---|
| **File Operations / File tools** | ✅ Aktifkan | Agar Hermes bisa membaca dan mengolah file yang diizinkan. |
| **Terminal & Processes / Terminal tools** | ✅ Aktifkan hanya untuk bot pribadi yang dibatasi ke ID-mu | Memungkinkan menjalankan perintah. Container ini berjalan sebagai root, jadi jangan buka aksesnya untuk publik. |
| **Web search / Web tools** | ✅ Aktifkan jika tersedia | Agar bisa mencari informasi. Pilih backend yang memang kamu punya akses/key-nya; jangan pilih Nous Subscription jika tidak berlangganan. |
| **Memory / Session search** | ✅ Aktifkan jika tersedia | Membantu konteks/memori dan pencarian sesi. Pastikan Volume `/opt/data` terpasang agar state persisten. |
| **Browser automation** | Opsional | Aktifkan jika memang perlu membuka dan berinteraksi dengan situs, dan backend-nya tersedia. Lewati cloud browser berbayar jika tidak punya akses. |
| **Code execution** | Opsional | Aktifkan untuk analisis/koding yang memerlukannya; kalau diaktifkan, batasi bot hanya untuk akun sendiri. |
| **Delegation / subagents** | Opsional | Aktifkan jika perlu tugas paralel; bisa menambah pemakaian model/API. Untuk menghemat kuota, lewati dulu. |
| **Skills bawaan** | Gunakan yang tersedia/default | Tidak perlu memasang semua skill tambahan. Pasang skill pihak ketiga hanya setelah memeriksa sumbernya. |
| **MCP servers / external integrations** | Skip / No bila belum punya server dan kredensialnya | Nanti bisa ditambahkan setelah dasar bot berjalan. |
| **Image generation** | Skip jika belum punya provider/key gambar khusus | API key untuk chat tidak otomatis memberi akses generate gambar. |
| **Voice / TTS** | Skip jika tidak perlu suara | Memerlukan dukungan/backend dan kadang key tersendiri. |
| **Home Assistant, Spotify, integrasi khusus** | Skip jika tidak dipakai | Aktifkan hanya jika memang punya layanan/credential terkait. |

🟡 Jika menu menggunakan **Yes/No** untuk tiap fitur, ikuti kolom rekomendasi di atas. Jangan memilih "Yes" untuk layanan eksternal hanya karena terlihat tersedia—fitur itu mungkin membutuhkan credential tambahan.

### 6. Saat ditanya backend terminal

- Pilih **Keep current (local)** atau **local** jika ditawarkan.
- Jangan memilih Docker backend pada template ini kecuali Docker-in-Docker memang sengaja disiapkan.
- Jika muncul opsi browser/cloud sandbox yang meminta akun atau API key tambahan, pilih Skip/No apabila belum menyiapkannya.

### 7. Saat ditanya memory, profile, atau setting lain

- **Memory provider:** gunakan built-in/default jika ditawarkan; jangan pilih layanan memory eksternal yang meminta akun/key tambahan.
- **Profile:** gunakan `default` jika itu profil utama yang muncul.
- **Compression/checkpoints/smart routing:** pertahankan default awal jika kamu belum tahu fungsinya.
- **Custom system prompt/personality:** tekan Enter untuk default, kecuali memang ingin menyesuaikan instruksi bot.
- **Install/enable optional plugins:** Skip/No untuk plugin yang belum diperlukan.

### 8. Saat ditanya platform messaging

- Pilih **Telegram** jika ingin menghubungkan Telegram sekarang.
- Pilih **Discord** juga hanya jika memang ingin menghubungkan Discord dan sudah menyiapkan bot Discord.
- Jika wizard menawarkan **Manual** dan bot Telegram sudah dibuat lewat BotFather, pilih **Manual**.
- Semua pilihan wizard dimasukkan di terminal browser Railway. Perintah `/newbot` saja yang dikirim ke akun resmi `@BotFather` di Telegram.

### 9. Saat setup menawarkan menyimpan, menerapkan, atau menyelesaikan konfigurasi

- Pilih **Save / Apply / Yes / Finish** untuk menyimpan konfigurasi yang baru saja dipilih.
- Jika terminal meminta konfirmasi untuk membatalkan atau menghapus konfigurasi, pilih **No / Cancel** kecuali memang sengaja ingin membatalkan.
- Tunggu sampai wizard selesai dan kembali ke prompt terminal. Setelah itu jalankan pemeriksaan pada bagian C8.

## C6. Konfigurasi provider/model

Ikuti prompt versi Hermes yang tampil. Contoh alur Google AI Studio:

1. Pilih **Google AI Studio (Native Gemini API)** jika tersedia.
2. Tempel API key saat diminta.
3. Untuk Base URL, tekan Enter untuk memakai default jika prompt menyediakan default.
4. Pilih model yang tersedia untuk akunmu.
5. Pilih opsi reasoning yang diinginkan jika prompt muncul.
6. Untuk terminal backend, pilih **Keep current (local)** jika ditampilkan.

🟡 Jangan mengetik model ID contoh jika model tersebut tidak ada dalam daftar atau tidak tersedia di akun provider.

## C7. Hubungkan Telegram

1. Di daftar platform messaging, pilih **Telegram**.
2. Jika bot sudah dibuat lewat BotFather, pilih metode **Manual**.
3. Jika label Manual berada di opsi **2**, masukkan/pilih `2` pada terminal browser. Jika nomor berbeda, ikuti nomor yang tampil di layar.
4. Buka Telegram dan cari `@BotFather`.
5. Jika belum punya bot, kirim `/newbot` dan ikuti instruksi.
6. Salin token dari BotFather.
7. Kembali ke terminal browser; tempel token ketika wizard meminta token.
8. Saat diminta **Allowed user IDs**, masukkan ID Telegram numerik milikmu, bukan username atau token.
9. Jika ditanya **Use your user ID as the home channel?**, pilih **Yes** untuk penggunaan pribadi.
10. Tuntaskan seluruh prompt sampai setup selesai.

📌 Pilihan **Manual / angka 2** diketik di terminal browser. Jangan mengirim angka itu sebagai pesan ke bot Telegram.

Jika ingin mengubah platform messaging kemudian, gunakan `hermes gateway setup` dari terminal yang sama.

## C8. Pastikan konfigurasi sudah tersimpan

Ketik:

~~~bash
test -f /opt/data/config.yaml && echo "OK: konfigurasi ditemukan" || echo "Setup belum selesai"
~~~

✅ Hasil benar: `OK: konfigurasi ditemukan`.

Jika muncul `Setup belum selesai`, jalankan kembali `hermes setup` dan tuntaskan prompt yang belum selesai. Jangan menjalankan perintah uninstall yang dapat menghapus data.

## C9. Mulai dan tes Gateway

1. Buka Railway → **Hermes-Ubuntu → Deploy Logs**.
2. Setelah setup selesai, jika Gateway belum mulai, lakukan **restart service satu kali** dari Railway.
3. Tunggu log Gateway dan pastikan tidak ada error startup.
4. Buka Telegram → chat pribadi dengan bot.
5. Kirim `/start`, lalu kirim: `Halo, balas OK.`

✅ Setup berhasil saat Gateway aktif **dan bot benar-benar membalas pesan**.

🟡 Screenshot sebelumnya menunjukkan pesan bahwa setup Telegram terlihat selesai tetapi Gateway belum melaporkan koneksi. Dalam kondisi itu, periksa Deploy Logs; dengan `HERMES_AUTOSTART=true`, restart service sekali jika konfigurasi sudah ada. Jangan menjalankan Gateway manual bersamaan dengan auto-start.

## C10. Jika Telegram tetap diam

Periksa urutan berikut:

1. Pastikan file `/opt/data/config.yaml` ditemukan.
2. Pastikan `HERMES_AUTOSTART=true`.
3. Periksa **Deploy Logs** setelah service direstart.
4. Pastikan API key/provider/model berfungsi.
5. Pastikan token Telegram benar dan ID pengguna masuk allowlist.
6. Pastikan service lain tidak memakai token bot yang sama.
7. Uji melalui DM terlebih dahulu, bukan grup.

🔴 Jangan menjalankan `start-hermes` atau `hermes gateway run` ketika `HERMES_AUTOSTART=true` dan Gateway sudah dikelola otomatis.

---

## 3. Pemeriksaan akhir untuk semua mode

| Pemeriksaan | Dashboard | Variables | Ubuntu |
|---|---|---|---|
| Dockerfile Path | `Dockerfile` | `Dockerfile` | `ubuntu/Dockerfile` |
| Root Directory | Kosong | Kosong | Kosong |
| Volume | `/opt/data` sendiri | `/opt/data` sendiri | `/opt/data` sendiri |
| Domain | Ya, target 8080 | Tidak perlu | Ya, target 8080 |
| Kredensial | `USERNAME`, `PASSWORD`, `SECRET` | API key + token platform | `TERMINAL_USER`, `TERMINAL_PASSWORD` |
| Verifikasi akhir | Login Dashboard berhasil | Gateway dan balasan bot berhasil | CLI setup selesai dan bot membalas |

### Arti error yang sering muncul

| Error | Langkah pertama |
|---|---|
| `Application failed to respond` | Periksa Deploy Logs, Build settings, dan target port 8080 untuk Dashboard/Ubuntu |
| `SECRET must be at least 32 characters` | Buat secret acak yang lebih panjang dan redeploy |
| `No provider API key found` | Isi setidaknya satu API key yang valid pada Variables |
| HTTP 401 / Unauthorized | Periksa API key, provider, dan endpoint |
| HTTP 429 / quota | Periksa kuota atau batas permintaan provider |
| Model not found | Pilih model yang tersedia untuk API key-mu |
| Telegram conflict / `getUpdates` | Matikan Gateway lain yang memakai token sama |
| Telegram setup selesai, bot diam | Periksa Gateway di Deploy Logs, allowlist, token, dan provider |

🔴 Jangan bagikan API key, token bot, password, isi konfigurasi, atau log yang masih memuat rahasia.

