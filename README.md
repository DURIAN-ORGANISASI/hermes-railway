# Hermes Agent Railway — satu repo, dua mode

Repository ini menyediakan dua mode deployment melalui satu `Dockerfile`. Pilih satu mode per Railway service.

## Mode 1 — Dashboard

Ini mode default. Jangan set `DEPLOY_MODE=variables` jika ingin Dashboard. Isi variabel berikut untuk login dashboard:

```dotenv
USERNAME=
PASSWORD=
SECRET=
```

Tambahkan Railway Volume di `/opt/data`, buat domain publik untuk port yang digunakan Railway, lalu atur provider/model dan koneksi Telegram/Discord melalui dashboard. Gunakan password kuat dan `SECRET` acak panjang. Jangan publikasikan dashboard tanpa perlindungan yang memadai.

## Mode 2 — Railway Variables biasa

Set `DEPLOY_MODE=variables`. Mode ini tidak menjalankan dashboard; API key dan token diatur melalui Railway → service → Variables.

```dotenv
DEPLOY_MODE=variables
GROQ_API_KEY=
MISTRAL_API_KEY=
NVIDIA_API_KEY=
GEMINI_API_KEY=
TELEGRAM_BOT_TOKEN=
TELEGRAM_ALLOWED_USERS=
DISCORD_BOT_TOKEN=
DISCORD_ALLOWED_USERS=
DISCORD_ALLOWED_CHANNELS=
DISCORD_FREE_RESPONSE_CHANNELS=
DISCORD_AUTO_THREAD=false
```

**Cukup isi satu API key saja atau beberapa sekaligus.** Variabel provider lain boleh tidak ditambahkan atau dibiarkan kosong. Contoh jika hanya memakai NVIDIA:

```dotenv
DEPLOY_MODE=variables
NVIDIA_API_KEY=isi_api_key_nvidia
```

Untuk Gemini, `GOOGLE_API_KEY` juga diterima jika `GEMINI_API_KEY` tidak diisi. Tidak ada `PROVIDER_API`, `MODEL_PROVIDER`, `MODEL_ID`, atau `FALLBACK_MODELS` yang perlu diatur.

### Fallback otomatis

Skrip memeriksa key yang tidak kosong dengan urutan prioritas tetap: **Groq → Mistral → NVIDIA → Gemini**. Provider aktif pertama menjadi model awal saat startup, dan provider aktif berikutnya disusun menjadi fallback. Jika hanya `NVIDIA_API_KEY` yang diisi, NVIDIA menjadi model awal dan daftar fallback tidak dibuat. Jika Groq dan NVIDIA diisi, Groq menjadi model awal dan NVIDIA fallback. Tidak wajib mengisi keempat API key.

Model default saat startup:

| Provider | Model |
|---|---|
| Groq | `openai/gpt-oss-20b` |
| Mistral | `ministral-3b-latest` |
| NVIDIA | `nvidia/nemotron-3-super-120b-a12b` |
| Gemini | `gemini-2.5-flash` |

Pastikan model ID tersedia di akun provider. Di Telegram/Discord, gunakan `/model` untuk memilih model jika command tersebut tersedia pada versi Hermes dan channel yang digunakan. Pilihan model lewat chat tidak mengubah urutan fallback yang dibuat saat startup.

## Telegram dan Discord

- `TELEGRAM_BOT_TOKEN`: token dari BotFather.
- `TELEGRAM_ALLOWED_USERS`: ID user Telegram yang diizinkan.
- `DISCORD_BOT_TOKEN`: token bot Discord.
- `DISCORD_ALLOWED_USERS`: ID user Discord yang diizinkan.
- `DISCORD_ALLOWED_CHANNELS`: ID channel yang diizinkan.
- `DISCORD_FREE_RESPONSE_CHANNELS`: ID channel yang boleh dibalas tanpa mention.
- `DISCORD_AUTO_THREAD=false`: menonaktifkan pembuatan thread otomatis.

Aktifkan **Message Content Intent** di Discord Developer Portal bila dibutuhkan. Tambahkan Railway Volume pada `/opt/data` agar data bertahan saat redeploy. Jangan commit API key atau token ke GitHub.

## Catatan

Paket ini memakai image resmi `nousresearch/hermes-agent:latest` dan membungkus startup untuk memilih mode. Skrip dan konfigurasi dapat diperiksa dari repository. Build Docker dan deployment Railway harus tetap diuji di project kamu setelah upload.
