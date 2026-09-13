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

## Lisensi

Ikut lisensi project FCB (MIT).
