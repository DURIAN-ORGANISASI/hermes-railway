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


## Tutorial Ubuntu Railway: dari awal sampai bot membalas

Ikuti langkah ini **berurutan**. Semua pilihan setup dijawab di terminal browser Railway, bukan di chat Telegram.

**Arti tanda:** 🔴 wajib/jangan dilewati · 🟡 perhatian/error umum · 📋 blok siap salin · ✅ tanda berhasil · 🧰 perbaikan jika gagal.

### 1. ⚙️ Siapkan service

Railway → project → service Ubuntu → **Settings → Build**:

- Dockerfile Path: `ubuntu/Dockerfile`
- Root Directory: kosong
- Restart policy: `On Failure`
- Networking domain: target port `8080`

### 2. 📋 Isi Variables

Railway → service Ubuntu → **Variables**. Ganti username dan password contoh.

~~~dotenv
RAILWAY_DOCKERFILE_PATH=/ubuntu/Dockerfile
TERMINAL_USER=ganti_username
TERMINAL_PASSWORD=GANTI_PASSWORD_ACAK_MINIMAL_16_KARAKTER
HERMES_HOME=/opt/data
HERMES_RUNTIME_DIR=/usr/local/share/hermes-tools
UV_CACHE_DIR=/tmp/uv-cache
HERMES_AUTOSTART=true
TZ=Asia/Jakarta
PORT=8080
~~~

### 3. 💾 Pasang volume

Railway → service Ubuntu → **Volumes** → buat volume dan mount ke:

~~~text
/opt/data
~~~

Jangan hapus volume ini. Data konfigurasi dan sesi Hermes disimpan di sini.

### 4. 🌐 Deploy dan buka terminal

1. Deploy service dan tunggu sampai selesai.
2. Buka domain dari **Settings → Networking**.
3. Login memakai `TERMINAL_USER` dan `TERMINAL_PASSWORD`.
4. Perintah selanjutnya diketik di terminal browser.

Jika domain tidak terbuka, cek target port `8080` dan **Deploy Logs**.

### 5. 🔴 Jalankan setup Hermes

Ketik di terminal browser:

~~~bash
hermes setup
~~~

Saat ditanya **How would you like to set up Hermes?**, pilih **Full setup**.

- Jika menu bergerak: gunakan tombol panah, lalu Enter.
- Jika diminta nomor: ketik nomor di samping pilihan yang benar, lalu Enter.
- **Jangan kirim nomor pilihan ke bot Telegram.**

### 6. 🔑 Atur provider/model

Ikuti prompt yang tampil. Untuk contoh Gemini:

1. Provider: **Google AI Studio (Native Gemini API)**.
2. Masukkan API key Google AI Studio di terminal.
3. Base URL: tekan Enter untuk default.
4. Pilih model yang tersedia untuk API key-mu.
5. Reasoning effort: pilih `low` jika tersedia.
6. Terminal backend: **Keep current (local)** jika ditampilkan.

Jangan gunakan model ID contoh jika tidak tersedia di daftar.

### 7. 🤖 Hubungkan Telegram

1. Pada daftar platform, pilih **Telegram**.
2. Saat ditanya cara membuat/menghubungkan bot, pilih **Manual** jika bot sudah dibuat melalui BotFather.
3. **Jika layar yang tampil menunjukkan Manual sebagai opsi 2, masukkan/pilih 2 di terminal browser.** Jika nomor berbeda, ikuti nomor di samping label Manual.
4. Buka Telegram → `@BotFather` → kirim `/newbot` jika belum punya bot.
5. Salin token BotFather, lalu tempel ke prompt token di terminal browser.
6. Saat diminta **Allowed user IDs**, masukkan ID Telegram numerik milikmu—bukan username atau token.
7. Jika ditanya **Use your user ID as the home channel?**, pilih Yes untuk penggunaan pribadi.
8. Selesaikan semua prompt sampai **Setup Complete** atau kembali ke prompt shell.

### 8. ✅ Selesaikan setup dan cek konfigurasi

Untuk chat pribadi, lewati tools yang tidak dibutuhkan. Hindari mengaktifkan Terminal & Processes, File Operations, Code Execution, atau Computer Use jika tidak diperlukan.

Lalu jalankan:

~~~bash
test -f /opt/data/config.yaml && echo "OK: konfigurasi ditemukan" || echo "Setup belum selesai"
~~~

Jika hasilnya `Setup belum selesai`, ulangi `hermes setup` dan tuntaskan semua pertanyaan. **Jangan jalankan `hermes uninstall --full`** karena bisa menghapus data.

### 9. 🔴 Pastikan Gateway aktif

1. Railway → service Ubuntu → **Deploy Logs**.
2. Pastikan Gateway mulai tanpa error.
3. Karena `HERMES_AUTOSTART=true`, jangan jalankan Gateway manual.
4. Jika Gateway tidak mulai setelah setup selesai, restart service satu kali lalu periksa Deploy Logs.

Pastikan token bot yang sama tidak digunakan service Dashboard/Variables lain secara bersamaan.

### 10. ✅ Tes bot

Baru sekarang buka chat Telegram dengan bot:

1. Kirim `/start`.
2. Kirim `Halo, balas OK.`
3. Jika tidak membalas, lihat **Deploy Logs** saat pesan dikirim.

### 11. 🧰 Jika gagal, periksa ini

| Masalah | Tindakan |
|---|---|
| Domain tidak terbuka | Periksa domain, port 8080, dan status service. |
| `config.yaml` tidak ditemukan | Selesaikan `hermes setup`; pastikan `HERMES_HOME=/opt/data). |
| API error 401 | Periksa API key dan provider. |
| Error 429 / quota | Periksa kuota provider. |
| Model tidak ditemukan | Pilih model yang tersedia di akun provider. |
| Telegram conflict / getUpdates | Matikan Gateway lain yang memakai token sama. |
| Bot diam | Periksa token, Allowed user ID, Gateway, dan Deploy Logs. |

**Keamanan:** jangan membagikan API key, token bot, atau password terminal. Terminal berjalan sebagai root di container. Jika `HERMES_AUTOSTART=true`, jangan menjalankan `start-hermes` atau `hermes gateway run` manual.

---

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
