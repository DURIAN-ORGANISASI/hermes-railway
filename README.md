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

**Instalasi Ubuntu langsung di VPS/server:** jika tujuan Anda memasang Hermes pada Ubuntu biasa melalui SSH (bukan container Railway), ikuti [Jalur A dalam panduan instalasi Ubuntu](ubuntu/README.md#jalur-a-instalasi-langsung-di-ubuntu-server-atau-vps). Panduan yang sama juga menjelaskan Jalur B khusus Ubuntu Terminal Railway, beserta provider, Telegram/Discord, penyimpanan, auto-start, dan troubleshooting.

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
- Buka domain terminal setelah deploy, login dengan kredensial tadi, lalu jalankan perintah setup berikut satu per satu:

```bash
hermes setup
hermes gateway setup
```

Ikuti wizard untuk provider/model dan kanal chat. Pastikan konfigurasi dibuat:

```bash
test -f /opt/data/config.yaml && echo "Konfigurasi ditemukan" || echo "Setup belum selesai"
```

Setelah konfigurasi tersedia, restart service dari Railway. Dengan `HERMES_AUTOSTART=true`, entrypoint mencoba menghidupkan Gateway secara otomatis. Periksa Deploy Logs lalu uji dengan mengirim pesan pada bot Telegram/Discord yang dikonfigurasi.
- Untuk menjalankan Gateway manual, set `HERMES_AUTOSTART=false`, restart service, lalu gunakan `start-hermes`. Jangan menjalankan Gateway kedua saat auto-start aktif; jangan menjalankan `hermes gateway run` langsung karena itu melewati lock wrapper.
- **Keamanan penting:** shell berjalan sebagai root di dalam container. Log Railway sebelumnya menampilkan kredensial ttyd dalam bentuk Base64 (Base64 bukan enkripsi); jika kredensial pernah tercetak pada log, segera rotasi `TERMINAL_PASSWORD`, simpan, lalu redeploy. Jangan menyimpan rahasia di GitHub.

> [!NOTE]
> Railway telah mendepresiasi Config-as-Code (`railway.json`/`railway.toml`) untuk service baru dan menyatakan file lama berhenti dibaca pada 1 Desember 2026. File root dipertahankan demi kompatibilitas service lama; untuk service baru, atur build dan restart policy dari Settings Railway. Lihat [dokumentasi Railway](https://docs.railway.com/config-as-code).


## Panduan lengkap setup Hermes di Ubuntu dan memperbaiki bot tidak merespons

Bagian ini berada di README utama agar langkah setup dapat diikuti dari awal sampai bot berhasil membalas. Pilih lingkungan yang benar:

- **Ubuntu Server/VPS biasa:** masuk melalui SSH dan instal Hermes langsung pada Ubuntu.
- **Ubuntu Terminal Railway:** buka terminal melalui domain service Railway yang dibangun dari repo ini.

Jangan mencampur perintah service kedua lingkungan. VPS biasa menggunakan systemd; container Ubuntu Railway pada repo ini menggunakan entrypoint dan variabel HERMES_AUTOSTART.

Dokumentasi upstream: [Instalasi Hermes](https://hermes-agent.nousresearch.com/docs/getting-started/installation), [Referensi CLI](https://hermes-agent.nousresearch.com/docs/reference/cli-commands), [Messaging Gateway](https://hermes-agent.nousresearch.com/docs/user-guide/messaging), [Telegram](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram/), dan [Discord](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/discord/).

### 1. Aturan sebelum mulai

1. **Pastikan model AI bisa menjawab sebelum menguji bot.** Jika provider/model gagal, Telegram atau Discord juga tidak akan bisa menghasilkan jawaban.
2. **Satu token bot hanya boleh dipakai satu Gateway aktif.** Jangan jalankan token Telegram/Discord yang sama di Dashboard, Variables, dan Ubuntu bersamaan. Telegram bisa menampilkan error Conflict ketika beberapa proses melakukan polling dengan token yang sama.
3. **Jangan menaruh token/API key di README, commit Git, screenshot, atau chat publik.** Gunakan wizard, Railway Variables privat, atau file .env yang permission-nya dibatasi.
4. Setelah mengubah token, allowlist, intent, atau izin, restart Gateway yang benar-benar digunakan.

### 2. Ubuntu Server/VPS biasa — instalasi dari awal

Jalankan dari SSH sebagai pengguna Linux biasa yang memiliki sudo; jangan gunakan root untuk percakapan harian.

Perbarui Ubuntu dan pasang prasyarat:

~~~bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y curl ca-certificates git xz-utils tar coreutils
~~~

Pasang Hermes melalui installer resmi:

~~~bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
~~~

Setelah proses instalasi selesai, muat ulang PATH dan verifikasi:

~~~bash
source ~/.bashrc
export PATH="$HOME/.local/bin:$PATH"
command -v hermes
hermes --help
hermes doctor
~~~

Jika command -v hermes tidak menghasilkan path, pastikan installer selesai tanpa error, jalankan source ~/.bashrc lagi, lalu sambungkan ulang melalui SSH sebagai pengguna yang sama.

Konfigurasikan provider/model AI:

~~~bash
hermes setup
~~~

Ikuti wizard dan pastikan API key valid, ID model tersedia untuk akun dan endpoint yang dipakai, serta kuota provider masih ada. Jika hanya ingin mengubah model, jalankan:

~~~bash
hermes model
~~~

**Tes model secara langsung sebelum setup bot:**

~~~bash
hermes -z "Balas hanya dengan kata OK."
~~~

Jika tes gagal, jalankan hermes doctor dan periksa provider, model, API key, kuota, endpoint, serta koneksi internet. Jangan melanjutkan debugging Telegram/Discord sampai tes model berhasil.

### 3. Setup Telegram/Discord di Ubuntu

Cara paling mudah adalah menjalankan wizard:

~~~bash
hermes gateway setup
~~~

Pilih platform yang ingin digunakan dan ikuti prompt.

#### Telegram

1. Buat bot lewat akun resmi @BotFather dan simpan tokennya.
2. Dapatkan **numeric Telegram user ID** akun yang diizinkan. Username seperti @nama bukan pengganti ID numerik.
3. Pastikan TELEGRAM_BOT_TOKEN valid dan TELEGRAM_ALLOWED_USERS memuat ID yang benar. Untuk beberapa pengguna, gunakan ID numerik yang dipisahkan koma.
4. Tes lewat **DM langsung** dengan /start, lalu kirim “Halo, balas OK”.
5. Jika DM berhasil tetapi grup tidak, coba mention bot. Periksa BotFather → /mybots → bot kamu → Bot Settings → Group Privacy. Sesuaikan privacy mode bila memang ingin bot membaca pesan biasa dalam grup, kemudian tambahkan kembali bot ke grup jika diperlukan.
6. Jika log berisi Conflict atau getUpdates, hentikan Gateway lain yang menggunakan token Telegram sama dan sisakan satu proses.

Alternatif manual untuk instalasi Ubuntu dengan HOME default: buka file environment berikut, lalu tambahkan atau perbarui variabel yang dibutuhkan tanpa menghapus setting lain:

~~~bash
mkdir -p ~/.hermes
chmod 700 ~/.hermes
nano ~/.hermes/.env
~~~

Contoh nilai — ganti dengan kredensial milikmu:

~~~dotenv
TELEGRAM_BOT_TOKEN=ISI_TOKEN_DARI_BOTFATHER
TELEGRAM_ALLOWED_USERS=123456789
~~~

Ganti contoh ID dengan numeric user ID sebenarnya. Simpan file di nano dengan Ctrl+O, tekan Enter, lalu keluar dengan Ctrl+X. Lindungi file:

~~~bash
chmod 600 ~/.hermes/.env
~~~

Jika HERMES_HOME disetel ke direktori khusus, file .env harus berada di direktori home Hermes tersebut, bukan otomatis di ~/.hermes.

#### Discord

1. Buat application dan bot di [Discord Developer Portal](https://discord.com/developers/applications), salin token bot, lalu undang bot ke server.
2. Pada aplikasi → **Bot → Privileged Gateway Intents**, aktifkan **Message Content Intent** dan simpan. Hermes memerlukannya untuk membaca isi pesan. Jika menggunakan username atau role pada allowlist, aktifkan juga **Server Members Intent**.
3. Pastikan bot memiliki izin View Channels, Send Messages, dan Read Message History pada channel uji.
4. Konfigurasikan DISCORD_BOT_TOKEN dan setidaknya satu kebijakan akses, misalnya DISCORD_ALLOWED_USERS berisi numeric Discord user ID kamu. Tanpa allowlist/policy yang valid, Gateway bisa tersambung tetapi menolak pesan masuk secara default.
5. Tes melalui DM. Di server, bot secara default perlu disebut/di-mention, misalnya “@Hermes Halo, balas OK”. Jika hanya satu channel gagal, periksa DISCORD_ALLOWED_CHANNELS dan DISCORD_IGNORED_CHANNELS jika variabel itu digunakan.

Alternatif manual untuk instalasi Ubuntu dengan HOME default:

~~~bash
mkdir -p ~/.hermes
chmod 700 ~/.hermes
nano ~/.hermes/.env
~~~

Tambahkan atau perbarui hanya variabel yang diperlukan:

~~~dotenv
DISCORD_BOT_TOKEN=ISI_TOKEN_DISCORD_BOT
DISCORD_ALLOWED_USERS=123456789012345678
~~~

Gunakan numeric user ID yang sebenarnya. Simpan lalu lindungi file:

~~~bash
chmod 600 ~/.hermes/.env
~~~

Wizard direkomendasikan karena dapat memvalidasi token dan menampilkan instruksi lanjutan. Setelah mengubah .env, restart Gateway.

### 4. Uji Gateway di foreground sebelum dipasang sebagai service

Pada Ubuntu VPS, pastikan tidak ada Gateway lain yang aktif memakai token yang sama. Jalankan:

~~~bash
hermes gateway
~~~

Biarkan terminal terbuka dan kirim pesan tes lewat Telegram/Discord. Perhatikan error yang tercetak. Jika bot membalas, integrasi dasar berhasil. Tekan Ctrl+C untuk menghentikan tes sebelum memasang service permanen.

Jika Gateway gagal, simpan teks error tanpa token/API key. Jangan memasang service permanen sebelum penyebab error diperbaiki.

### 5. Jalankan Gateway otomatis pada Ubuntu VPS

Untuk VPS/headless yang perlu berjalan saat boot, gunakan system service:

~~~bash
sudo hermes gateway install --system
sudo hermes gateway start --system
sudo hermes gateway status --system
~~~

Lihat log secara langsung:

~~~bash
sudo journalctl -u hermes-gateway -f
~~~

Keluar dari log dengan Ctrl+C. User service adalah alternatif lain: gunakan hermes gateway install, hermes gateway start, dan hermes gateway status; log dapat dilihat dengan journalctl --user -u hermes-gateway -f. Jangan menjalankan user service dan system service untuk bot/token yang sama secara bersamaan. Setelah mengubah konfigurasi, restart service yang dipilih.

### 6. Setup Gateway pada Ubuntu Terminal Railway dari repo ini

Mode ini sudah memasang Hermes saat image dibuat. Jangan menjalankan installer Hermes lagi di dalam terminal, kecuali memang sedang memelihara image.

Pastikan service Railway dikonfigurasi seperti ini:

- Dockerfile Path: ubuntu/Dockerfile.
- Root Directory: kosong (root repository).
- Domain terminal menargetkan port 8080.
- Volume persisten dipasang ke /opt/data.
- Variables berisi HERMES_HOME=/opt/data, HERMES_AUTOSTART=true, PORT=8080, TERMINAL_USER, dan TERMINAL_PASSWORD.
- TERMINAL_PASSWORD kuat, unik, dan minimal 16 karakter.

Buka domain terminal dan jalankan:

~~~bash
hermes doctor
hermes setup
hermes gateway setup
~~~

Ikuti wizard provider/model dan messaging, lalu verifikasi konfigurasi:

~~~bash
test -f /opt/data/config.yaml && echo "Config ditemukan" || echo "Config belum ada"
~~~

Jika file belum ada, selesaikan wizard dan periksa error yang ditampilkan. Pastikan volume /opt/data terpasang pada service Ubuntu yang benar.

Setelah konfigurasi tersedia, restart service melalui Railway. Dengan HERMES_AUTOSTART=true, entrypoint repo akan mencoba memulai Gateway. Periksa **Railway → Deploy Logs** dan kirim pesan tes ke bot.

Untuk pengujian manual tanpa proses ganda:

1. Ubah HERMES_AUTOSTART=false di Railway Variables.
2. Restart service.
3. Buka terminal browser dan jalankan:

~~~bash
start-hermes
~~~

Biarkan output terlihat sambil mengirim pesan tes. start-hermes memakai lock /opt/data/.gateway.lock. Jangan jalankan Gateway kedua secara bersamaan. Setelah pengujian, hentikan Gateway manual, kembalikan HERMES_AUTOSTART=true, lalu restart service.

**Penyimpanan:** /opt/data adalah lokasi konfigurasi dan state Hermes persisten dalam mode ini. /data adalah direktori kerja terminal; pasang volume kedua yang terpisah jika file di sana harus bertahan saat container diganti.

**Peringatan kredensial:** ttyd dapat menampilkan kredensial terminal yang dikodekan Base64 di log; Base64 bukan enkripsi. Jika password terminal terlihat di log, rotasi TERMINAL_PASSWORD dan redeploy.

### 7. Troubleshooting: bot tidak membalas

| Gejala/log | Penyebab yang mungkin | Tindakan |
| --- | --- | --- |
| hermes: command not found | PATH/instalasi belum benar | Jalankan source ~/.bashrc, cek command -v hermes dan log installer. Di Railway, periksa Deploy Logs. |
| hermes -z gagal | Provider/model/API key/kuota bermasalah | Jalankan hermes doctor dan hermes model; perbaiki provider sebelum memeriksa bot. |
| config.yaml tidak ditemukan | Wizard belum selesai atau direktori home salah | Jalankan hermes setup dan hermes gateway setup; periksa HERMES_HOME. |
| Telegram Conflict/getUpdates | Token dipakai beberapa Gateway | Hentikan Gateway lain yang memakai token itu; sisakan satu proses aktif. |
| Telegram tidak membalas lewat DM | Token salah, user tidak diizinkan, Gateway mati, atau model gagal | Periksa token, TELEGRAM_ALLOWED_USERS, status/log Gateway, dan tes model. |
| Telegram DM bekerja tetapi grup diam | Privacy Mode atau mention | Tes dengan mention; periksa Group Privacy di BotFather dan tambahkan ulang bot jika perlu. |
| Discord offline atau PrivilegedIntentsRequired | Intent belum diaktifkan | Aktifkan Message Content Intent; aktifkan Server Members Intent jika menggunakan username/role allowlist. Simpan lalu restart Gateway. |
| Discord online tetapi semua pesan diabaikan | Tidak ada access policy/allowlist valid | Set DISCORD_ALLOWED_USERS dengan numeric user ID atau policy akses yang sesuai; restart Gateway. |
| Discord DM bekerja tetapi channel server diam | Bot tak disebut atau izin channel kurang | Mention bot dan periksa View Channels, Send Messages, Read Message History, serta channel allowlist. |
| Provider memberi HTTP 401 | API key salah/dicabut atau endpoint salah | Perbarui kredensial pada konfigurasi provider. Jangan membagikan key. |
| Provider memberi HTTP 429 | Rate limit, kuota, atau saldo habis | Periksa limit akun/model dan gunakan provider/model yang tersedia. |
| Provider memberi HTTP 404/model not found | ID model atau endpoint tidak cocok | Pilih ID model valid untuk provider terkait. |
| Gateway mati setelah logout/reboot di VPS | Service belum dipasang atau diaktifkan | Periksa status service yang dipilih dan log journalctl. |
| Gateway mati setelah redeploy Railway | Config tidak ada, autostart mati, atau startup error | Pastikan config tersedia, HERMES_AUTOSTART=true, lalu periksa Deploy Logs. |

### 8. Urutan diagnosis — ikuti satu per satu

1. Tes model: hermes -z "Balas hanya dengan kata OK."
2. Periksa setup dengan hermes doctor dan pastikan konfigurasi tersedia.
3. Periksa service: hermes gateway status untuk user service atau hermes gateway status --system untuk system service.
4. Periksa log yang sesuai: journalctl --user -u hermes-gateway -f, sudo journalctl -u hermes-gateway -f, atau Railway Deploy Logs.
5. Jalankan Gateway foreground untuk satu kali tes dan kirim pesan.
6. Sesuaikan token, allowlist, Discord intents/permissions, serta pengaturan grup berdasarkan error yang muncul.
7. Setelah berhasil, pastikan hanya satu Gateway aktif untuk setiap token dan uji kembali pada mode service/auto-start.

Jika tetap gagal, kumpulkan 30–50 baris log saat mengirim pesan tes, versi Hermes, platform (Telegram/Discord), dan jenis instalasi (VPS/Railway). **Sensor semua token, API key, password, dan data pribadi sebelum membagikan log.**

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
