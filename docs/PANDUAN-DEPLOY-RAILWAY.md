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

🧰 **Kalau men-deploy dari fork/salinan repo ini**, sebelum build periksa dulu baris instalasi adapter messaging di `ubuntu/Dockerfile` (dekat komentar "Telegram and Discord are optional Hermes extras"). Versi yang benar memakai:

```dockerfile
RUN cd /usr/local/share/hermes-agent && \
    python3 -c "from pm import sync_venv; sync_venv(['all', 'messaging'], explicit=True)"
```

Bukan `hermes pm install --extra all --extra messaging` — perintah itu tidak valid (`hermes pm install` tidak punya flag `--extra`) dan menyebabkan adapter Telegram/Discord tidak terpasang walau build terlihat sukses, sehingga bot tidak pernah bisa membalas. Repo resmi `DURIAN-ORGANISASI/hermes-railway` branch `main` (commit `b511baa` ke atas) sudah memakai versi yang benar.

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

Perintah `hermes setup` dijalankan di **terminal browser Railway**. Prompt dari wizard CLI dijawab di terminal. Jika yang kamu lihat adalah menu/pertanyaan terpisah yang dikirim bot di chat Telegram, pilih tombol atau balas angka di chat Telegram yang sama—ikuti instruksi di layar tersebut.

Ketik:

~~~bash
hermes setup
~~~

1. Pilih **Full setup**.
2. Jika menu bergerak, gunakan tombol panah lalu Enter.
3. Jika prompt meminta nomor, ketik nomor di samping pilihan yang sesuai, lalu Enter.
4. Lanjutkan ke pengaturan provider/model.

🔴 Nomor opsi dapat berbeda menurut versi wizard. Ikuti label dan angka yang tampil pada layar yang sedang bertanya.

**Jangan tertukar tempat menjawab:**
- Prompt yang muncul di **terminal browser Railway** dijawab di terminal itu.
- Jika bot mengirim menu/pertanyaan di **chat Telegram** dan meminta balasan angka (misalnya `1` atau `2`), kirim angka itu sebagai balasan pada **chat Telegram yang sama**.
- Jika Telegram menampilkan tombol pilihan, ketuk tombolnya langsung.
- Jangan menyalin angka dari satu layar ke layar lain. Ikuti instruksi pada layar tempat pilihan muncul.

## C5A. Peta pilihan wizard — isi menu satu per satu

**Ikuti tabel ini saat menu muncul.** Nama opsi bisa sedikit berbeda antarversi. Pilih berdasarkan label yang terlihat, bukan nomor yang dihafal.

### 1. Pilih jenis setup

| Opsi | Pilihan | Kenapa |
|---|---|---|
| **Full Setup** | ✅ PILIH | Konfigurasi provider, model, tools, dan platform secara lengkap. |
| Quick Setup / Nous Portal | ❌ Lewati | Memakai alur Nous Portal; bukan pilihan utama jika memakai API key provider sendiri. |
| Blank Slate | ❌ Lewati | Konfigurasi minimal dan banyak hal perlu diatur manual. |

### 2. Pilih provider AI

| Opsi di menu | Pilihan untuk kebutuhanmu |
|---|---|
| **Google AI Studio / Native Gemini API** | ✅ Pilih jika menggunakan Gemini dan punya Google AI Studio API key. |
| **NVIDIA NIM** | ✅ Pilih jika ingin NVIDIA/Nemotron dan punya NVIDIA API key. |
| **Groq** | Pilih jika API key Groq sudah tersedia dan ingin model Groq. |
| **Mistral** | Pilih jika API key Mistral sudah tersedia dan ingin model Mistral. |
| **Nous Portal** | ❌ Lewati jika tidak punya akses/subscription Nous Portal. |
| **GitHub Copilot** | ❌ Lewati kecuali akun dan paket Copilot memang mendukung integrasi ini. |
| **Other / Custom OpenAI-compatible** | Pilih hanya jika memang punya Base URL dan API key provider yang kompatibel. |
| **Cancel / Back** | Jangan pilih kecuali ingin kembali atau membatalkan. |

