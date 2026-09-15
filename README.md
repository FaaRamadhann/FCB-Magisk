# Faa Clipboard Magisk (FCB)

[![Magisk](https://img.shields.io/badge/Magisk-Module-00af9c)](https://github.com/topjohnwu/Magisk) [![KernelSU](https://img.shields.io/badge/KernelSU-Module-323136)](https://github.com/tiann/KernelSU) [![APatch](https://img.shields.io/badge/APatch-Module-334d83)](https://github.com/apatch/apatch) [![License: MIT](https://img.shields.io/badge/License-MIT-lime.svg)](LICENSE)

---

## Apa itu FCB?

Modul **Magisk / KernelSU / APatch** untuk copy-paste dua arah **PC ↔ HP** — termasuk **emoji utuh** (yang tidak bisa diketik via `adb shell input`). Punya CLI (`faacb`), companion app (manager), dan client PC (tkinter). Keyboard tetap GBoard, tanpa buka aplikasi tiap paste.

## Fitur

- **CLI `faacb`** — `set <base64>` / `get` / `paste` via root (base64 = anti masalah quote)
- **Emoji utuh 100%** — via Java API (`ClipboardManager`), bukan KeyCharacterMap (yang NPE)
- **Auto-fallback** — client PC otomatis pilih jalur: faacb-root → helper APK → ketik biasa
- **Manager app** (`com.faa.fcbmod`) — status izin + grant root + deep-link Settings, icon custom
- **Client PC** (`client/`) — UI tkinter + installer portable (PATH + shortcut Desktop)
- **`zip.py`** untuk mem-packing modul jadi `.zip` (anti-bug backslash `\`)

## Persyaratan

- **Android:** 7.0+ (API 24+, teruji: Android 12 custom ROM, Xiaomi Android 13)
- **Root:** Magisk / KernelSU / APatch (+ reboot setelah install module)
- **PC (untuk client):** Python 3.8+ (sudah termasuk `tkinter`) + ADB di PATH

---

## Cara Install

Ada dua cara: **via PC (Windows/Linux)** atau **via Termux di HP**.

### A. Via PC (Windows / Linux) — pakai `adb push`

**Langkah 0 — Siapkan (clone + pack zip):**

Prasyarat: sudah ada `git` dan `python 3` (versi apa pun) di PC.

```
# 1. Clone repo ini
git clone https://github.com/FaaRamadhann/FCB-Magisk.git
cd FCB-Magisk

# 2. Pack jadi zip (atau langsung pakai faacb-vX.Y.Z.zip yang sudah ada)
cd module
python zip.py
```

Perintah `python zip.py` menghasilkan file:

```
module/build/faacb-v1.0.0.zip
```

**Langkah 1 — Hubungkan HP ke PC:**

Aktifkan **USB Debugging** di HP (Developer Options), lalu colok USB
(atau `adb connect IP:5555` untuk wireless debugging).

```
# Cek HP terdeteksi
adb devices
# Harus muncul status "device"
```

**Langkah 2 — Push zip ke HP:**

```
adb push module/build/faacb-v1.0.0.zip /sdcard/
```

**Langkah 3 — Install lewat manager root (dari HP):**

Buka aplikasi **Magisk / KernelSU / APatch** → **Modul** → **Install dari penyimpanan** → pilih `faacb-v1.0.0.zip`.

Atau via terminal/shell (root):

```
# masuk shell adb
adb shell
# lalu jalankan sebagai root (sesuaikan versi!)
su -c 'magisk --install-module /sdcard/faacb-v1.0.0.zip'
```

**Langkah 4 — Reboot**, lalu cek dari PC:

```
adb shell su -c faacb
# Harus muncul: pakai: faacb set <base64> | faacb get | faacb paste
```

---

### B. Via Termux (di HP, tanpa PC)

Prasyarat: sudah ada **Termux** dan akses **root** (`su`).

**Langkah 1 — Install git & clone:**

```
pkg install -y git python
git clone https://github.com/FaaRamadhann/FCB-Magisk.git
cd FCB-Magisk/module
```

**Langkah 2 — Build zip:**

```
python zip.py
```

**Langkah 3 — Pindahkan zip ke penyimpanan (agar bisa dipilih manager):**

```
cp build/faacb-v*.zip /sdcard/
```

**Langkah 4 — Install via manager root:**

Buka aplikasi **Magisk / KernelSU / APatch** → **Modul** → **Install dari penyimpanan** → pilih zip.

Atau lewat Termux dengan root:

```
su -c 'magisk --install-module /sdcard/faacb-v*.zip'
```

**Langkah 5 — Reboot**, lalu cek:

```
su -c faacb
```

---

## Cara Pakai

```sh
# Taruh teks (unicode/emoji utuh) ke clipboard HP. Teks di-base64 dulu:
su -c "faacb set $(echo -n 'halo 🩵' | base64 | tr -d '\n')"

# Baca clipboard HP (terbatas aturan background Android 10+;
# untuk baca penuh pakai client PC / tab HTP yang via service call)
su -c faacb get

# Tekan tombol PASTE di kolom aktif (sebagai root, lolos INJECT_EVENTS)
su -c faacb paste
```

Atau tanpa hafal command — pakai **client PC** (`client/`, lihat bawah):
double-click `fcb.vbs`, pilih Mode **Module (root)**, paste seperti biasa.

## Struktur Modul

```
FCB-Magisk/
├── README.md
├── LICENSE
├── client/                   # Client PC (salinan repo Faa-Clipboard-FCB)
│   ├── fcc.py                # UI tkinter: PTH (PC→HP) + HTP (HP→PC) + Manual
│   ├── fcb.vbs               # Launcher tanpa console (double-click)
│   ├── install.bat           # Installer Windows: PATH + shortcut Desktop
│   ├── uninstall.bat         # Uninstaller Windows
│   ├── install.sh            # Installer Linux (~/.local/bin/fcb)
│   └── icon.ico / icon.png
├── module/
│   ├── module.prop           # Metadata modul (id faacb, Faa Ramadhan)
│   ├── customize.sh          # Info install (dijalankan sekali)
│   ├── uninstall.sh          # Cleanup saat module dihapus
│   ├── service.sh            # Log tiap boot + grant izin manager
│   ├── zip.py                # Packing repo jadi .zip (forward-slash + chmod)
│   ├── META-INF/...          # Installer Magisk modern (v20.4+)
│   ├── system/bin/faacb      # CLI utama (set/get/paste, wajib root)
│   ├── helper/               # Helper Java (reflection ServiceManager)
│   │   ├── src/.../Main.java # set/get via IClipboard (tanpa hidden-API)
│   │   ├── build-dex.py      # Compile -> classes.dex
│   │   └── classes.dex       # Hasil build (dikomit, dibutuhkan runtime)
│   ├── manager/              # Companion app (tanpa Gradle)
│   │   ├── build/FcbManager.apk # hasil build (TIDAK dikomit, lihat bawah)
│   │   ├── build.py          # Build APK (javac+d8+aapt ala Example-Build)
│   │   ├── AndroidManifest.xml # package com.faa.fcbmod
│   │   ├── src/com/faa/fcbmod/  # ClipReceiver + MainActivity (grant UI)
│   │   ├── res/...           # Icon launcher
│   │   └── debug.keystore    # Backup! Update APK wajib key yang sama
│   └── system/app/FcbManager/
│       └── FcbManager.apk    # Copy hasil build manager (auto-mount)
└── tests/                    # (TODO) tes otomatis tiap rilis
```

### Build manager.apk (tanpa Gradle)

```
cd module/manager
python build.py
```

Hasil: `module/manager/build/FcbManager.apk`.
Lalu salin ke module agar ikut ke-pack:

```
copy module\manager\build\FcbManager.apk module\system\app\FcbManager\
```

Lalu pack module seperti biasa: `cd module && python zip.py` →
`build/faacb-v1.0.0.zip` berisi `system/app/FcbManager/FcbManager.apk`,
dan HP akan memunculkan app **FCB Manager** otomatis setelah reboot.
Buka sekali → cek status / tap **Grant via Root** bila perlu.

Butuh JDK + SDK build-tools. Detail + link download:
https://github.com/FaaRamadhann/Example-Build (README + REQUIREMENTS).

## Troubleshooting

Masalah | Solusi
`faacb: butuh root` | Jalankan dengan `su -c` (atau sebagai root). Tanpa root, pakai mode helper APK / ketik di client.
`faacb: ... classes.dex hilang` | Reinstall module (file korup / belum reboot setelah install).
Paste emoji gagal diam-diam | Buka FCB Manager → tap **Grant via Root** (popup Superuser) atau beri izin clipboard manual. Atau biarkan client yang urus otomatis (mode helper ada self-heal appops).
`faacb get` kosong | Wajar — aturan baca-background Android 10+ berlaku bahkan buat root. Untuk baca penuh pakai tab HTP (service call) di client.
Module tidak aktif setelah install | Reboot dulu (mount butuh reboot). Masih? Cek Magisk → modul centang aktif.
`faacb command not found` (via adb) | Module belum aktif (reboot?) atau shell bukan root: pakai `su -c 'faacb ...'`.
APK manager gagal update (signature) | Update wajib key sama (`module/manager/debug.keystore` di-backup, jangan dikomit); kalau key beda, uninstall `com.faa.fcbmod` dulu.
File `.sh` error aneh setelah clone di Windows | Pastikan LF (repo sudah paksa `eol=lf` di `.gitattributes`); jalankan ulang `python zip.py` setelah fix.

## Versi

Naikkan `version` + `versionCode` di `module/module.prop` **setiap update/fix**,
lalu rebuild zip (`python zip.py` membaca versi otomatis).

## Lisensi

[MIT License](LICENSE) — © 2026 Faa Ramadhan
