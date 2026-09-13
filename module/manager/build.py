"""
build.py — build APK manager FCB (com.faa.fcbmod) tanpa Android Studio.
Diadaptasi dari ex-build.py Example-Build (JFK: JDK + SDK build-tools).

Cara pakai (dari folder manager/):
    python build.py
Hasil: build/FcbManager.apk -> salin ke ../system/app/FcbManager/
"""
import os
import subprocess
import sys

# ---------------- KONFIG ----------------
APP_NAME = "FcbManager"
MIN_SDK = "24"
BUILD_TOOLS = r"C:\AndroidSDK\build-tools\35.0.0"
ANDROID_JAR = r"C:\AndroidSDK\platforms\android-34\android.jar"
JAVA_HOME = r"C:\Program Files\Java\jdk-21.0.10"
KEYSTORE = "debug.keystore"   # relatif ke folder manager/
KEY_ALIAS = "fcbmod"
STOREPASS = "android"
KEYPASS = "android"
# ----------------------------------------


def run(cmd, cwd):
    print("  $", " ".join(cmd))
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print((r.stdout or "")[-2000:])
        print((r.stderr or "")[-2000:])
        sys.exit("GAGAL (rc=%d): %s" % (r.returncode, cmd[0]))
    return r


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    for must in ("AndroidManifest.xml", "src"):
        if not os.path.exists(os.path.join(root, must)):
            sys.exit("Bukan project Android: %s hilang" % must)

    javac = os.path.join(JAVA_HOME, "bin", "javac.exe")
    keytool = os.path.join(JAVA_HOME, "bin", "keytool.exe")
    d8 = os.path.join(BUILD_TOOLS, "d8.bat")
    aapt = os.path.join(BUILD_TOOLS, "aapt.exe")
    zipalign = os.path.join(BUILD_TOOLS, "zipalign.exe")
    apksigner = os.path.join(BUILD_TOOLS, "apksigner.bat")
    build = os.path.join(root, "build")
    os.makedirs(os.path.join(build, "obj"), exist_ok=True)
    os.makedirs(os.path.join(build, "dex"), exist_ok=True)

    print("[1/6] kumpulkan source...")
    sources = []
    for dp, _, fns in os.walk(os.path.join(root, "src")):
        sources += [os.path.join(dp, f) for f in fns if f.endswith(".java")]
    if not sources:
        sys.exit("Tidak ada .java di src/")

    print("[2/6] javac...")
    with open(os.path.join(build, "sources.txt"), "w") as fh:
        fh.write("\n".join(sources))
    run([javac, "--release", "8", "-classpath", ANDROID_JAR,
         "-d", os.path.join(build, "obj"),
         "@" + os.path.join(build, "sources.txt")], root)

    print("[3/6] d8...")
    classes = []
    for dp, _, fns in os.walk(os.path.join(build, "obj")):
        classes += [os.path.join(dp, f) for f in fns if f.endswith(".class")]
    run([d8, "--min-api", MIN_SDK, "--lib", ANDROID_JAR,
         "--output", os.path.join(build, "dex")] + classes, root)

    print("[4/6] aapt package...")
    cmd = [aapt, "package", "-f", "-M", "AndroidManifest.xml"]
    if os.path.isdir(os.path.join(root, "res")):
        cmd += ["-S", "res"]
    cmd += ["-I", ANDROID_JAR, "-F", os.path.join(build, "unsigned.apk")]
    run(cmd, root)
    run([aapt, "add", os.path.join(build, "unsigned.apk"), "classes.dex"],
        os.path.join(build, "dex"))

    print("[5/6] keystore (sekali saja)...")
    ks = os.path.join(root, KEYSTORE)
    if not os.path.exists(ks):
        run([keytool, "-genkeypair", "-keystore", ks, "-alias", KEY_ALIAS,
             "-keyalg", "RSA", "-keysize", "2048", "-validity", "10950",
             "-storepass", STOREPASS, "-keypass", KEYPASS,
             "-dname", "CN=%s" % APP_NAME], root)

    print("[6/6] zipalign + apksigner...")
    run([zipalign, "-f", "4", os.path.join(build, "unsigned.apk"),
         os.path.join(build, "aligned.apk")], root)
    out_apk = os.path.join(build, "%s.apk" % APP_NAME)
    run([apksigner, "sign", "--ks", ks, "--ks-key-alias", KEY_ALIAS,
         "--ks-pass", "pass:%s" % STOREPASS, "--key-pass", "pass:%s" % KEYPASS,
         "--out", out_apk, os.path.join(build, "aligned.apk")], root)
    run([apksigner, "verify", out_apk], root)
    print("\nSELESAI: %s" % out_apk)


if __name__ == "__main__":
    main()