🟡 Jika daftar menunjukkan `NVIDIA NIM (82)` atau `Google AI Studio (16)`, angka dalam kurung adalah jumlah model yang tercantum, bukan nomor opsi.

### 3. Pilih metode autentikasi

| Opsi | Yang harus dilakukan |
|---|---|
| **API key** | ✅ Pilih untuk memakai key provider sendiri. |
| **OAuth / Sign in / Browser login** | Lewati jika kamu tidak ingin login akun dan hanya ingin memakai API key. |
| **Base URL** | Tekan Enter untuk default jika memakai endpoint resmi. Isi hanya jika provider meminta URL khusus. |
| **API key / Token** | Tempel key milik provider yang dipilih. Jangan menempelkan key NVIDIA ke kolom Google, atau sebaliknya. |
| **Skip / Cancel** | Jangan dipilih jika itu membuat provider tidak terkonfigurasi. |

### 4. Pilih model

| Provider | Pilih |
|---|---|
| **Google AI Studio** | Model **Gemini Flash** yang tersedia untuk API key-mu, untuk chat umum yang cepat. |
| **NVIDIA NIM** | Model **chat/instruct/reasoning** yang tersedia untuk akunmu. Jika ada Nemotron yang bisa diakses, pilih itu untuk percakapan dan instruksi. |
| **Groq** | Model **chat/instruct** yang tersedia di akun Groq. |
| **Mistral** | Model **chat/instruct** yang tersedia di akun Mistral. |

- ❌ Jangan memilih model embedding, reranker, image-only, atau audio-only untuk bot chat teks.
- Jika ada opsi **Default / Recommended** dan kamu tidak yakin, pilih itu.
- Jika ditanya **Reasoning effort**, pilih `medium` untuk instruksi dan tugas umum; pilih `low` untuk kecepatan.
- Jika ditanya **Context length**, biarkan default atau pilih nilai yang didukung model. Jangan memaksakan nilai yang tidak tersedia.
- Jika model yang diinginkan tidak terlihat, pilih model chat yang memang muncul dan dapat diakses.

### 5. Pilih tools / kemampuan

Gunakan tabel ini jika wizard menampilkan pertanyaan Yes/No atau menu pemilihan tools.

| Opsi | Pilihan | Alasan |
|---|---|---|
| **Web Search / Web Tools** | ✅ Aktifkan jika ada backend gratis/yang sudah punya key | Agar bot dapat mencari informasi online. Jika backend meminta key berbayar yang tidak kamu punya, Skip. |
| **File Operations / File Tools** | Opsional; aktifkan jika ingin bot mengolah file | Tidak wajib untuk chat biasa. |
| **Terminal / Shell / Processes** | ⚠️ Untuk bot pribadi saja; jika hanya chat, Skip dulu | Bisa menjalankan perintah pada lingkungan container. Jangan beri akses ke pengguna umum. |
| **Code Execution** | Skip untuk chat biasa; aktifkan hanya jika perlu coding/eksekusi | Menambah kemampuan sekaligus risiko eksekusi. |
| **Browser Automation / Computer Use** | Skip jika belum menyiapkan browser/backend-nya | Bisa membutuhkan komponen atau konfigurasi tambahan. |
| **Memory / Session Search** | ✅ Aktifkan jika tersedia dan ingin konteks tersimpan | Pastikan Volume `/opt/data` terpasang. |
| **Skills** | Pertahankan default; aktifkan skill tertentu hanya jika dibutuhkan | Tidak perlu mengaktifkan semua skill. |
| **Subagents / Delegation** | Skip untuk awal | Bisa menambah panggilan model dan pemakaian kuota. |
| **MCP Servers / External Integrations** | Skip / No jika belum punya server dan credential | Baru aktifkan jika alamat server dan autentikasi sudah tersedia. |
| **Image Generation** | Skip jika belum menyiapkan provider gambar | API key chat tidak otomatis mendukung pembuatan gambar. |
| **Voice / TTS / Speech** | Skip jika bot teks saja | Memerlukan dukungan atau provider tambahan. |
| **Home Assistant / Spotify / integrasi khusus** | Skip jika tidak digunakan | Hanya perlu jika memang memakai layanan tersebut. |

