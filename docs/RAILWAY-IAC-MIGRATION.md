# Migrasi Railway Config-as-Code ke Infrastructure as Code

**Batas akhir legacy Config-as-Code: 1 Desember 2026.** Railway menghentikan pembacaan `railway.json` dan `railway.toml` pada tanggal tersebut. Service baru tidak dapat memakai format lama. Penggantinya adalah Railway Infrastructure as Code dengan file proyek seperti `.railway/railway.ts`.

> **Penting untuk repo ini:** jangan membuat satu konfigurasi generik lalu langsung menerapkannya. Repository ini dapat dipakai oleh tiga Railway service berbeda—Dashboard, Variables, dan Ubuntu—dengan Dockerfile, Watch Paths, domain, volume, dan Variables yang tidak sama. Pengaturan aktual hanya dapat dipertahankan dengan menarik konfigurasi dari project Railway yang benar.

Dokumentasi resmi: [Infrastructure as Code](https://docs.railway.com/infrastructure-as-code), [Config-as-Code migration](https://docs.railway.com/config-as-code), dan [CLI](https://docs.railway.com/guides/cli).

## 1. Yang perlu dipertahankan

| Service | Build/Dockerfile | Variables utama | Penyimpanan dan jaringan |
| --- | --- | --- | --- |
| Dashboard | Root `Dockerfile` | `DEPLOY_MODE=dashboard`, `USERNAME`, `PASSWORD`, `SECRET` | Volume sendiri di `/opt/data`; domain hanya setelah auth publik/OIDC/access gateway benar |
| Variables | Root `Dockerfile` | `DEPLOY_MODE=variables`, minimal satu provider key, token bot bila dipakai | Volume sendiri di `/opt/data`; domain publik biasanya tidak diperlukan |
| Ubuntu Terminal | `ubuntu/Dockerfile`; Root Directory kosong | `TERMINAL_USER`, `TERMINAL_PASSWORD`, `HERMES_AUTOSTART` | Volume sendiri di `/opt/data`; volume berbeda di `/data` bila file terminal perlu persisten; domain target port 8080 |

Jangan berbagi volume antarservice. Jangan menjalankan token Telegram/Discord yang sama pada lebih dari satu Gateway. Secrets tetap berada di Railway Variables—jangan menyalinnya ke file IaC, git, issue, atau screenshot.

## 2. Sebelum menjalankan migrasi

1. Pastikan kamu berada di salinan repo yang benar dan buat backup/commit dari perubahan lokal.
2. Buka Railway Dashboard dan pastikan project serta environment yang dipilih memang project Hermes yang ingin dimigrasikan.
3. Catat tiga service dan identitasnya: Dashboard, Variables, Ubuntu. Periksa masing-masing Dockerfile Path, Root Directory, Watch Paths, restart policy, port/domain, volume mount, healthcheck, dan service variables.
4. Catat nama variabel, tetapi **jangan menyalin nilai rahasia**. Pastikan volume dan data persisten tetap terpasang pada service yang benar.
5. Pasang/upgrade Railway CLI mengikuti [panduan resmi CLI](https://docs.railway.com/guides/cli), lalu login.

Jangan menghapus `railway.json` saat persiapan ini.

## 3. Tarik konfigurasi project yang sebenarnya

Dari direktori repo, tautkan CLI ke project dan environment Railway yang benar:

```bash
railway login
railway link
railway config pull --force
```

Periksa file yang dihasilkan dan pastikan seluruh service yang ingin dikelola terlihat. Simpan salinan lokal sebelum menjalankan perintah migrasi berikutnya karena perintah pull/migrate dapat memperbarui file konfigurasi lokal.

Jika CLI hanya mengembalikan satu service sementara project-mu memiliki tiga service, **berhenti dulu**. Jangan menerapkan hasil tersebut. Pastikan project/environment benar, lalu gunakan workflow IaC project-level untuk memasukkan ketiga service dengan service ID dan pengaturan masing-masing yang nyata.

## 4. Konversi dan tinjau rencana

Jalankan migrasi dalam mode preview terlebih dahulu:

```bash
railway config migrate
railway config plan
```

Periksa output dan diff `.railway/railway.ts`. Hasil yang benar harus mempertahankan tiga service terpisah beserta build path, Root Directory, restart policy, networking, volume, dan konfigurasi non-rahasia yang memang diperlukan.

**Jangan lanjut** bila plan menunjukkan salah satu hal berikut:
- service akan dihapus, diganti nama, atau dibuat duplikat;
- Volume `/opt/data` atau `/data` akan dilepas/dipindahkan;
- Dockerfile Path Dashboard/Variables/Ubuntu menjadi sama;
- domain, target port, atau restart policy berubah tanpa sengaja;
- Variables atau environment berpindah ke service/environment lain.

Perbaiki file IaC dan ulangi `railway config plan` sampai perubahan yang ditampilkan sesuai dengan konfigurasi yang memang ingin dipertahankan.

## 5. Terapkan dengan hati-hati

Setelah seluruh perubahan sudah ditinjau dan sesuai:

```bash
railway config apply
```

Jangan menggunakan opsi penghapusan file legacy secara otomatis sebelum verifikasi. Setelah apply, periksa Railway Dashboard satu per satu:

- ketiga service masih ada dan terhubung ke service yang benar;
- Dockerfile Path serta Root Directory benar;
- setiap service memiliki volume sendiri dengan mount yang tepat;
- Variables dan secrets tetap pada service/environment yang benar;
- domain dan target port tetap sesuai;
- Deploy Logs tidak menunjukkan perubahan konfigurasi atau startup yang tidak diharapkan.

Lakukan tes per service. Dashboard harus dilindungi sesuai kebutuhan aksesnya, Variables harus menjalankan Gateway yang diinginkan, dan Ubuntu harus membuka terminal serta menjalankan Gateway hanya bila `HERMES_AUTOSTART=true`.

## 6. Setelah migrasi berhasil

1. Simpan dan commit `.railway/railway.ts` beserta file IaC pendukung yang memang dibutuhkan.
2. Hapus `railway.json` hanya setelah seluruh service sudah dikelola oleh IaC, plan/apply bersih, dan ketiga service lolos pemeriksaan di atas.
3. Hapus pola `/railway.json` dari Watch Paths masing-masing service lama.
4. Untuk perubahan konfigurasi IaC berikutnya, jalankan plan lalu apply melalui Railway CLI. Perubahan file IaC tidak sama dengan perubahan source aplikasi dan tidak boleh dianggap otomatis menerapkan konfigurasi.
5. Simpan backup konfigurasi serta data volume. Volume Railway bukan pengganti backup.

## 7. Jika belum siap migrasi

Sampai migrasi selesai, pertahankan `railway.json` untuk service lama dan lakukan pengaturan service baru langsung melalui Railway Dashboard. Jangan mengandalkan Config-as-Code lama untuk service baru. Selesaikan migrasi sebelum **1 Desember 2026** agar konfigurasi tidak hilang saat Railway berhenti membaca file legacy.
