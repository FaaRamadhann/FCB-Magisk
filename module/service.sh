#!/system/bin/sh
# service.sh — jalan otomatis tiap boot sebagai root (late_start).
MODDIR=${0%/*}

log -t faacb "service start (faacb v1.0.0)" 2>/dev/null

# Amankan izin tulis clipboard untuk manager APK (membantu jalur fallback
# broadcast bila dipakai; tidak wajib untuk faacb CLI karena sudah root).
appops set com.faa.fcbmod WRITE_CLIPBOARD allow 2>/dev/null
appops set --uid com.faa.fcbmod WRITE_CLIPBOARD allow 2>/dev/null

log -t faacb "service ready" 2>/dev/null
