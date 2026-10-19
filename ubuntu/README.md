# Panduan Instalasi Hermes Agent di Ubuntu

Pilih salah satu jalur di bawah ini:

- **Jalur A — Ubuntu Server/VPS biasa:** Hermes dipasang langsung pada server Ubuntu melalui SSH. Cocok untuk Gateway yang harus hidup otomatis saat server reboot.
- **Jalur B — Ubuntu Terminal di Railway:** menjalankan container Ubuntu dan terminal browser melalui repo ini.

Keduanya berbeda. Jalur A menggunakan service systemd pada server; container Railway pada Jalur B menggunakan entrypoint dan mekanisme auto-start milik repo ini.

Dokumentasi resmi: [Installation](https://hermes-agent.nousresearch.com/docs/getting-started/installation), [Quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart), dan [Messaging Gateway](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/).

---

# Jalur A: Instalasi langsung di Ubuntu Server atau VPS

## A1. Persiapan

Siapkan Ubuntu Server 64-bit yang dapat diakses melalui SSH, koneksi internet keluar, akun Ubuntu biasa dengan akses sudo, dan API key dari salah satu penyedia model yang didukung Hermes. Panduan ini menggunakan perintah apt dan systemd, serta sesuai untuk Ubuntu Server 24.04 LTS atau 26.04 LTS.

Token Telegram atau Discord hanya diperlukan jika Anda ingin menghubungkan bot. Installer Hermes tidak otomatis menyediakan API key, saldo, atau kuota model. Jika model dipanggil melalui API, biasanya GPU tidak diperlukan. Browser automation dan tool tambahan dapat menambah kebutuhan sumber daya.

## A2. Masuk melalui SSH

Dari PowerShell Windows, sambungkan ke server dengan mengganti nama pengguna dan IP:

~~~bash
ssh NAMA_PENGGUNA@IP_SERVER
~~~

Jika SSH memakai port khusus, tambahkan opsi -p PORT_SSH. Setelah masuk, periksa sistem dan akun:

~~~bash
whoami
lsb_release -a
uname -m
~~~

**Jangan memasang Hermes sebagai root untuk pemakaian harian.** Jika saat ini Anda masuk sebagai root, buat akun biasa lalu sambungkan ulang:

~~~bash
adduser hermes
usermod -aG sudo hermes
exit
ssh hermes@IP_SERVER
~~~

Ganti nama hermes jika Anda memilih nama akun lain. Jika sudah memiliki akun biasa dengan akses sudo, gunakan akun tersebut dan lewati pembuatan akun baru.

## A3. Perbarui Ubuntu dan pasang prasyarat

Jalankan sebagai pengguna biasa dengan akses sudo:

~~~bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y git curl ca-certificates xz-utils tar coreutils
~~~

Tunggu sampai selesai. Jika pembaruan sistem meminta reboot, reboot kemudian masuk kembali melalui SSH. Verifikasi prasyarat:

~~~bash
git --version
curl --version
tar --version
sha256sum --version
~~~

Untuk instalasi standar, Anda **tidak perlu memasang Python, Node.js, npm, atau uv secara manual**. Installer Hermes mengelola runtime dan dependensi yang dibutuhkannya. Gunakan installer resmi; jangan memasang lewat pip atau uv tool.

### Opsional: firewall

Untuk bot Telegram/Discord dengan pola polling, biasanya tidak perlu membuka port web masuk karena koneksi dibuat keluar dari server. Sebelum mengaktifkan UFW, izinkan SSH agar Anda tidak mengunci diri dari server:

~~~bash
sudo ufw allow OpenSSH
sudo ufw status
~~~

Jika konfigurasi SSH sudah benar, aktifkan firewall dan periksa hasilnya:

~~~bash
sudo ufw enable
sudo ufw status verbose
~~~

Jangan membuka port secara acak. Port masuk hanya diperlukan untuk layanan yang memang ingin Anda publikasikan.

## A4. Instal Hermes dari sumber resmi

Jalankan sebagai **pengguna Ubuntu biasa**, tanpa sudo:

~~~bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
~~~

Tunggu sampai proses selesai dan jangan menutup sesi SSH saat installer masih berjalan.

Jika ingin memeriksa script terlebih dahulu, gunakan alternatif berikut. Keluar dari tampilan less dengan menekan tombol q:

~~~bash
curl -fsSLo /tmp/hermes-install.sh https://hermes-agent.nousresearch.com/install.sh
less /tmp/hermes-install.sh
bash /tmp/hermes-install.sh
rm -f /tmp/hermes-install.sh
~~~

Pilih salah satu metode di atas saja. Ikuti wizard interaktif jika muncul. Instalasi standar biasanya menempatkan launcher di ~/.local/bin/hermes dan data pengguna di ~/.hermes/. Lokasi dapat berbeda jika Anda mengubah opsi instalasi atau HERMES_HOME.

## A5. Verifikasi instalasi

Muat ulang environment shell dan pastikan perintah Hermes tersedia:

~~~bash
source ~/.bashrc
export PATH="$HOME/.local/bin:$PATH"
command -v hermes
hermes --help
~~~

Perintah command -v hermes seharusnya menampilkan lokasi launcher. Jika tidak ditemukan, pastikan installer selesai tanpa error, jalankan source ~/.bashrc lagi, atau keluar dan sambungkan kembali sebagai pengguna yang sama.

Jalankan pemeriksaan diagnostik:

~~~bash
hermes doctor
~~~

Baca hasilnya dan selesaikan error yang dilaporkan sebelum menambahkan integrasi chat. Jika installer menampilkan lokasi log, gunakan log tersebut untuk memeriksa langkah yang gagal.

## A6. Atur provider dan model AI

Jika wizard belum berjalan atau setup perlu diulang, jalankan:

~~~bash
hermes setup
~~~

Ikuti wizard untuk memilih provider, model, serta pengaturan lain yang ditampilkan. Masukkan API key melalui prompt konfigurasi lokal Hermes. Untuk mengubah provider atau model setelahnya:

~~~bash
hermes model
~~~

Catatan penting:

- API key harus berasal dari akun provider Anda; installer Hermes tidak memberikannya.
- Pastikan model tersedia untuk akun, endpoint, dan kuota Anda. Nama model dan kebijakan provider bisa berubah.
- Jangan menaruh API key di GitHub, tangkapan layar, pesan publik, atau argumen perintah yang bisa tersimpan dalam shell history.
- Jika muncul error autentikasi, kuota, atau model tidak ditemukan, periksa provider dan konfigurasi sebelum menyimpulkan instalasi rusak.

Setelah konfigurasi selesai, jalankan:

~~~bash
hermes doctor
hermes status
~~~

## A7. Tes chat lokal sebelum mengaktifkan bot

Mulai sesi percakapan:

~~~bash
hermes
~~~

Ketik pertanyaan sederhana dan pastikan model membalas. **Pastikan chat lokal bekerja sebelum menghubungkan Telegram atau Discord.** Integrasi Gateway tidak akan memperbaiki API key atau model yang gagal.

Jika chat gagal, periksa pengaturan dengan hermes model, API key, nama model, kuota/saldo, endpoint, dan koneksi internet. Jalankan hermes doctor untuk diagnosis.

## A8. Hubungkan Telegram atau Discord (opsional)

Jika Anda hanya ingin menggunakan Hermes dari terminal, bagian ini dapat dilewati. Untuk mengatur integrasi chat, jalankan:

~~~bash
hermes gateway setup
~~~

Pilih platform melalui wizard dan ikuti petunjuknya.

### Telegram

1. Hubungi akun resmi @BotFather di Telegram dan buat bot.
2. Salin token yang diberikan lalu masukkan melalui wizard.
3. Atur pembatasan pengguna atau allowlist sesuai kebutuhan serta dukungan versi Hermes yang dipasang.
4. Uji bot dari akun yang diizinkan.

Token Telegram adalah rahasia seperti kata sandi. Jangan membagikannya atau memasukkannya ke commit GitHub.

### Discord

1. Buat application dan bot di [Discord Developer Portal](https://discord.com/developers/applications).
2. Simpan token bot secara privat dan masukkan melalui wizard Hermes.
3. Aktifkan **Message Content Intent** bila konfigurasi dan pola penggunaan bot membutuhkannya.
4. Undang bot ke server dengan izin minimum yang dibutuhkan.
5. Atur user ID, channel ID, serta allowlist yang diminta Hermes, kemudian uji di channel yang diizinkan.

Bot yang tidak membalas bisa disebabkan token, izin server, intent, allowlist, kuota model, atau Gateway ganda; belum tentu instalasi gagal.

## A9. Jalankan Gateway otomatis setelah reboot

Pengaturan platform chat dan pemasangan service sistem adalah dua hal berbeda. Untuk VPS berbasis systemd, pasang Gateway sebagai **system service** agar hidup saat boot dan tidak bergantung pada sesi SSH:

~~~bash
sudo hermes gateway install --system
sudo hermes gateway start --system
sudo hermes gateway status --system
~~~

Jalankan perintah dari akun yang sama dengan akun yang memasang dan mengonfigurasi Hermes. Jangan berpindah ke root lalu membuat konfigurasi berbeda di home root.

Periksa log:

~~~bash
sudo journalctl -u hermes-gateway -f
~~~

Keluar dari tampilan log dengan Ctrl+C. Periksa service setelah reboot:

~~~bash
sudo hermes gateway status --system
sudo systemctl status hermes-gateway --no-pager
~~~

Jika nama unit tidak sama, misalnya karena HERMES_HOME khusus atau profil lain, cari nama service yang benar:

~~~bash
systemctl list-units --all | grep -i hermes
~~~

Jangan menjalankan lebih dari satu Gateway yang memakai token bot sama. Jika Anda sebelumnya memasang user service melalui hermes gateway install, pastikan user service dan system service tidak sama-sama menjalankan bot yang sama. Pilih satu cakupan service. Saat system service aktif, jangan menjalankan hermes gateway run secara bersamaan untuk token yang sama.

Setelah service aktif, kirim pesan uji ke bot. Status active hanya membuktikan service berjalan; pastikan balasan benar-benar diterima dan periksa log.

## A10. Update dan lindungi data

Untuk memperbarui instalasi standar, jalankan sebagai pengguna yang memasang Hermes:

~~~bash
hermes update
hermes doctor
hermes status
~~~

Sebelum perubahan besar, buat backup atas data Hermes yang diperlukan. Lokasi default biasanya ~/.hermes/, berisi konfigurasi, memori, sesi, dan log. Data ini bisa berisi token atau informasi sensitif; lindungi backup dan jangan mengunggahnya ke repo.

Praktik keamanan:

- Jangan memakai root untuk percakapan harian.
- Simpan API key dan token hanya dalam konfigurasi lokal yang terlindungi.
- Batasi akses SSH dan gunakan firewall sesuai kebutuhan.
- Batasi bot dengan allowlist; jangan memberi semua pengguna akses tanpa memahami risikonya.
- Jangan membagikan isi ~/.hermes/, konfigurasi, log, atau backup tanpa memeriksa rahasia di dalamnya.
- Jika token bocor, rotasi token di layanan terkait dan perbarui konfigurasi.

## A11. Troubleshooting Ubuntu

| Gejala | Pemeriksaan dan tindakan |
| --- | --- |
| hermes: command not found | Jalankan source ~/.bashrc, lalu export PATH="$HOME/.local/bin:$PATH". Periksa command -v hermes dan pastikan installer berhasil. |
| Installer gagal | Periksa koneksi, paket prasyarat A3, pesan error, dan log instalasi. Jalankan sebagai pengguna biasa. |
| hermes doctor melaporkan masalah | Ikuti diagnosis spesifik. Jangan langsung menghapus ~/.hermes/ karena menyimpan data pengguna. |
| Model tidak menjawab | Periksa hermes model, API key, nama model, kuota/saldo, izin akun, endpoint, dan koneksi jaringan. |
| Konfigurasi belum siap | Jalankan hermes setup sebagai pengguna yang sama dengan instalasi, lalu cek hermes status. |
| Telegram tidak membalas | Periksa token BotFather, allowlist/user ID, status Gateway, log, provider model, dan Gateway duplikat. |
| Discord tidak membalas | Periksa token, undangan bot, channel/user ID, permission, Message Content Intent bila diperlukan, log, dan Gateway duplikat. |
| Gateway mati setelah logout/reboot | Periksa pemasangan system service di A9, status Gateway, dan log journalctl. |
| Service terus restart | Baca log; periksa konfigurasi, autentikasi provider, permission, dan Gateway duplikat. |
| SSH terputus | Sambungkan kembali dan periksa service. Gunakan system service agar Gateway tidak bergantung pada terminal SSH terbuka. |

Urutan diagnosis yang disarankan: **(1) hermes doctor, (2) tes chat lokal, (3) hermes gateway status --system, (4) baca log Gateway, (5) tes bot dan periksa izin/allowlist.**

---

# Jalur B — Ubuntu Terminal di Railway

Bagian ini khusus untuk mode **Ubuntu Terminal** pada repo ini. Anda tidak perlu memasang Ubuntu atau Hermes dari awal di terminal browser: image ubuntu/Dockerfile sudah memasang Ubuntu dan Hermes saat build. Anda hanya perlu mengatur Railway, membuka terminal browser, lalu menyelesaikan wizard Hermes.

Mode ini **bukan** Dashboard web Hermes dan bukan VPS Ubuntu penuh dengan systemd. Container menggunakan ttyd serta entrypoint repo untuk terminal dan auto-start Gateway.

## B1. Buat service Railway

1. Hubungkan service baru ke DURIAN-ORGANISASI/hermes-railway, branch main.
2. Biarkan **Root Directory kosong** agar build context tetap root repo.
3. Pada Settings → Build, pilih Dockerfile dan set **Dockerfile Path** ke ubuntu/Dockerfile. Jangan hanya mengandalkan environment variable; pastikan pengaturan build aktual benar.
4. Atur restart policy menjadi **On Failure**, maksimal 10 retry.
5. Buat domain Railway. Terminal mendengarkan pada port 8080, sehingga target port domain harus sama.

## B2. Isi Railway Variables

Salin blok ini ke **Railway → service Ubuntu → Variables**. Ganti kredensial contoh sebelum deploy:

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

- TERMINAL_USER wajib diisi dan tidak boleh berisi titik dua (:).
- TERMINAL_PASSWORD wajib diisi, minimal 16 karakter, kuat, dan unik.
- RAILWAY_DOCKERFILE_PATH=/ubuntu/Dockerfile dicantumkan untuk dokumentasi, tetapi Dockerfile Path pada Railway Settings tetap harus menunjuk ke ubuntu/Dockerfile.
- HERMES_AUTOSTART=true membuat entrypoint menjalankan Gateway setelah konfigurasi tersedia.
- Jangan gunakan password yang sama dengan akun lain.

## B3. Pasang volume persisten

Buat Railway Volume khusus service Ubuntu dan mount ke:

~~~text
/opt/data
~~~

Lokasi ini menyimpan konfigurasi Hermes, sesi/history, memori, dan log. Jangan berbagi volume dengan service Dashboard atau Variables.

Direktori kerja terminal adalah /data. File di sana belum tentu bertahan setelah container diganti. Jika perlu persisten, pasang **volume kedua yang berbeda** ke /data; jangan berbagi satu volume yang sama antarlayanan atau antarmount point.

Runtime dan cache yang dapat dibuat ulang dipisahkan dari volume utama agar tidak cepat memenuhi penyimpanan.

## B4. Deploy dan buka terminal

Deploy service dan tunggu build/startup selesai. Buka domain Railway dan login menggunakan TERMINAL_USER serta TERMINAL_PASSWORD.

Jika terminal tidak dapat dibuka, pastikan domain menargetkan port 8080, service berjalan, lalu periksa Build Logs dan Deploy Logs.

Terminal dapat terbuka walaupun setup Hermes belum selesai. Pesan bahwa config.yaml belum ditemukan berarti Gateway belum siap, bukan berarti image harus dibangun ulang.

## B5. Konfigurasi Hermes di terminal browser

Jalankan:

~~~bash
hermes setup
~~~

Ikuti wizard provider/model. Untuk menghubungkan chat:

~~~bash
hermes gateway setup
~~~

Simpan API key dan token melalui wizard, bukan di GitHub atau log publik. Periksa konfigurasi persisten:

~~~bash
test -f /opt/data/config.yaml \
  && echo "Konfigurasi Hermes ditemukan" \
  || echo "Konfigurasi belum ada — selesaikan setup dahulu"
~~~

Jika belum ada, selesaikan wizard dan perbaiki error yang ditampilkan.

## B6. Jalankan dan uji Gateway

Setelah /opt/data/config.yaml tersedia, restart service dari Railway. Dengan HERMES_AUTOSTART=true, entrypoint seharusnya mendeteksi konfigurasi dan memulai supervisor Gateway.

Periksa Deploy Logs lalu kirim pesan uji ke Telegram/Discord. Status deploy SUCCESS tidak menjamin provider, token, izin bot, atau balasan pesan telah bekerja.

Untuk Gateway manual:

1. Set HERMES_AUTOSTART=false di Railway Variables.
2. Restart service.
3. Jalankan:

~~~bash
start-hermes
~~~

Wrapper start-hermes dan auto-start menggunakan lock /opt/data/.gateway.lock. Jangan memulai Gateway kedua pada service yang sama. Hindari menjalankan hermes gateway run langsung saat auto-start aktif karena melewati lock wrapper.

## B7. Penyimpanan dan keamanan Railway

- /opt/data: konfigurasi, sesi/history, memori, dan log Hermes.
- /data: file terminal; persisten hanya jika dipasang volume terpisah.
- /usr/local/share/hermes-agent dan /usr/local/share/hermes-tools: runtime yang dapat dibuat ulang saat image dibangun ulang.

Terminal berjalan sebagai root di container dan dapat diakses melalui domain service. Gunakan password kuat, batasi akses publik jika memungkinkan, dan jangan mempublikasikan kredensial terminal, API key, atau token bot.

**Peringatan log:** ttyd dapat mencetak kredensial HTTP Basic Auth dalam bentuk Base64. Base64 bukan enkripsi. Jika password terminal muncul di log, anggap kredensial terekspos: rotasi TERMINAL_PASSWORD, simpan perubahan, lalu redeploy.

## B8. Troubleshooting Railway

| Gejala | Pemeriksaan |
| --- | --- |
| Domain terminal 502 | Pastikan target port 8080, service berjalan, dan periksa Deploy Logs. |
| Login gagal | Periksa TERMINAL_USER dan TERMINAL_PASSWORD; password minimal 16 karakter dan username tidak boleh berisi titik dua. |
| Konfigurasi belum ada | Jalankan hermes setup dan hermes gateway setup, lalu periksa /opt/data/config.yaml. |
| Gateway tidak mulai | Pastikan HERMES_AUTOSTART=true, konfigurasi tersedia, dan periksa error provider/auth di log. |
| Telegram/Discord tidak membalas | Periksa token, API key, nama model, allowlist, permission/intent, dan Gateway duplikat. |
| File di /data hilang setelah redeploy | Pasang volume kedua yang berbeda di /data. |
| Volume /opt/data cepat penuh | Simpan state pengguna di volume persisten; cache/runtime yang dapat dibuat ulang tetap di luar volume. |

Lihat [README utama](../README.md) untuk mode Dashboard dan Railway Variables.


---

# Jika bot sudah dikonfigurasi tetapi tidak membalas

Ikuti urutan ini dari atas ke bawah. Jangan langsung menghapus konfigurasi atau membuat bot baru; log biasanya menunjukkan penyebabnya. Perintah di bagian ini berlaku untuk Hermes CLI upstream. Untuk terminal Railway, gunakan langkah Railway tersendiri di bawah.

## 1. Pastikan satu token hanya dipakai satu Gateway

**Penting untuk repo ini:** jangan menjalankan token Telegram atau Discord yang sama sekaligus di service Dashboard, Variables, dan Ubuntu. Pilih hanya satu service untuk setiap token bot. Untuk pengujian, hentikan Gateway di service lain yang memakai token tersebut, lalu mulai ulang service yang sedang diuji. Telegram polling khususnya dapat memutus salah satu proses jika token yang sama memiliki lebih dari satu poller.

## 2. Pastikan Hermes dan model memang bisa menjawab

Di Ubuntu VPS, login sebagai akun yang memasang Hermes, lalu jalankan:

~~~bash
command -v hermes
hermes --version
hermes doctor
hermes -z "Balas hanya dengan kata OK."
~~~

Perintah terakhir menguji pipeline model tanpa Telegram atau Discord. Jika gagal, perbaiki error provider/model terlebih dahulu melalui:

~~~bash
hermes model
hermes doctor
~~~

Pastikan API key benar, model ID tersedia bagi akun Anda, kuota tidak habis, serta endpoint/provider dapat dijangkau. Gateway tidak dapat memperbaiki kegagalan model.

## 3. Periksa konfigurasi dan log tanpa membocorkan token

Hermes standar biasanya menyimpan konfigurasi di ~/.hermes. Jika HERMES_HOME Anda diatur ke /opt/data, gunakan lokasi /opt/data. Jangan menempelkan token asli ke issue, chat publik, atau screenshot.

Ubuntu VPS, lokasi default:

~~~bash
ls -la ~/.hermes
tail -n 100 ~/.hermes/logs/gateway.log
~~~

Ubuntu Terminal Railway pada repo ini:

~~~bash
ls -la /opt/data
test -f /opt/data/config.yaml && echo "config.yaml tersedia" || echo "config.yaml belum ada"
test -f /opt/data/.env && echo ".env tersedia" || echo ".env belum ada"
test -f /opt/data/logs/gateway.log && tail -n 100 /opt/data/logs/gateway.log || echo "gateway.log belum ada; periksa Railway Deploy Logs"
~~~

File log dapat berisi data sensitif. Jika akan membagikan log untuk diagnosis, hapus token, API key, URL rahasia, ID pribadi, dan isi percakapan terlebih dahulu.

## 4. Jalankan Gateway di foreground untuk melihat error sebenarnya

Lakukan langkah ini hanya setelah menghentikan service Gateway lain yang memakai token yang sama.

### Ubuntu VPS biasa

Jika Anda memakai user service:

~~~bash
hermes gateway stop
hermes gateway run
~~~

Jika Anda memakai system service, hentikan system service dahulu:

~~~bash
sudo hermes gateway stop --system
hermes gateway run
~~~

Biarkan perintah foreground tetap terbuka, kirim pesan uji, dan perhatikan error yang muncul. Tekan Ctrl+C setelah pengujian. Jangan menyalakan foreground Gateway bersamaan dengan system service.

Setelah penyebabnya diperbaiki, nyalakan lagi hanya satu mode service yang dipilih. User service menggunakan hermes gateway start/status; system service menggunakan sudo hermes gateway start/status --system.

### Ubuntu Terminal Railway pada repo ini

Container Railway tidak mengandalkan systemd. Jika HERMES_AUTOSTART=true, entrypoint dapat menjalankan Gateway supervisor secara otomatis. Periksa Deploy Logs terlebih dahulu dan jangan menjalankan Gateway manual di atas proses auto-start.

Untuk menguji manual, ubah HERMES_AUTOSTART=false di Railway Variables, restart service, login kembali ke terminal browser, lalu jalankan:

~~~bash
start-hermes
~~~

Perhatikan output Gateway dan kirim pesan uji. Untuk mengembalikan auto-start, hentikan sesi manual, ubah HERMES_AUTOSTART=true, lalu restart service. Jangan biarkan dua Gateway aktif di container yang sama.

## 5. Jika menggunakan Telegram

1. Uji pesan langsung (DM) ke bot terlebih dahulu, mulai dengan /start. Jangan mulai dari grup.
2. Jalankan wizard untuk memeriksa token dan allowlist:

~~~bash
hermes gateway setup
~~~

Pilih Telegram, masukkan token bot yang benar, kemudian isi ID pengguna Telegram berupa angka, bukan @username. ID dapat diperiksa dengan mengirim pesan ke @userinfobot.
3. Pastikan TELEGRAM_ALLOWED_USERS memuat ID pengguna Anda. Jika lebih dari satu, gunakan ID angka yang dipisahkan koma sesuai format yang diterima versi Anda.
4. Pastikan token Telegram yang sama tidak dipakai service Gateway lain. Jika log menyebut conflict atau terminated by other getUpdates request, hentikan Gateway lain yang memakai token tersebut dan mulai ulang hanya satu.
5. Jika DM bekerja tetapi grup tidak, periksa Privacy Mode di BotFather. Matikan melalui /mybots → pilih bot → Bot Settings → Group Privacy. Setelah mengubah pengaturan, keluarkan bot dari grup lalu tambahkan kembali, atau jadikan bot admin. Di grup, coba juga mention @nama_bot.
6. Setelah perubahan token atau allowlist, mulai ulang Gateway dan uji lagi.

## 6. Jika menggunakan Discord

1. Mulai dengan DM ke bot. Di server, coba sebut bot menggunakan mention yang benar, misalnya @Hermes. Secara default, Hermes hanya membalas pesan channel yang menyebut bot.
2. Buka Discord Developer Portal → aplikasi bot → Bot → Privileged Gateway Intents. Aktifkan Message Content Intent, lalu simpan. Jika allowlist memakai username atau role, aktifkan Server Members Intent juga; penggunaan numeric user ID menghindari ketergantungan pada pencocokan nama.
3. Pastikan bot diundang ke server dan memiliki View Channels, Send Messages, serta Read Message History pada channel uji. Beri izin Embed Links dan Attach Files bila respons membutuhkannya.
4. Atur kebijakan akses. Untuk penggunaan pribadi, gunakan ID pengguna Discord numerik milik Anda di DISCORD_ALLOWED_USERS. Pada versi Hermes baru, Discord dapat berhasil connect tetapi menolak semua pesan jika tidak ada kebijakan akses. Jangan mengaktifkan allow-all pada server publik untuk mengatasi masalah ini.
5. Jika hanya satu channel tidak berfungsi, periksa DISCORD_ALLOWED_CHANNELS dan DISCORD_IGNORED_CHANNELS serta pastikan ID channel yang dimasukkan benar.
6. Restart Gateway dan uji ulang. Periksa log apabila bot online tetapi tetap diam.

## 7. Cara membaca error yang umum

| Pesan/gejala | Makna yang perlu diperiksa |
| --- | --- |
| config.yaml belum ada | Wizard setup belum selesai, atau HERMES_HOME berbeda dari lokasi konfigurasi yang diperiksa. |
| HTTP 401 / Unauthorized dari provider | API key provider salah, dicabut, atau tidak sesuai endpoint. |
| HTTP 429 / rate limit / quota | Kuota, limit permintaan, atau billing provider; bot mungkin menerima pesan tetapi tidak bisa menghasilkan jawaban. |
| model not found / HTTP 404 dari model API | Model ID atau endpoint tidak cocok dengan provider yang dipilih. |
| Telegram conflict / getUpdates | Ada proses lain yang memakai token bot yang sama atau update polling bersamaan. |
| Telegram unauthorized | ID pengguna tidak diizinkan oleh TELEGRAM_ALLOWED_USERS atau kebijakan akses. |
| Discord privileged Gateway Intents | Aktifkan intent yang diminta pada Developer Portal dan simpan perubahan. |
| Discord online tetapi diam di server | Uji DM, mention bot, allowlist pengguna/role, dan channel allowlist/denylist. |
| Gateway tidak aktif | Periksa perintah service yang sesuai, atau jalankan foreground untuk melihat error. |
| Model uji berhasil, tetapi bot tetap diam | Fokus pada Gateway, token platform, allowlist, intent, mention/privacy mode, izin channel, atau duplikasi Gateway. |

## 8. Setelah berhasil

Begitu pengujian foreground berhasil, hentikan foreground dengan Ctrl+C dan aktifkan hanya satu pengelola Gateway:

- Ubuntu VPS: pilih user service atau system service dan pastikan aktif setelah reboot.
- Railway Ubuntu Terminal: pilih auto-start entrypoint atau mode manual; jangan menjalankan keduanya bersamaan.
- Uji sekali lagi setelah service berjalan di latar belakang. Status service aktif saja belum membuktikan bot berhasil mengirim balasan.
