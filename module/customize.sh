#!/system/bin/sh
# customize.sh — dijalankan sekali saat install module (oleh update-binary).
# MODPATH sudah di-set oleh update-binary.

ui_print "- customize faacb..."
ui_print "  faacb CLI   : system/bin/faacb (adb shell faacb ...)"
ui_print "  manager APK : system/app/FcbManager (auto-mount)"
ui_print "  Butuh root saat dipakai (Magisk su)."
ui_print "  Setelah reboot, tes: adb shell su -c 'faacb get'"