### 6. Pilih terminal / execution backend

| Opsi | Pilihan |
|---|---|
| **Keep current (local) / Local** | ✅ Pilih jika tersedia. |
| **Docker backend** | Skip kecuali Docker-in-Docker sudah sengaja disiapkan. |
| **Cloud sandbox / Remote browser** | Skip jika meminta akun, key, atau layanan tambahan yang belum kamu punya. |

### 7. Pilih memory, profile, dan konfigurasi lain

| Pertanyaan | Jawaban yang disarankan |
|---|---|
| **Profile** | `default`, jika tersedia. |
| **Memory provider** | Built-in/default; jangan pilih layanan eksternal yang meminta key tambahan. |
| **Custom system prompt / personality** | Tekan Enter untuk default jika belum punya instruksi khusus. |
| **Compression / checkpoints / smart routing** | Pertahankan default awal. |
| **Install optional plugins?** | No / Skip untuk plugin yang belum diperlukan. |
| **Save / Apply / Finish?** | Yes / Save / Apply untuk menyimpan konfigurasi. |
| **Delete / reset / overwrite config?** | No / Cancel kecuali memang sengaja ingin menghapus atau menimpa konfigurasi. |

### 8. Pilih platform chat

| Opsi | Pilihan |
|---|---|
| **Telegram** | ✅ Pilih untuk menghubungkan bot Telegram. |
| **Discord** | Pilih juga jika ingin bot Discord dan sudah punya token bot Discord. |
| **Slack / WhatsApp / platform lain** | Skip jika tidak digunakan atau belum menyiapkan kredensialnya. |
| **Manual** | Pilih jika bot Telegram sudah dibuat lewat `@BotFather` dan kamu akan memasukkan token sendiri. |

**PENTING — di mana memasukkan angka?**

- Jika prompt ada di terminal browser Railway, jawab di terminal tersebut.
- Jika bot mengirim pilihan berbentuk tombol di Telegram, ketuk tombolnya.
- Jika bot di Telegram meminta balasan angka `1` atau `2`, kirim angka itu di chat Telegram yang sama.
- Jangan menebak nomor opsi dari tutorial; nomor dan urutannya bisa berbeda.

### 9. Pengaturan akses bot

| Pertanyaan | Pilihan |
|---|---|
| **Allowed user IDs** | Masukkan ID numerik milikmu; jangan masukkan username atau token bot. |
| **Allow all users?** | ❌ No untuk bot pribadi. |
| **Use your user ID as home channel?** | ✅ Yes untuk penggunaan pribadi, jika opsi ini muncul. |
| **Allowed channels / Free response channels** | Batasi ke channel yang memang ingin digunakan. Lewati dulu jika belum perlu. |
| **Create a thread automatically?** | No / false jika tidak ingin bot membuat thread otomatis. |

### 10. Setelah wizard selesai

1. Pilih **Save / Apply / Finish** jika diminta.
2. Tunggu sampai wizard selesai dan kembali ke prompt terminal.
3. Periksa konfigurasi dengan perintah pada bagian C8.
4. Buka Railway → **Deploy Logs**.
5. Restart service satu kali jika konfigurasi sudah tersimpan tetapi Gateway belum mulai.
6. Uji chat pribadi dengan `/start`, lalu kirim `Halo, balas OK.`

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

📌 **Di mana memilih Manual?** Jika pertanyaannya muncul pada terminal browser, pilih di terminal. Jika menu dikirim sebagai tombol oleh bot di Telegram, ketuk **Manual** di Telegram; jika bot meminta angka, balas angka pada chat Telegram yang sama. Ikuti tempat pertanyaan itu muncul.

Perintah `/newbot` dikirim ke akun resmi `@BotFather` di Telegram. Token BotFather kemudian ditempel ke kolom/prompt token pada layar setup yang sedang digunakan.

