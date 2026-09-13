package com.faa.fcbmod;

import android.app.Activity;
import android.app.AppOpsManager;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.Settings;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import java.io.DataOutputStream;

/**
 * Layar info + perizinan sekali sentuh.
 * - Status izin clipboard (cek via AppOpsManager).
 * - Tombol root: menjalankan `appops set` sebagai root (popup Superuser).
 * - Tombol settings: deep-link ke App Info bila non-root.
 * Icon launcher selalu muncul (tanpa fitur hide).
 */
public class MainActivity extends Activity {

    static final String PKG = "com.faa.fcbmod";
    // nama op clipboard (tidak ada konstantanya di SDK, jadi hardcode;
    // bila salah, checkOp melempar -> status jadi UNKNOWN, bukan crash)
    static final String OP_WRITE_CLIPBOARD = "android:write_clipboard";

    final TextView[] statusBox = new TextView[1];

    /** null = tidak bisa dicek otomatis. */
    Boolean isGranted() {
        try {
            AppOpsManager am = (AppOpsManager) getSystemService(APP_OPS_SERVICE);
            int mode = am.checkOpNoThrow(OP_WRITE_CLIPBOARD,
                    android.os.Process.myUid(), getPackageName());
            return mode == AppOpsManager.MODE_ALLOWED;
        } catch (Exception e) {
            return null;
        }
    }

    void refreshStatus() {
        Boolean g = isGranted();
        statusBox[0].setText(g == null
                ? "Izin clipboard: tidak bisa dicek otomatis.\n"
                  + "Kalau paste emoji gagal diam-diam, pakai tombol di bawah."
                : (g ? "Izin clipboard: OK (full-otomatis aktif)"
                     : "Izin clipboard: BELUM (paste emoji akan gagal diam-diam)"));
    }

    /** Jalankan `appops set` sebagai root. Return true bila exit 0. */
    boolean grantViaRoot() {
        String cmd = "appops set " + PKG + " WRITE_CLIPBOARD allow\n"
                + "appops set --uid " + PKG + " WRITE_CLIPBOARD allow\n";
        try {
            Process p = Runtime.getRuntime().exec(new String[]{"su", "-c", cmd});
            DataOutputStream os = new DataOutputStream(p.getOutputStream());
            os.writeBytes("exit\n");
            os.flush();
            p.waitFor();
            return p.exitValue() == 0;
        } catch (Exception e) {
            return false;
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        LinearLayout lay = new LinearLayout(this);
        lay.setOrientation(LinearLayout.VERTICAL);
        lay.setPadding(40, 60, 40, 40);

        TextView info = new TextView(this);
        info.setText("FCB Manager aktif.\nBroadcast ADB jalan tanpa buka app ini.\n"
                + "GBoard tidak berubah sama sekali.");
        info.setTextSize(16);
        lay.addView(info);

        TextView status = new TextView(this);
        status.setTextSize(16);
        status.setPadding(0, 40, 0, 10);
        lay.addView(status);
        statusBox[0] = status;

        Button rootBtn = new Button(this);
        rootBtn.setText("Grant via Root");
        rootBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                boolean ok = grantViaRoot();
                Toast.makeText(MainActivity.this,
                        ok ? "Grant dikirim, cek status di bawah"
                           : "Gagal (tidak ada root / ditolak). Pakai tombol Settings.",
                        Toast.LENGTH_LONG).show();
                refreshStatus();
            }
        });
        lay.addView(rootBtn);

        Button setBtn = new Button(this);
        setBtn.setText("Buka Settings (non-root)");
        setBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS,
                        Uri.parse("package:" + getPackageName()));
                startActivity(i);
            }
        });
        lay.addView(setBtn);

        setContentView(lay);
        refreshStatus();
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (statusBox[0] != null) {
            refreshStatus();
        }
    }
}
