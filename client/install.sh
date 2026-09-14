#!/bin/sh
# FCB installer (Linux):  ./install.sh [--uninstall]
# - Salin client ke ~/.local/share/fcb
# - Wrapper ~/.local/bin/fcb  (pastikan ~/.local/bin ada di PATH)
# - Shortcut menu ~/.local/share/applications/fcb.desktop (icon anime)
set -e
APP=fcb
NAME="FCB Clipboard"
SRC=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
DEST="$HOME/.local/share/fcb"
BIN="$HOME/.local/bin/$APP"
DESK="$HOME/.local/share/applications/$APP.desktop"

if [ "$1" = "--uninstall" ] || [ "$1" = "uninstall" ]; then
  echo "hapus $DEST, $BIN, $DESK ..."
  rm -rf "$DEST" "$BIN" "$DESK"
  echo "selesai."
  exit 0
fi

command -v python3 >/dev/null || { echo "butuh python3!"; exit 1; }
[ -f "$SRC/fcc.py" ] || { echo "fcc.py tidak ada di $SRC"; exit 1; }

echo "[1/3] copy ke $DEST ..."
mkdir -p "$DEST" "$HOME/.local/bin" "$(dirname "$DESK")"
cp -f "$SRC/fcc.py" "$SRC/icon.png" "$DEST/"

echo "[2/3] wrapper $BIN ..."
printf '#!/bin/sh\nexec python3 "%s/fcc.py" "$@"\n' "$DEST" > "$BIN"
chmod +x "$BIN"

echo "[3/3] shortcut menu ..."
printf '[Desktop Entry]\nName=%s\nExec=%s\nIcon=%s/icon.png\nTerminal=false\nType=Application\nCategories=Utility;\n' \
  "$NAME" "$BIN" "$DEST" > "$DESK"
chmod +x "$DESK"
command -v update-desktop-database >/dev/null && update-desktop-database "$(dirname "$DESK")" || true

echo ""
echo "SELESAI. Buka terminal BARU lalu ketik:  $APP"
echo "(pastikan ~/.local/bin ada di PATH)"