Jika ingin mengubah platform messaging kemudian, gunakan `hermes gateway setup` dari terminal yang sama.

### C7A. Jika juga ingin memakai Discord

Lakukan bagian ini hanya jika memang ingin bot membalas di Discord. Jika wizard menanyakan platform, pilih **Discord**.

1. Buka Discord Developer Portal: https://discord.com/developers/applications.
2. Pilih aplikasimu atau klik **New Application**.
3. Buka menu **Bot** dan buat bot jika belum ada.
4. Salin **Bot Token**. Tempel token ke prompt yang sedang meminta token—jangan kirim ke chat publik.
5. Pada daftar **Allowed user IDs**, masukkan ID numerik akun Discord milikmu. Aktifkan **Developer Mode** di Discord → User Settings → Advanced, lalu klik kanan profilmu → **Copy User ID**.
6. Di Developer Portal → **Bot → Privileged Gateway Intents**, aktifkan **Message Content Intent**, lalu Save Changes.
7. Undang bot ke server melalui **OAuth2 → URL Generator**. Pilih scope `bot` dan izin minimum seperti View Channels, Send Messages, dan Read Message History.
8. Untuk pengujian pertama, kirim DM langsung ke bot. Di server, mention bot dengan `@nama-bot`; bot biasanya tidak menjawab semua pesan channel tanpa mention.
9. Bila wizard bertanya **Allow all users?**, pilih **No**. Batasi akses ke ID milikmu.
10. Bila ditanya channel bebas mention, lewati dulu. Atur channel khusus setelah bot berhasil membalas DM.

🟡 Jangan gunakan token akun pengguna atau self-bot. Pakai token bot resmi dari Developer Portal.

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
8. Jalankan `hermes doctor` di terminal dan cek baris `python-telegram-bot` di bagian **Required Packages** — harus ada tanda centang. Kalau tidak, image belum memasang adapter messaging dengan benar (lihat C10A).
9. Kalau kamu baru saja menjalankan ulang `hermes setup` pada service yang Gateway-nya **sudah pernah jalan sebelumnya**, Gateway lama kemungkinan masih pakai config lama di memori — lihat C10A untuk cara memastikan Gateway reload.

🔴 Jangan menjalankan `start-hermes` atau `hermes gateway run` ketika `HERMES_AUTOSTART=true` dan Gateway sudah dikelola otomatis.

## C10A. Pelajaran penting: Gateway tidak otomatis reload config baru

Kasus nyata yang pernah terjadi: setup Telegram sudah benar, adapter messaging sudah terpasang, tapi bot tetap diam. Penyebabnya Gateway yang **sudah berjalan sejak sebelum** `hermes setup` dijalankan ulang (misalnya setelah ganti token atau provider) tidak otomatis membaca ulang `config.yaml` — proses lama tetap jalan dengan config lama di memori.

Cara memastikan Gateway benar-benar pakai config terbaru, di terminal browser Railway:

1. `hermes gateway status` — catat PID yang sedang aktif.
2. `tail -n 100 /opt/data/logs/gateway.log` — kalau ada baris `No messaging platforms enabled`, itu tandanya Gateway proses tersebut start **sebelum** Telegram dikonfigurasi.
3. `kill <PID>` (PID dari langkah 1) — dengan `HERMES_AUTOSTART=true`, supervisor otomatis di `entrypoint.sh` akan menjalankan ulang Gateway dalam ~5 detik memakai config terbaru. Ini aman: bukan `kill -9`, Gateway akan shutdown bersih lalu supervisor merestartnya.
4. `hermes gateway status` lagi sampai muncul PID baru, lalu cek log sekali lagi — harus muncul `Connecting to telegram...` lalu `Cold boot: dropping Telegram updates...`. Itu tanda Telegram berhasil connect.

🔴 Lakukan langkah ini setiap kali selesai mengubah konfigurasi messaging (`hermes setup` atau `hermes setup gateway`) pada service yang Gateway-nya sudah pernah berjalan — jangan hanya mengandalkan prompt "Restart the gateway to pick up changes?" di dalam wizard, karena restart itu bisa gagal diam-diam kalau lock Gateway sedang dipegang proses supervisor lain.

