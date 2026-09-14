# FCB Magisk Module — faacb

Clipboard PC ↔ HP via root. Paste emoji utuh tanpa buka aplikasi, keyboard tetap GBoard.

## Isi

```
FCB-Magisk/
└── module/                     # root project module (yg di-zip)
    ├── module.prop             # id=faacb, versi (naikkan tiap update!)
    ├── customize.sh            # jalan sekali saat install
    ├── service.sh              # jalan tiap boot (root): log + grant izin manager
    ├── uninstall.sh            # bersih-bersih saat module dihapus
    ├── zip.py                  # pack -> build/faacb-v<version>.zip
    ├── META-INF/com/google/android/
    │   ├── update-binary       # installer (Magisk v20.4+)
    │   └── updater-script      # #MAGISK
    ├── system/bin/faacb        # CLI: faacb set <b64> | faacb get | faacb paste
    ├── helper/
    │   ├── src/.../Main.java   # helper Java (reflection ServiceManager)
    │   ├── build-dex.py        # compile -> classes.dex
    │   └── classes.dex         # hasil build (dikomit, dibutuhkan runtime)
    ├── manager/                # project APK manager (com.faa.fcbmod)
    │   ├── AndroidManifest.xml # label "FCB Manager", icon custom
    │   ├── build.py            # build -> build/FcbManager.apk
    │   ├── src/...             # ClipReceiver + MainActivity (grant UI)
    │   └── res/...             # icon launcher
    ├── system/app/FcbManager/
    │   └── FcbManager.apk      # copy hasil build manager (auto-mount)
    └── build/                  # output zip (jangan dikomit)
```

## Cara build

```bat
:: 1. dex helper
cd module\helper && python build-dex.py && cd ..\..

:: 2. APK manager
cd module\manager && python build.py && cd ..\..

:: 3. salin APK ke system/app
copy module\manager\build\FcbManager.apk module\system\app\FcbManager\

:: 4. pack zip
cd module && python zip.py
:: -> build\faacb-v1.0.0.zip
```

Butuh JDK + SDK build-tools (lihat `example-tools/REQUIREMENTS.txt`
di repo Example-Build, atau ../example-tools bila sefolder).

## Cara install di HP

1. Flash `build/faacb-v*.zip` via aplikasi Magisk (Modules → Install from storage),
   lalu **reboot**.
2. Buka aplikasi **FCB Manager** sekali (opsional, untuk cek status/grant).
3. Tes dari PC:
   ```bat
   adb shell su -c "faacb set $(python -c "import base64,sys;print(base64.b64encode(sys.argv[1].encode()).decode())" "halo 🩵")"
   adb shell su -c faacb get
   ```

## Perintah faacb (di HP, sebagai root)

```
faacb set <base64>   taruh teks ke clipboard (base64 = anti masalah quote)
faacb get            cetak isi clipboard ke stdout
faacb paste          tekan tombol PASTE di kolom aktif (keyevent 279)
```

## Versi

Naikkan `version` + `versionCode` di `module.prop` **setiap update/fix**,
lalu rebuild zip (`python zip.py` membaca versi otomatis).

## Client PC (`client/`)

UI tkinter untuk pakai module dari PC (tidak perlu hafal command).
Isi: `fcc.py` + `fcb.vbs` (salinan dari repo Faa-Clipboard-FCB —
kalau ada update di sana, copy ulang ke sini).

### Cara pasang

1. Install Python 3.8+ (sudah termasuk `tkinter`) dan ADB di PATH.
2. Sambungkan HP (`adb devices`), pastikan module faacb sudah
   terinstall + reboot (lihat atas).
3. Double-click `fcb.vbs` (tanpa jendela cmd), atau:
   ```bat
   python fcc.py
   ```

### Installer portable (Windows)

Di folder `client/` ada installer sekali klik:

- `install.bat` — copy client ke `%LOCALAPPDATA%\FCB`, daftarkan
  `fcc` ke PATH user, bikin shortcut Desktop + Start Menu
  (icon anime). Buka terminal **baru** lalu ketik `fcb`.
  Tanpa admin. Butuh `pythonw` di PATH.
- `uninstall.bat` — hapus shortcut, PATH, dan folder install.
- `install.sh` — versi Linux (`~/.local/bin/fcb` + shortcut menu,
  `./install.sh --uninstall` untuk hapus). Icon `icon.png`.

### Cara setup (sekali saja)

1. Buka tab **PTH**, pilih device HP di dropdown.
2. Dropdown **Mode**: pilih **Module (root)** (atau biarkan bila itu default).
3. Di HP: tap kolom teks sampai GBoard muncul (kursor aktif).
4. Paste teks ber-emoji → log harusnya nongol `Mode faacb-root...`
   + `[faacb 1/1] OK`, teks masuk utuh.
5. Grant root: saat pertama dipakai, allow popup Magisk untuk Shell
   (atau permanen di pengaturan Superuser). Tanpa ini mode root
   turun otomatis ke mode lain (dicatat di log).

Tab **HTP** buat arah sebaliknya (copy di HP → Ctrl+V di PC),
Tab **Manual** berisi panduan + troubleshooting di dalam aplikasi.

## Lisensi

Ikut lisensi project FCB (MIT).
