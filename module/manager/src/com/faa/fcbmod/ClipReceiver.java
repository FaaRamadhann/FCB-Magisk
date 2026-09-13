package com.faa.fcbmod;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;

/**
 * Terima teks via ADB broadcast, taruh ke clipboard HP (unicode/emoji utuh
 * karena lewat Java API, bukan KeyCharacterMap).
 *
 *   adb shell am broadcast -a com.faa.fcbmod.SET \
 *       -n com.faa.fcbmod/.ClipReceiver -e text "halo 🩵"
 */
public class ClipReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        if ("com.faa.fcbmod.SET".equals(intent.getAction())) {
            String text = intent.getStringExtra("text");
            if (text != null) {
                ClipboardManager cm = (ClipboardManager)
                        context.getSystemService(Context.CLIPBOARD_SERVICE);
                cm.setPrimaryClip(ClipData.newPlainText("fcb", text));
                // bukti untuk pengirim via `am broadcast` (terlihat di output)
                setResultCode(Activity.RESULT_OK);
                setResultData("FCB-OK");
            }
        }
    }
}
