#!/system/bin/sh
# uninstall.sh — jalan saat module dihapus. System/app ikut ter-unmount
# otomatis oleh Magisk, jadi di sini hanya bersih-bersih sisa bila ada.
rm -rf /data/adb/modules/faacb 2>/dev/null
rm -rf /data/adb/modules_update/faacb 2>/dev/null
echo "faacb dihapus."
