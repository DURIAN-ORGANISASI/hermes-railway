# Hermes Agent Railway — mode Railway Variables

Mode ini tidak menyalakan dashboard. Semua API key dan token ditambahkan di **Railway → service Hermes → Variables**. Kamu tidak perlu mengisi `MODEL_PROVIDER`, `MODEL_ID`, `PROVIDER_API`, atau `FALLBACK_MODELS`.

## Variabel yang dipakai

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

**Satu API key sudah cukup.** Variabel provider lain boleh tidak dibuat atau dibiarkan kosong. Contoh konfigurasi minimal untuk NVIDIA saja:

```dotenv
DEPLOY_MODE=variables
NVIDIA_API_KEY=isi_api_key_nvidia
```

Untuk Gemini, `GOOGLE_API_KEY` juga diterima sebagai alias jika `GEMINI_API_KEY` tidak diisi.

## Fallback otomatis

Jika ada beberapa API key yang diisi, skrip mendeteksi key yang tidak kosong dan membentuk fallback otomatis dengan urutan tetap berikut:

1. Groq — `GROQ_API_KEY`
2. Mistral — `MISTRAL_API_KEY`
3. NVIDIA — `NVIDIA_API_KEY`
4. Gemini — `GEMINI_API_KEY` atau `GOOGLE_API_KEY`

Provider aktif pertama menjadi model awal saat startup; provider aktif berikutnya menjadi fallback. Contoh: jika hanya `NVIDIA_API_KEY` diisi, NVIDIA menjadi model awal tanpa daftar fallback. Jika Groq dan NVIDIA diisi, Groq menjadi model awal dan NVIDIA menjadi fallback. Tidak perlu mengisi keempat key. Fallback bergantung pada dukungan konfigurasi dan jenis error yang ditangani Hermes; tidak semua kegagalan atau limit provider pasti bisa dialihkan.

Model default startup:

| Provider | Model default startup |
|---|---|
| Groq | `openai/gpt-oss-20b` |
| Mistral | `ministral-3b-latest` |
| NVIDIA | `nvidia/nemotron-3-super-120b-a12b` |
| Gemini | `gemini-2.5-flash` |

Pastikan model ID masih tersedia pada akun/provider kamu. Kamu dapat memilih atau mengganti model melalui perintah `/model` di Telegram/Discord jika command dan provider tersebut didukung oleh versi Hermes yang digunakan. Pemilihan model lewat chat tidak mengubah urutan fallback otomatis yang dibuat saat startup.

## Telegram dan Discord

- `TELEGRAM_BOT_TOKEN`: token bot dari BotFather.
- `TELEGRAM_ALLOWED_USERS`: ID user Telegram yang diizinkan; format mengikuti dokumentasi Hermes.
- `DISCORD_BOT_TOKEN`: token bot Discord.
- `DISCORD_ALLOWED_USERS`: ID user Discord yang diizinkan.
- `DISCORD_ALLOWED_CHANNELS`: ID channel yang boleh dipakai.
- `DISCORD_FREE_RESPONSE_CHANNELS`: ID channel yang boleh dibalas tanpa mention.
- `DISCORD_AUTO_THREAD=false`: menonaktifkan pembuatan thread otomatis.

Aktifkan **Message Content Intent** di Discord Developer Portal jika dibutuhkan. Tambahkan Railway Volume dengan mount path `/opt/data` untuk mempertahankan data saat redeploy. Jangan pernah menaruh API key/token asli di GitHub atau README.
