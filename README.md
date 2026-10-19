<div align="center">

<img src="docs/brand.svg" alt="Hermes Agent Railway" width="84" height="84">

<h1>Hermes Agent Railway</h1>

<p><a href="https://github.com/DURIAN-ORGANISASI/hermes-railway/actions/workflows/validate.yml"><img alt="Validation workflow configured; see Actions for live status" src="https://img.shields.io/badge/validation-configured-2088FF?logo=githubactions&amp;logoColor=white"></a> <a href="LICENSE"><img alt="Project license: MIT" src="https://img.shields.io/badge/project_license-MIT-blue.svg"></a> <img alt="Railway" src="https://img.shields.io/badge/Deploy-Railway-0B0D0E?logo=railway&amp;logoColor=white"> <img alt="Docker" src="https://img.shields.io/badge/Container-Docker-2496ED?logo=docker&amp;logoColor=white"></p>

<p><a href="README.md">🇮🇩 Bahasa Indonesia</a> · <a href="README.en.md">🇬🇧 English</a></p>

<p><strong>Jalankan Hermes Agent di Railway.</strong><br>
Tersedia tiga mode: Dashboard, Railway Variables, dan Ubuntu Terminal.</p>

<p><a href="#fitur">Fitur</a> · <a href="#pilih-mode">Mode deployment</a> · <a href="#deploy-ke-railway">Deploy</a> · <a href="#keamanan-dashboard">Keamanan</a> · <a href="#sumber-atribusi-dan-lisensi">Sumber &amp; lisensi</a></p>

</div>

![Ikhtisar Hermes Agent Railway](docs/hero.id.svg)
<p align="center"><sub>Ilustrasi orisinal untuk dokumentasi — bukan aset atau screenshot resmi Hermes Agent/Railway.</sub></p>

<p align="center"><sub>Badge validation menandakan workflow tersedia, bukan status lulus/gagal secara langsung. Buka <a href="https://github.com/DURIAN-ORGANISASI/hermes-railway/actions">Actions</a> untuk hasil terbaru.</sub></p>