## C10B. Ringkasan perintah diagnostik cepat

| Perintah | Fungsinya |
|---|---|
| `test -f /opt/data/config.yaml && echo OK \|\| echo BELUM` | Cek apakah setup sudah pernah disimpan |
| `hermes doctor` | Cek kesehatan instalasi — provider, adapter messaging, dependency |
| `hermes gateway status` | Lihat apakah Gateway jalan dan PID-nya |
| `tail -n 100 /opt/data/logs/gateway.log` | Baca log startup Gateway — cari status koneksi Telegram |
| `kill <PID>` | Paksa Gateway restart supaya baca config terbaru (auto-restart via supervisor) |
| `hermes setup` | Jalankan ulang wizard lengkap kapan saja untuk ubah provider/model/messaging |
| `hermes setup gateway` | Ubah konfigurasi messaging saja tanpa mengulang semua langkah |

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
| Gateway jalan tapi `No messaging platforms enabled` di log | Gateway start sebelum Telegram dikonfigurasi — lihat C10A, `kill <PID>` lalu biarkan supervisor restart otomatis |
| `hermes doctor` tidak menandai `python-telegram-bot` | Image belum memasang adapter messaging dengan benar — pastikan `ubuntu/Dockerfile` pakai `sync_venv(['all', 'messaging'], explicit=True)`, lalu build ulang |

🔴 Jangan bagikan API key, token bot, password, isi konfigurasi, atau log yang masih memuat rahasia.



## C5B. Urutan jawaban siap ikuti (untuk bot pribadi)

Bagian ini adalah jalur rekomendasi untuk **satu bot pribadi Telegram**. Gunakan pilihan yang setara jika teks menu sedikit berbeda. **Jangan menebak nomor opsi**: pilih labelnya atau gunakan nomor yang tampil di layar saat itu.

