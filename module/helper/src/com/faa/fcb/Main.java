package com.faa.fcb;

import android.content.ClipData;
import android.os.IBinder;
import java.lang.reflect.Method;

/**
 * Helper clipboard via root (dijalankan lewat app_process, tanpa Activity).
 * ClipboardManager butuh Context, jadi akses IClipboard langsung via
 * ServiceManager + reflection (tidak ada hidden-API di compile-time).
 *
 *   set <teks>  -> taruh teks (unicode/emoji utuh) ke clipboard
 *   get          -> cetak isi clipboard ke stdout
 */
public class Main {

    static Object clipboard() throws Exception {
        Class<?> sm = Class.forName("android.os.ServiceManager");
        Method getService = sm.getMethod("getService", String.class);
        IBinder b = (IBinder) getService.invoke(null, "clipboard");
        Class<?> stub = Class.forName("android.content.IClipboard$Stub");
        Method asInterface = stub.getMethod("asInterface", IBinder.class);
        return asInterface.invoke(null, b);
    }

    public static void main(String[] args) throws Exception {
        if (args.length == 0) {
            System.err.println("pakai: set <teks> | get");
            return;
        }
        Object clip = clipboard();
        if ("set".equals(args[0]) && args.length > 1) {
            ClipData data = ClipData.newPlainText("fcb", args[1]);
            Method set = clip.getClass().getMethod("setPrimaryClip",
                    ClipData.class, String.class, int.class);
            set.invoke(clip, data, "com.faa.fcbmod", 0);
        } else if ("get".equals(args[0])) {
            Method get = clip.getClass().getMethod("getPrimaryClip",
                    String.class, int.class);
            ClipData data = (ClipData) get.invoke(clip, "com.faa.fcbmod", 0);
            String out = "";
            if (data != null && data.getItemCount() > 0
                    && data.getItemAt(0).getText() != null) {
                out = data.getItemAt(0).getText().toString();
            }
            System.out.print(out);
        } else {
            System.err.println("pakai: set <teks> | get");
        }
    }
}
