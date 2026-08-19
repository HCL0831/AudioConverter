import os
import sys
import shutil
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import PyInstaller.__main__

def build_exe():
    print("=" * 60)
    print("開始打包 [音檔轉檔與壓縮大師] 為獨立 EXE 執行檔...")
    print("=" * 60)

    project_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(project_dir, "main.py")
    
    # 使用本機暫存目錄進行編譯，避開網路/虛擬磁碟 (如 T:) 的權限問題
    temp_dir = os.path.join(tempfile.gettempdir(), "pyinstaller_audio_build")
    dist_dir = os.path.join(temp_dir, "dist")
    build_dir = os.path.join(temp_dir, "build")
    
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)
    os.makedirs(dist_dir, exist_ok=True)
    os.makedirs(build_dir, exist_ok=True)

    internal_name = "AudioConverter"
    final_name = "音檔轉檔與壓縮大師.exe"

    version_file = os.path.join(project_dir, "version_info.txt")

    pyinstaller_args = [
        main_script,
        f"--name={internal_name}",
        "--onefile",
        "--noconsole",
        "--clean",
        f"--version-file={version_file}",
        "--collect-all=customtkinter",
        "--collect-all=tkinterdnd2",
        "--collect-all=imageio_ffmpeg",
        f"--distpath={dist_dir}",
        f"--workpath={build_dir}",
        f"--specpath={temp_dir}",
    ]

    print(f"正在執行 PyInstaller (暫存目錄: {temp_dir})...")
    PyInstaller.__main__.run(pyinstaller_args)

    # 檢查產生的 EXE
    exe_path = os.path.join(dist_dir, f"{internal_name}.exe")
    if os.path.exists(exe_path):
        target_path = os.path.join(project_dir, final_name)
        shutil.copyfile(exe_path, target_path)
        print("=" * 60)
        print("[OK] 打包成功！")
        print(f"已將執行檔輸出至專案根目錄: {target_path}")
        print(f"檔案大小: {os.path.getsize(target_path) / (1024*1024):.2f} MB")
        print("您可直接將此 .exe 複製到任何 Windows 電腦上執行，無需安裝 Python 或任何依賴。")
        print("=" * 60)
        
        # 清理專案目錄下的舊 build / dist 資料夾與 spec
        for folder in ["build", "dist"]:
            p = os.path.join(project_dir, folder)
            if os.path.exists(p):
                shutil.rmtree(p, ignore_errors=True)
        spec_file = os.path.join(project_dir, "音檔轉檔與壓縮大師.spec")
        if os.path.exists(spec_file):
            try: os.remove(spec_file)
            except: pass
    else:
        print("[ERROR] 打包完成但找不到生成的 .exe 檔案，請檢查錯誤訊息。")

if __name__ == "__main__":
    build_exe()
