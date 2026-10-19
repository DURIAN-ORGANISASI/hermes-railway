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

    DEPLOY_MODE=dashboard
    USERNAME=admin
    PASSWORD=ganti-dengan-password-kuat-dan-unik
    SECRET=ganti-dengan-secret-acak-minimal-32-karakter

- Gunakan password unik dan `SECRET` acak minimal 32 karakter. Contoh: `openssl rand -base64 32`.
- Pasang Railway Volume pada `/opt/data`.
- Script memakai `PORT` jika tersedia; bila tidak, Dashboard memakai port `9119`. Target port Railway harus cocok.
- Setelah akses diamankan, atur provider/model dan integrasi chat mengikuti dokumentasi resmi Hermes.

> [!IMPORTANT]
> Basic username/password bukan pengganti OAuth/OIDC untuk Dashboard yang terbuka ke internet. Gunakan OAuth/OIDC atau access gateway yang benar-benar membatasi akses bila memakai domain publik.

### 2. Railway Variables

Mode ini tidak menyalakan Dashboard. Tambahkan variabel di **Railway → service Variables → Variables**. Minimal satu API key provider harus diisi; provider lain boleh kosong atau tidak dibuat.

    DEPLOY_MODE=variables
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

Variabel di **Railway → service Ubuntu → Variables**:

    TERMINAL_USER=durianadmin
    TERMINAL_PASSWORD=password-unik-minimal-16-karakter
    HERMES_AUTOSTART=true
    TZ=Asia/Jakarta

- Pada service Ubuntu, set variable service-scoped `RAILWAY_DOCKERFILE_PATH=/ubuntu/Dockerfile`. Biarkan Root Directory kosong agar build context tetap di root repo, lalu set restart policy `On Failure` dengan maksimal 10 retry.
- Pasang Volume tersendiri di `/opt/data` untuk konfigurasi, sesi, memori, dan log Hermes. Pasang Volume lain di `/data` jika ingin file yang dibuat lewat terminal tetap tersimpan.
- Setelah login ke terminal, jalankan `hermes setup` lalu `hermes gateway setup` sesuai provider dan kanal yang digunakan. Setelah `/opt/data/config.yaml` tersedia, `HERMES_AUTOSTART=true` (default) menghidupkan Gateway secara otomatis; set ke `false` untuk menonaktifkan auto-start.
- Untuk menjalankan Gateway secara manual, gunakan `start-hermes`. Terminal dan Gateway tetap mengikuti siklus hidup container Railway.
- Domain service ini membuka shell Ubuntu dengan hak root di dalam container. Pakai password kuat, batasi akses domain, dan jangan menyimpan rahasia di GitHub.

> [!NOTE]
> Railway telah mendepresiasi Config-as-Code (`railway.json`/`railway.toml`) untuk service baru dan menyatakan file lama berhenti dibaca pada 1 Desember 2026. File root dipertahankan demi kompatibilitas service lama; untuk service baru, atur build dan restart policy dari Settings Railway. Lihat [dokumentasi Railway](https://docs.railway.com/config-as-code).

## Deploy ke Railway

Untuk menjalankan ketiga mode **bersamaan**, buat tiga Railway service yang masing-masing terhubung ke repo dan branch yang sama. Biarkan **Root Directory** kosong (root repository). Jangan mencoba menjalankan ketiga mode dalam satu service.

1. **Dashboard:** gunakan Dockerfile root dan atur builder/path di Railway Settings untuk service baru. Set restart policy `On Failure` dengan maksimal 10 retry. Set `DEPLOY_MODE=dashboard`, `USERNAME`, `PASSWORD`, dan `SECRET`.
2. **Variables:** gunakan Dockerfile root dan atur builder/path di Railway Settings untuk service baru. Set restart policy `On Failure` dengan maksimal 10 retry. Set `DEPLOY_MODE=variables` serta API key provider dan token Telegram/Discord yang memang ingin digunakan.
3. **Ubuntu:** pada Variables service itu, set `RAILWAY_DOCKERFILE_PATH=/ubuntu/Dockerfile`. Ini memilih image Ubuntu 26.04 tanpa mengubah build context. Biarkan Root Directory kosong karena Dockerfile menyalin `ubuntu/...` dari root repo.
4. **Pisahkan penyimpanan:** buat Volume berbeda untuk setiap service dan pasang masing-masing pada `/opt/data`. Jangan berbagi volume antarservice. Pada Ubuntu, pasang satu Volume tambahan yang berbeda di `/data` bila file terminal juga perlu bertahan setelah redeploy.
5. **Pisahkan secrets:** simpan variables pada tingkat service, bukan variables bersama tingkat environment. Gunakan set kredensial Dashboard hanya pada service Dashboard; provider/chat keys hanya pada service yang memerlukannya; `TERMINAL_USER` dan `TERMINAL_PASSWORD` hanya pada Ubuntu.
6. **Jaringan:** Variables mode umumnya tidak membutuhkan domain publik. Dashboard hanya dibuka setelah dilindungi OAuth/OIDC atau access gateway tepercaya. Ubuntu membutuhkan domain untuk browser terminal; terminal tetap berjalan sebagai root di dalam container, jadi gunakan password kuat dan unik.
7. Deploy setiap service secara manual saat siap, lalu periksa Deploy Logs dan uji mode tersebut. Perubahan repository ini sendiri tidak melakukan deploy ke Railway.


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