> [!WARNING]
> **Dashboard di domain publik:** mode Dashboard memakai autentikasi username/password dasar. Dokumentasi resmi Hermes menyarankan metode ini hanya untuk jaringan tepercaya atau VPN, bukan untuk mengekspos Dashboard langsung ke internet. Railway public domain dapat diakses dari internet. Sebelum membuka Dashboard secara publik, konfigurasikan OAuth/OIDC atau access gateway tepercaya. Repo ini tidak mengatur OAuth/OIDC secara otomatis. Baca [Keamanan Dashboard](#keamanan-dashboard).

## Ringkasan

Repo ini menyediakan tiga mode deployment yang dapat berjalan bersamaan sebagai tiga Railway service terpisah. Dashboard dan Variables memakai image Hermes upstream; Ubuntu memakai Dockerfile Ubuntu khusus di `ubuntu/Dockerfile`.

| Mode | Tujuan | Variabel utama |
| --- | --- | --- |
| **Dashboard** | Antarmuka web untuk mengelola Hermes. | `USERNAME`, `PASSWORD`, `SECRET` |
| **Railway Variables** | Gateway Telegram/Discord tanpa Dashboard web. | Minimal satu API key provider; token chat opsional |
| **Ubuntu Terminal** | Terminal Ubuntu 26.04 via browser, Hermes CLI, dan Gateway opsional. | `TERMINAL_USER`, `TERMINAL_PASSWORD`, `HERMES_AUTOSTART` |

> [!IMPORTANT]
> **Token bot harus dimiliki satu service saja.** Mode Dashboard dan Variables sama-sama menjalankan Gateway; Ubuntu juga dapat menjalankannya jika `HERMES_AUTOSTART=true`. Jangan salin token Telegram/Discord yang sama ke beberapa service sekaligus. Pilih satu service untuk setiap bot, atau gunakan token bot berbeda, agar beberapa Gateway tidak berebut menerima event/pembaruan.
 
## Fitur

- **Tiga mode deployment:** Dashboard dan Variables dipilih melalui `DEPLOY_MODE`; Ubuntu memakai Dockerfile terpisah yang dipilih melalui `RAILWAY_DOCKERFILE_PATH` agar basis OS dan fungsi terminal tidak mengubah image Hermes upstream.
- **Data terpisah:** setiap service memiliki Volume Railway sendiri di `/opt/data`; jangan menggunakan atau memasang ulang volume yang sama pada service lain.
- **Pemilihan model otomatis:** mode Variables memprioritaskan Groq → Mistral → NVIDIA → Gemini; provider aktif selanjutnya dikonfigurasi sebagai fallback.
- **Integrasi chat:** Telegram/Discord dengan allowlist pengguna dan channel pada mode yang dikonfigurasi.
- **Ubuntu Terminal:** mempertahankan `ttyd`, autentikasi terminal, banner sistem, Git/Python, dan Gateway opsional; file terminal dapat dipersistenkan terpisah di `/data`.
- **Dokumentasi terawat:** sumber dan lisensi, kebijakan keamanan, contoh environment, serta pemeriksaan CI.

## Pilih mode

### 1. Dashboard

Mode default bila `DEPLOY_MODE` tidak diatur. Tambahkan di **Railway → service Dashboard → Variables**:

Salin blok variabel ini ke **Railway → Hermes-Dashboard → Variables**. Ganti seluruh nilai contoh sebelum menyimpan:

```dotenv
DEPLOY_MODE=dashboard
USERNAME=ganti_dengan_username
PASSWORD=GANTI_DENGAN_PASSWORD_UNIK_YANG_KUAT
SECRET=GANTI_DENGAN_SECRET_ACAK_MINIMAL_32_KARAKTER
HERMES_HOME=/opt/data
TZ=Asia/Jakarta
PORT=8080
```

- `USERNAME` dan `PASSWORD` mengatur login Dashboard. `SECRET` wajib minimal 32 karakter; hasilkan dengan `openssl rand -hex 32` di terminal dan jangan gunakan nilai dari dokumentasi.
- Pasang Railway Volume pada `/opt/data`.
- `PORT=8080` dipakai pada konfigurasi domain Railway contoh di repo ini. Di **Settings → Networking**, pastikan target port domain sama dengan port aplikasi, yaitu `8080`. Jika port aplikasi diubah, samakan juga target domain.
- Setelah kredensial disimpan, deploy/restart service dan cek **Deploy Logs** serta halaman login. Status deploy `SUCCESS` saja belum membuktikan HTTP bisa diakses.
- Setelah akses diamankan, atur provider/model dan integrasi chat mengikuti dokumentasi resmi Hermes.

> [!IMPORTANT]
> Basic username/password bukan pengganti OAuth/OIDC untuk Dashboard yang terbuka ke internet. Gunakan OAuth/OIDC atau access gateway yang benar-benar membatasi akses bila memakai domain publik.

### 2. Railway Variables

Mode ini tidak menyalakan Dashboard. Tambahkan variabel di **Railway → service Variables → Variables**. Minimal satu API key provider harus diisi; provider lain boleh kosong atau tidak dibuat.

Salin blok lengkap ini ke **Railway → Hermes-Variables → Variables**. API key dan token yang tidak digunakan boleh dibiarkan kosong atau tidak dibuat:

```dotenv
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
```

Wajib: isi minimal satu provider key yang valid. Nilai kosong di atas hanya placeholder, bukan kredensial aktif. Untuk bot, isi token dan allowlist yang benar-benar dibutuhkan.

Contoh minimal untuk NVIDIA saja:

    DEPLOY_MODE=variables
    NVIDIA_API_KEY=isi_api_key_nvidia

`GOOGLE_API_KEY` diterima sebagai alias Gemini jika `GEMINI_API_KEY` kosong.

#### Urutan provider dan model startup

| Prioritas | Variabel | Model default startup |
| ---: | --- | --- |
| 1 | `GROQ_API_KEY` | `openai/gpt-oss-20b` |
| 2 | `MISTRAL_API_KEY` | `ministral-3b-latest` |
| 3 | `NVIDIA_API_KEY` | `nvidia/nemotron-3.5-super-vl-120b-a12b` |
| 4 | `GEMINI_API_KEY` / `GOOGLE_API_KEY` | `gemini-3.8-flash` |

Model ID default diperiksa pada 18 Oktober 2026 berdasarkan dokumentasi penyedia. Harga, kuota, dan ketersediaan bisa berubah; periksa akses model di akun provider sebelum deploy. Fallback hanya berlaku pada jenis error yang didukung Hermes/provider; tidak semua limit atau error autentikasi dialihkan otomatis.

> [!NOTE]
> Mode Variables membuat ulang `/opt/data/config.yaml` setiap startup dari API key aktif. Jadikan Railway Variables sebagai sumber konfigurasi; edit manual file yang dihasilkan dapat tertimpa.

#### Variabel Telegram dan Discord

| Variabel | Fungsi |
| --- | --- |
| `TELEGRAM_BOT_TOKEN` | Token bot dari [BotFather](https://core.telegram.org/bots#botfather). |
| `TELEGRAM_ALLOWED_USERS` | ID pengguna Telegram yang diizinkan; ikuti format versi Hermes yang digunakan. |
| `DISCORD_BOT_TOKEN` | Token bot aplikasi Discord resmi, bukan token akun pribadi. |
| `DISCORD_ALLOWED_USERS` | ID pengguna Discord yang diizinkan. |
| `DISCORD_ALLOWED_CHANNELS` | ID channel Discord yang diizinkan. |
| `DISCORD_FREE_RESPONSE_CHANNELS` | Channel yang boleh dibalas tanpa mention. |
| `DISCORD_AUTO_THREAD` | Setel `false` untuk menonaktifkan thread otomatis. |

Aktifkan **Message Content Intent** di Discord Developer Portal bila diperlukan. Batasi user/channel dan gunakan izin bot seminimal mungkin. Jangan gunakan self-bot.

### 3. Ubuntu Terminal

Mode ini menyediakan Ubuntu 26.04 dengan terminal browser `ttyd`, banner sistem, Git/Python, Hermes CLI, dan Gateway opsional. Mode ini **bukan** Dashboard web Hermes dan tidak menggunakan wrapper Variables untuk membuat ulang `config.yaml`.

Untuk setup mode Ubuntu Terminal di Railway dari login terminal sampai bot membalas, ikuti [panduan satu jalur di bawah ini](#tutorial-lengkap-ubuntu-railway-sampai-bot-telegram-membalas).

Variabel di **Railway → service Ubuntu → Variables**:

Salin blok ini ke **Railway → Hermes-Ubuntu → Variables**. Ganti nilai contoh dengan kredensial baru:

```dotenv
RAILWAY_DOCKERFILE_PATH=/ubuntu/Dockerfile
TERMINAL_USER=ganti_username_terminal
TERMINAL_PASSWORD=GANTI_PASSWORD_ACAK_MINIMAL_16_KARAKTER
HERMES_HOME=/opt/data
HERMES_RUNTIME_DIR=/usr/local/share/hermes-tools
UV_CACHE_DIR=/tmp/uv-cache
HERMES_AUTOSTART=true
TZ=Asia/Jakarta
PORT=8080
```

- Pada service Ubuntu, set Dockerfile Path ke `ubuntu/Dockerfile` dan pastikan **Root Directory tetap kosong**, sehingga build context tetap root repository. `RAILWAY_DOCKERFILE_PATH` dicantumkan di template; pengaturan build Railway juga harus menunjuk ke path yang benar. Set restart policy `On Failure` dengan maksimal 10 retry.
- `TERMINAL_USER` tidak boleh mengandung titik dua (`:`) dan `TERMINAL_PASSWORD` wajib minimal 16 karakter. Gunakan nilai acak unik.
- Pasang Volume khusus service Ubuntu di `/opt/data` untuk konfigurasi, sesi/history, memori, dan log Hermes. `/data` adalah direktori file terminal; pasang Volume kedua yang berbeda di `/data` jika file buatan terminal harus bertahan sesudah redeploy. Jangan berbagi volume dengan service lain.
- Buka domain terminal setelah deployment terbaru selesai, login dengan kredensial tadi, lalu jalankan satu wizard:

~~~bash
hermes setup
~~~

Pilih **Full setup**, pilih provider/model, dan konfigurasi Telegram saat diminta. Wizard utama juga menyimpan pengaturan messaging; jalankan `hermes gateway setup` hanya jika ingin mengubah messaging secara terpisah. Pastikan konfigurasi dibuat:

~~~bash
test -f /opt/data/config.yaml && echo "Konfigurasi ditemukan" || echo "Setup belum selesai"
~~~

Pada image terbaru repo ini, entrypoint menunggu file `/opt/data/config.yaml` jika setup belum selesai. Dengan `HERMES_AUTOSTART=true`, supervisor akan mencoba menjalankan Gateway setelah file konfigurasi tersedia. Periksa Railway Deploy Logs; restart service dari Railway hanya jika Gateway tidak mulai setelah setup selesai. Jangan menjalankan Gateway manual bersamaan dengan auto-start. Tes pesan DM ke bot.
- Untuk menjalankan Gateway manual, set `HERMES_AUTOSTART=false`, restart service, lalu gunakan `start-hermes`. Jangan menjalankan Gateway kedua saat auto-start aktif; jangan menjalankan `hermes gateway run` langsung karena itu melewati lock wrapper.
- **Keamanan penting:** shell berjalan sebagai root di dalam container. Log Railway sebelumnya menampilkan kredensial ttyd dalam bentuk Base64 (Base64 bukan enkripsi); jika kredensial pernah tercetak pada log, segera rotasi `TERMINAL_PASSWORD`, simpan, lalu redeploy. Jangan menyimpan rahasia di GitHub.

> [!NOTE]
> Railway telah mendepresiasi Config-as-Code (`railway.json`/`railway.toml`) untuk service baru dan menyatakan file lama berhenti dibaca pada 1 Desember 2026. File root dipertahankan demi kompatibilitas service lama; untuk service baru, atur build dan restart policy dari Settings Railway. Lihat [dokumentasi Railway](https://docs.railway.com/config-as-code).


## Tutorial lengkap: Ubuntu Railway sampai bot Telegram membalas

Panduan ini khusus untuk **service Ubuntu Terminal** pada repository ini. Ikuti langkah **berurutan dari atas ke bawah**. Jangan mulai dari chat Telegram untuk menjawab pilihan wizard yang sedang tampil di terminal.

> [!IMPORTANT]
> **Angka pilihan 1 atau 2 dimasukkan di tempat prompt itu muncul.** Jika prompt muncul di halaman terminal browser Railway, klik area terminal lalu pilih opsi di sana—bukan mengirim angka ke chat bot Telegram. Pada menu pilihan, gunakan tombol panah ↑/↓ lalu tekan **Enter** jika wizard memakai menu navigasi. Jika prompt meminta Anda mengetik angka secara langsung, ketik angka di terminal lalu tekan **Enter**. Teks dan urutan opsi bisa berbeda antarversi Hermes; baca label yang tampil, jangan menebak berdasarkan angka saja.

### Langkah 1 — Pastikan service Railway benar

1. Buka Railway dan pilih project yang berisi service **Ubuntu Terminal**.
2. Klik service Ubuntu tersebut, lalu buka **Settings → Build**.
3. Pastikan **Dockerfile Path** adalah ubuntu/Dockerfile.
4. Pastikan **Root Directory kosong**. Jangan isi /ubuntu; build context harus tetap root repository.
5. Buka **Settings → Networking** dan pastikan domain terminal menargetkan port 8080.
6. Buka **Volumes** dan pastikan ada volume khusus service ini yang dipasang ke /opt/data. Jangan menghapus, detach, atau mengganti volume tersebut saat troubleshooting.

### Langkah 2 — Periksa Variables

Buka **service Ubuntu → Variables**. Pastikan variabel berikut ada. Ganti username/password contoh dengan nilai milikmu; jangan menyalin password contoh ke produksi.

~~~dotenv
RAILWAY_DOCKERFILE_PATH=/ubuntu/Dockerfile
TERMINAL_USER=ganti_username_terminal
TERMINAL_PASSWORD=GANTI_DENGAN_PASSWORD_ACAK_MINIMAL_16_KARAKTER
HERMES_HOME=/opt/data
HERMES_RUNTIME_DIR=/usr/local/share/hermes-tools
UV_CACHE_DIR=/tmp/uv-cache
HERMES_AUTOSTART=true
TZ=Asia/Jakarta
PORT=8080
~~~

- TERMINAL_USER wajib diisi dan tidak boleh mengandung titik dua (:).
- TERMINAL_PASSWORD wajib minimal 16 karakter, kuat, dan unik.
- HERMES_HOME=/opt/data menjaga konfigurasi dan data Hermes di volume persisten.
- HERMES_AUTOSTART=true membuat supervisor repo menjalankan Gateway setelah konfigurasi tersedia.
- Pengaturan **Dockerfile Path di Settings** tetap wajib benar; variabel RAILWAY_DOCKERFILE_PATH tidak menggantikan pengaturan build aktual.

Klik **Deploy/Redeploy** jika ada perubahan yang belum diterapkan. Tunggu deployment terbaru selesai, lalu periksa **Deploy Logs**. Jika domain belum bisa dibuka, selesaikan masalah domain/port sebelum lanjut.

### Langkah 3 — Buka terminal browser dan login

1. Buka domain publik yang dibuat di **Settings → Networking**.
2. Saat diminta login, masukkan TERMINAL_USER dan TERMINAL_PASSWORD dari Variables.
3. Setelah prompt shell muncul, kamu sudah berada di **terminal Ubuntu dalam browser**. Perintah Linux dan pilihan wizard berikutnya dijalankan di sini.

Jika halaman tidak terbuka, periksa target port 8080, status deployment, dan Deploy Logs. Jangan memasukkan token Telegram ke halaman login terminal.

### Langkah 4 — Mulai wizard Hermes

Di terminal browser, jalankan perintah ini lalu tekan Enter:

~~~bash
hermes setup
~~~

Saat muncul pertanyaan **How would you like to set up Hermes?**, pilih **Full setup — configure every provider, tool & option yourself** agar kamu bisa mengatur provider dan Telegram sendiri.

- Jika layar menampilkan menu yang dapat digerakkan, gunakan tombol panah ↑/↓ untuk menyorot **Full setup**, kemudian tekan **Enter**.
- Jika layar meminta nomor pilihan, masukkan nomor yang berada di samping label **Full setup** pada terminal itu, lalu tekan **Enter**.
- Jangan mengirim angka pilihan tersebut ke bot Telegram. Bot belum perlu membalas pada tahap setup ini.

### Langkah 5 — Konfigurasikan provider dan model

Ikuti prompt provider yang benar-benar muncul pada versi Hermes yang terpasang. Untuk jalur Gemini yang digunakan sebagai contoh di repo ini:

1. Pada **Select provider**, pilih **Google AI Studio (Native Gemini API)** jika pilihan itu tersedia.
2. Saat prompt meminta **Google AI Studio API key**, tempel API key milikmu di terminal dan tekan Enter. Jangan kirim key ke Telegram, issue GitHub, screenshot, atau commit.
3. Pada **Base URL**, tekan Enter untuk memakai nilai default jika tidak memiliki endpoint khusus.
4. Pada **Select default model**, pilih model Gemini yang tersedia untuk API key-mu. Jangan memaksakan ID model dari contoh jika tidak muncul atau tidak tersedia di akunmu.
5. Pada **Reasoning effort**, pilih low untuk mengutamakan respons ringan/cepat, jika opsi ini tersedia.
6. Pada **Terminal backend**, pilih **Keep current (local)** jika prompt tersebut muncul.

Nama, urutan, dan jumlah pilihan bisa berubah mengikuti versi Hermes dan provider. Gunakan label aktual pada layar; bila pilihan tidak sama dengan dokumentasi ini, jangan menebak nomor pilihan.

### Langkah 6 — Pilih platform Telegram

Saat wizard menampilkan daftar **Messaging Platforms** atau **Select platforms to configure**, pilih Telegram. Pastikan pilihan Telegram terpilih sebelum melanjutkan.

Saat prompt **How would you like to create your Telegram bot?** muncul:

1. Baca label di samping setiap opsi.
2. Pilih **Manual** jika kamu sudah membuat bot lewat BotFather. Pada layar yang menjadi contoh panduan ini, **Manual adalah opsi 2**. Jadi, jika prompt itu muncul di **terminal browser**, pilih opsi 2 di sana—bukan di chat Telegram.
3. Untuk menu navigasi, sorot **Manual** dengan tombol panah lalu tekan Enter. Jika diminta memasukkan angka, ketik angka yang sesuai dengan label **Manual** dan tekan Enter.
4. Buka Telegram di tab/aplikasi terpisah, cari @BotFather, lalu buat bot dengan /newbot jika belum punya.
5. Salin token yang diberikan BotFather dan tempel **ke prompt token di terminal browser**, lalu tekan Enter. Token adalah rahasia.
6. Saat prompt **Allowed user IDs** muncul, masukkan **numeric Telegram user ID milik akunmu**, bukan username dan bukan token bot. Masukkan hanya ID yang diizinkan.
7. Jika ditanya **Use your user ID as the home channel?**, pilih **Yes** jika bot ditujukan untuk percakapan pribadi dengan akun tersebut.

### Langkah 7 — Selesaikan prompt tools dan opsi tambahan

Wizard dapat menampilkan daftar tool beberapa kali—misalnya satu daftar untuk CLI dan daftar lain untuk Telegram. Itu bagian dari setup. Selesaikan setiap prompt hingga wizard menyatakan **Setup Complete** atau kembali ke prompt shell.

Untuk penggunaan chat pribadi yang sederhana:

- Nonaktifkan tool berisiko yang tidak dibutuhkan, terutama **Terminal & Processes**, **File Operations**, **Code Execution**, dan **Computer Use**. Terminal container berjalan sebagai root, sehingga tool tersebut dapat memiliki akses luas.
- **Browser Automation** dan **Image Generation** boleh di-skip untuk setup chat dasar.
- **Search Provider** boleh di-skip dahulu; bisa dikonfigurasi belakangan.
- Pada **Help improve Hermes?**, pilih **No thanks** jika tidak ingin ikut mengirim metrik penggunaan.

Baca label yang muncul. Jika versi Hermes menampilkan prompt berbeda, selesaikan sesuai keterangannya dan jangan mengasumsikan setiap nomor selalu sama.

### Langkah 8 — Pastikan konfigurasi tersimpan

Setelah wizard selesai dan prompt shell muncul kembali, jalankan:

~~~bash
test -f /opt/data/config.yaml && echo "Konfigurasi Hermes tersimpan" || echo "KONFIGURASI BELUM ADA"
~~~

Lanjutkan hanya jika hasilnya **Konfigurasi Hermes tersimpan**. Jika belum ada, jalankan kembali hermes setup dan tuntaskan wizard sampai selesai. Jangan menjalankan hermes uninstall --full; perintah itu dapat menghapus data persisten.

### Langkah 9 — Pastikan Gateway mulai

Dengan HERMES_AUTOSTART=true, entrypoint repo menunggu /opt/data/config.yaml jika file belum ada, kemudian mencoba menjalankan Gateway. Setelah wizard selesai:

1. Buka Railway → service Ubuntu → **Deploy Logs**.
2. Cari pesan tentang konfigurasi ditemukan dan Gateway dimulai.
3. Jika supervisor belum berjalan atau log menampilkan error, simpan pesan error pertama yang muncul. Jangan langsung mengulang instalasi.

Jika Gateway tidak mulai setelah konfigurasi selesai, lakukan **restart service satu kali dari Railway** agar proses membaca konfigurasi final, lalu cek Deploy Logs lagi. Jangan menjalankan Gateway manual bersamaan dengan auto-start.

### Langkah 10 — Tes bot di Telegram

Sekarang buka Telegram—baru pada tahap ini gunakan chat bot untuk pengujian.

1. Buka chat pribadi dengan bot yang tokennya kamu masukkan.
2. Kirim /start.
3. Kirim pesan biasa, misalnya: **Halo, balas hanya dengan OK.**
4. Tunggu balasan dan periksa Deploy Logs pada saat pesan dikirim.

Tes melalui DM terlebih dahulu, bukan grup. Jika bot membalas, instalasi dasar selesai.

### Langkah 11 — Jika bot masih diam

Jangan mengulang instalasi dan jangan menghapus volume. Periksa berdasarkan gejala:

| Gejala | Pemeriksaan berikutnya |
| --- | --- |
| Domain terminal tidak terbuka | Periksa deployment, domain, target port 8080, dan Deploy Logs. |
| Terminal terbuka tetapi hermes setup tidak ditemukan | Pastikan service memakai build dari repo ini dan lihat error startup/build. |
| /opt/data/config.yaml belum ada | Wizard belum selesai; jalankan hermes setup dan tuntaskan semua prompt. |
| Tidak ada log Gateway | Pastikan HERMES_AUTOSTART=true, konfigurasi tersedia, dan deployment memakai entrypoint terbaru. |
| HTTP 401 dari provider | API key salah, dicabut, atau tidak cocok dengan provider yang dipilih. Perbaiki konfigurasi provider. |
| HTTP 429 / quota | Periksa kuota atau rate limit akun provider. |
| Model not found / HTTP 404 | Pilih model yang benar-benar tersedia untuk API key tersebut. |
| Telegram Conflict / getUpdates | Token yang sama kemungkinan dipakai Gateway lain. Matikan Gateway lain dan sisakan satu pemakai token. |
| Bot mengabaikan akunmu | Pastikan numeric user ID yang diizinkan sama dengan akun yang mengirim DM. |
| Gateway mulai lalu berhenti | Baca error pertama pada Deploy Logs; status deploy SUCCESS saja tidak menjamin bot bekerja. |

**Jangan jalankan hermes gateway run atau start-hermes secara manual saat HERMES_AUTOSTART=true.** Jika ingin uji manual, ubah HERMES_AUTOSTART=false di Variables, restart service, lalu jalankan start-hermes dari terminal. Setelah pengujian, hentikan proses manual, kembalikan HERMES_AUTOSTART=true, lalu restart service.

> [!WARNING]
> Terminal berjalan sebagai root di dalam container. Jangan bagikan API key, token bot, atau password terminal. Jika password terminal terlihat di log, rotasi TERMINAL_PASSWORD pada Railway Variables dan redeploy. Base64 bukan enkripsi.

## Deploy ke Railway

Untuk menjalankan ketiga mode **bersamaan**, buat tiga Railway service yang masing-masing terhubung ke repo dan branch yang sama. Biarkan **Root Directory** kosong (root repository). Jangan mencoba menjalankan ketiga mode dalam satu service.

1. **Dashboard:** gunakan Dockerfile root dan atur builder/path di Railway Settings untuk service baru. Set restart policy `On Failure` dengan maksimal 10 retry. Set `DEPLOY_MODE=dashboard`, `USERNAME`, `PASSWORD`, dan `SECRET`.
2. **Variables:** gunakan Dockerfile root dan atur builder/path di Railway Settings untuk service baru. Set restart policy `On Failure` dengan maksimal 10 retry. Set `DEPLOY_MODE=variables` serta API key provider dan token Telegram/Discord yang memang ingin digunakan.
3. **Ubuntu:** pada Variables service itu, set `RAILWAY_DOCKERFILE_PATH=/ubuntu/Dockerfile`. Ini memilih image Ubuntu 26.04 tanpa mengubah build context. Biarkan Root Directory kosong karena Dockerfile menyalin `ubuntu/...` dari root repo.
4. **Pisahkan penyimpanan:** buat Volume berbeda untuk setiap service dan pasang masing-masing pada `/opt/data`. Jangan berbagi volume antarservice. Pada Ubuntu, pasang satu Volume tambahan yang berbeda di `/data` bila file terminal juga perlu bertahan setelah redeploy.
5. **Pisahkan secrets:** simpan variables pada tingkat service, bukan variables bersama tingkat environment. Gunakan set kredensial Dashboard hanya pada service Dashboard; provider/chat keys hanya pada service yang memerlukannya; `TERMINAL_USER` dan `TERMINAL_PASSWORD` hanya pada Ubuntu.
6. **Jaringan:** Variables mode umumnya tidak membutuhkan domain publik. Dashboard hanya dibuka setelah dilindungi OAuth/OIDC atau access gateway tepercaya. Ubuntu membutuhkan domain untuk browser terminal; terminal tetap berjalan sebagai root di dalam container, jadi gunakan password kuat dan unik.
7. Deploy setiap service secara manual saat siap, lalu periksa Deploy Logs dan uji mode tersebut. Perubahan repository ini sendiri tidak melakukan deploy ke Railway.


## Watch Paths agar deployment tidak saling memicu

Watch Paths perlu diatur **pada Settings masing-masing Railway service**; daftar ini tidak bisa berbeda per service hanya melalui satu `railway.json` bersama. Biarkan Root Directory kosong. Gunakan pola berikut pada bagian Watch Paths:

**Dashboard service**
```text
/Dockerfile
/railway-entrypoint.sh
/dashboard-entrypoint.sh
/railway.json
```

**Variables service**
```text
/Dockerfile
/railway-entrypoint.sh
/variables/**
/railway.json
```

**Ubuntu service**
```text
/ubuntu/**
/railway.json
```

Pola memakai sintaks gitignore-style Railway. `railway.json` sengaja dicantumkan di ketiga service karena konfigurasi root tersebut dapat memengaruhi semuanya. Perubahan dokumentasi saja tidak perlu membangun ulang container. Jika kelak menambahkan file root yang dipakai saat build, masukkan path itu ke Watch Paths service yang relevan. Lihat [dokumentasi Watch Paths Railway](https://docs.railway.com/builds/build-configuration#configure-watch-paths).

## Arsitektur dan struktur repo

![Arsitektur Hermes Agent Railway](docs/architecture.svg)

| Path | Fungsi |
| --- | --- |
| `Dockerfile`, `railway.json` | Build image dan konfigurasi Railway. |
| `railway-entrypoint.sh` | Memilih mode startup. |
| `dashboard-entrypoint.sh` | Memvalidasi kredensial dan menyiapkan Dashboard. |
| `variables/railway-entrypoint.sh` | Membuat konfigurasi provider/fallback. |
| `ubuntu/Dockerfile`, `ubuntu/entrypoint.sh` | Image dan startup Ubuntu Terminal, termasuk `ttyd` dan Gateway opsional. |
| `RAILWAY_DOCKERFILE_PATH` | Memilih `ubuntu/Dockerfile` khusus untuk service Ubuntu. |
| `ubuntu/README.md` | Petunjuk khusus service Ubuntu dan persistent volumes. |
| `env-examples/` | Contoh variabel tanpa kredensial aktif. |
| `docs/SOURCES.md` | Referensi upstream, atribusi artwork, dan batas lisensi. |
| `CONTRIBUTING.md`, `SECURITY.md` | Panduan kontribusi dan keamanan. |
| `scripts/` | Pemeriksaan statis konfigurasi, dokumentasi, dan shell syntax. |

## Keamanan Dashboard

- **Jangan publikasikan Dashboard langsung ke internet hanya dengan password bersama.** Upstream menyarankan basic auth hanya untuk jaringan tepercaya/VPN. Untuk domain publik, gunakan OAuth/OIDC atau access gateway yang dikonfigurasi dengan benar.
- Dashboard adalah antarmuka administratif untuk konfigurasi sensitif dan tindakan agent.
- Simpan password, API key, token bot, dan `SECRET` di Railway Variables, bukan di kode, README, screenshot, atau log publik.
- `SECRET` menandatangani sesi. Gunakan nilai acak yang kuat dan stabil antar-redeploy; rotasi jika bocor.
- Pastikan Volume `/opt/data` terpasang, batasi siapa yang dapat membaca/mengubah Variables, dan backup data penting.
- Dockerfile memakai upstream tag `latest`. Build ulang bisa mengambil versi Hermes berbeda; untuk deployment produksi yang reproducible, pin versi atau digest yang sudah diuji.
- Pantau biaya API model dan izin bot.

## Troubleshooting

| Masalah | Pemeriksaan |
| --- | --- |
| Container berhenti saat startup | Periksa Deploy Logs dan nilai `DEPLOY_MODE`. |
| Dashboard tak terbuka | Periksa `USERNAME`, `PASSWORD`, `SECRET` minimal 32 karakter, dan target port. |
| Login gagal | Periksa kredensial dan pastikan `SECRET` tidak berubah saat redeploy. |
| Variables mode gagal startup | Isi minimal satu API key Groq, Mistral, NVIDIA, atau Gemini/Google. |
| Model tak tersedia | Periksa model ID, kuota/saldo, status provider, dan izin akun. |
| Telegram tak merespons | Periksa token BotFather, allowlist ID, dan log gateway. |
| Discord tak merespons | Periksa token, izin, Message Content Intent bila perlu, dan allowlist. |
| Data hilang setelah redeploy | Pastikan Volume terpasang di `/opt/data` pada service/environment yang benar. |

## Pengembangan dan validasi

    python scripts/validate_repo.py
    python scripts/check_docs.py
    python -m json.tool railway.json
    sh -n railway-entrypoint.sh
    sh -n dashboard-entrypoint.sh
    sh -n variables/railway-entrypoint.sh
    bash -n ubuntu/entrypoint.sh
    bash -n ubuntu/start-hermes
    bash -n ubuntu/system-banner.sh

CI memeriksa konfigurasi statis, tautan lokal, SVG, JSON, dan sintaks shell. Ini bukan tes live terhadap Docker image, Railway, provider model, atau pengiriman pesan.

## Sumber, atribusi, dan lisensi

Lihat [`docs/SOURCES.md`](docs/SOURCES.md) untuk sumber resmi, atribusi artwork, dan batas lisensi.

- **Lisensi repository:** [MIT](LICENSE) berlaku untuk materi milik proyek yang tercakup, termasuk wrapper dan dokumentasi buatan repo ini.
- **Hermes Agent upstream:** source dan image upstream memiliki lisensi sendiri; repository upstream saat ini menyertakan MIT License. Ini tidak otomatis melisensikan ulang semua dependency, layanan API, atau merek dagang.
- **Pihak ketiga:** Railway, Docker, Telegram, Discord, dan penyedia model mengikuti ketentuan masing-masing.

Proyek ini independen dan tidak berafiliasi dengan atau didukung secara resmi oleh Nous Research, Railway, Telegram, Discord, Groq, Mistral, NVIDIA, atau Google.

## Kontribusi

Bug report dan pull request dipersilakan. Baca [`CONTRIBUTING.md`](CONTRIBUTING.md). Jangan sertakan token aktif, file environment, API key, atau data pribadi di issue/commit.