| Urutan layar/prompt | Pilih atau ketik | Catatan |
|---|---|---|
| Setup type / setup mode | **Full Setup** | Jangan pilih Blank Slate. |
| Provider | **NVIDIA NIM** jika memakai NVIDIA API key; jika tidak, pilih provider yang key-nya sudah kamu punya | Jangan pilih provider hanya karena namanya terlihat populer. |
| Authentication method | **API key** | Hindari OAuth/browser login jika memang memakai API key. |
| API key / token | Tempel key provider yang dipilih | Nilai rahasia; jangan masukkan ke repo atau screenshot publik. |
| Base URL | Tekan **Enter** untuk default | Hanya isi URL khusus jika memang disediakan provider/proyekmu. |
| Model | Pilih model **chat / instruct / reasoning** yang tersedia | Jangan pilih embedding, reranker, image-only, atau audio-only. Nama dan ketersediaan model bergantung pada akun provider. |
| Reasoning effort | **medium** | Jika mengutamakan respons cepat, pilih **low**. Jika prompt tidak muncul, lanjutkan. |
| Context length | **Default / Recommended** | Jangan masukkan angka yang tidak ditawarkan di menu. |
| Web search / web tools | **Enable/Yes** hanya jika backend pencarian sudah dikonfigurasi; jika meminta API key yang belum ada, **Skip/No** | Mengaktifkan tool tanpa backend/key tidak otomatis membuat pencarian berfungsi. |
| File tools | **Enable/Yes** jika memang ingin membaca/mengelola file; selain itu **Skip/No** | Boleh diaktifkan nanti. |
| Terminal / shell / code execution | **Skip/No** untuk awal | Kurangi risiko perintah sistem dieksekusi oleh bot. |
| Browser automation / computer use | **Skip/No** | Aktifkan hanya setelah backend browser disiapkan. |
| Memory / session search | **Enable/Yes** jika tersedia | Volume `/opt/data` harus sudah terpasang. |
| Skills | **Default** | Tidak perlu memilih semua skill. |
| Subagents / delegation | **Skip/No** untuk awal | Mengurangi kompleksitas dan pemakaian model. |
| MCP / external integrations | **Skip/No** jika belum ada server dan kredensial | Isi hanya jika sudah punya endpoint dan autentikasi. |
| Image generation / voice / TTS | **Skip/No** untuk bot teks | Provider chat biasa tidak otomatis menyediakan fitur ini. |
| Terminal backend | **Keep current / Local** | Jangan pilih Docker atau Cloud Sandbox kecuali sengaja sudah menyiapkannya. |
| Profile | **default** jika tersedia | Jika tidak ditanya, lanjutkan. |
| System prompt / personality | Tekan **Enter** untuk default | Tambahkan instruksi khusus nanti bila diperlukan. |
| Optional plugins | **No/Skip** | Bisa dipasang setelah konfigurasi dasar berhasil. |
| Messaging platform | **Telegram** | Tambahkan Discord hanya jika benar-benar ingin menggunakannya juga. |
| Telegram setup method | **Manual** jika bot sudah dibuat melalui `@BotFather` | Pilih labelnya, bukan nomor yang diingat dari tutorial. |
| Telegram bot token | Tempel token dari `@BotFather` | Tempel di prompt token yang sedang aktif; jangan kirim ke repo. |
| Allowed user IDs | Masukkan **ID numerik akun Telegram milikmu** | Bukan username, nomor telepon, atau token bot. |
| Allow all users? | **No** | Lebih aman untuk bot pribadi. |
| Use your user ID as home channel? | **Yes** jika ingin penggunaan pribadi | Jika pertanyaan ini tidak muncul, lanjutkan. |
| Allowed channels / free-response channels | Batasi ke channel yang memang diperlukan; untuk tes awal, jangan buka akses umum | Jika tidak tahu ID channel atau belum perlu, biarkan kosong/skip sesuai prompt. |
| Auto-create threads | **No** untuk awal | Terutama jika ingin menghindari thread otomatis di Discord. |
| Save / Apply / Finish | **Yes / Save / Apply / Finish** | Ini menyimpan konfigurasi wizard. |
| Overwrite/delete/reset existing config? | **No/Cancel** kecuali sengaja ingin menimpa | Hindari kehilangan konfigurasi yang sudah berjalan. |

### Di layar mana jawaban dimasukkan?

- **Terminal CLI:** ketik jawaban di terminal browser Railway yang menjalankan `hermes setup`; tekan Enter setelah memilih/mengetik.
- **Menu tombol Telegram:** tekan tombol pada pesan Telegram itu sendiri.
- **Bot Telegram meminta angka sebagai balasan:** kirim angka tersebut di chat Telegram yang sama.
- **Token/API key:** tempel hanya pada prompt yang secara khusus meminta token/key. Jangan menempelkannya ke kolom user ID, channel ID, atau model.
- **Pilihan menu bernomor:** nomor bisa berubah menurut versi. Contoh: jika layar saat ini menampilkan `1. Telegram` dan `2. Discord`, pilih nomor yang cocok pada layar tersebut—bukan nomor dari screenshot versi lain.

### Setelah selesai, verifikasi sebelum mengubah hal lain

1. Jalankan pemeriksaan file di bagian **C8**.
2. Buka **Railway → Deployments → Deploy Logs**.
3. Pastikan tidak ada error API key, model, atau token platform.
4. Jika Gateway belum mulai setelah konfigurasi tersimpan, restart service **satu kali**.
5. Tes DM Telegram dengan `/start`, lalu kirim `Halo, balas OK.`.
6. Jika bot tetap diam, jangan mengulang setup secara acak. Catat error pertama di Deploy Logs dan cocokkan dengan bagian **C10**.

> **Batas akurasi:** nama menu dan urutan opsi dapat berbeda antarversi Hermes. Tabel ini memetakan keputusan yang disarankan berdasarkan label umum; untuk memastikan setiap opsi sama persis dengan screenshot wizard milikmu, screenshot menu tersebut perlu tersedia saat panduan diperbarui.
