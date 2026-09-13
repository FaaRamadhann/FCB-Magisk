"""
build-dex.py — compile helper Java (faacb) menjadi classes.dex.
Jalankan dari folder helper/:  python build-dex.py
Hasil: classes.dex (dikomit ke module, dibutuhkan faacb saat runtime).
Butuh: JDK + d8 (lihat ../REQUIREMENTS bila ada, atau example-tools).
"""
import os
import subprocess
import sys

BT = r"C:\AndroidSDK\build-tools\35.0.0"
ANDROID_JAR = r"C:\AndroidSDK\platforms\android-34\android.jar"
JAVA_HOME = r"C:\Program Files\Java\jdk-21.0.10"

ROOT = os.path.dirname(os.path.abspath(__file__))


def run(cmd):
    print("  $", " ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print((r.stdout or "")[-1500:])
        print((r.stderr or "")[-1500:])
        sys.exit("GAGAL: %s" % cmd[0])


def main():
    javac = os.path.join(JAVA_HOME, "bin", "javac.exe")
    d8 = os.path.join(BT, "d8.bat")
    obj = os.path.join(ROOT, "obj")
    os.makedirs(obj, exist_ok=True)
    srcs = []
    for dp, _, fns in os.walk(os.path.join(ROOT, "src")):
        srcs += [os.path.join(dp, f) for f in fns if f.endswith(".java")]
    if not srcs:
        sys.exit("Tidak ada .java di src/")
    run([javac, "--release", "8", "-classpath", ANDROID_JAR, "-d", obj] + srcs)
    classes = []
    for dp, _, fns in os.walk(obj):
        classes += [os.path.join(dp, f) for f in fns if f.endswith(".class")]
    run([d8, "--min-api", "24", "--lib", ANDROID_JAR,
         "--output", ROOT] + classes)
    # d8 menulis classes.dex di ROOT (sesuai --output dir)
    dex = os.path.join(ROOT, "classes.dex")
    if not os.path.exists(dex):
        sys.exit("classes.dex tidak terbentuk!")
    print("SELESAI:", dex)


if __name__ == "__main__":
    main()
