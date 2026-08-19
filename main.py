"""
AudioConverter - 音檔轉檔與壓縮大師
Author: HCL
GitHub: https://github.com/HCL0831/AudioConverter
Copyright (c) 2026 HCL. All rights reserved.
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import subprocess
import threading
import imageio_ffmpeg
import re
import sys
import json
import datetime

CONFIG_DIR = os.path.join(os.getenv('APPDATA', os.path.expanduser('~')), 'AudioConverter')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'agreement.json')
CURRENT_DISCLAIMER_VERSION = "2.0"

def is_disclaimer_agreed():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('agreed') is True and data.get('version') == CURRENT_DISCLAIMER_VERSION:
                    return True
    except Exception:
        pass
    return False

def save_disclaimer_agreement():
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'agreed': True,
                'version': CURRENT_DISCLAIMER_VERSION,
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'author': 'HCL'
            }, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving agreement config: {e}")

def get_ffmpeg_path():
    # 1. 嘗試由 imageio_ffmpeg 取得
    try:
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe and os.path.isfile(exe):
            return exe
    except Exception:
        pass

    # 2. 若為 PyInstaller 打包環境，搜尋 _MEIPASS 目錄
    if getattr(sys, 'frozen', False):
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        for root, _, files in os.walk(base_dir):
            for f in files:
                if f.lower().startswith("ffmpeg") and f.lower().endswith(".exe"):
                    return os.path.join(root, f)

    # 3. 搜尋執行檔所在目錄
    exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(exe_dir, "ffmpeg.exe")
    if os.path.isfile(candidate):
        return candidate

    return "ffmpeg"

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
except ImportError:
    TkinterDnD = None
    DND_FILES = None

if TkinterDnD:
    class CTk_DnD(ctk.CTk, TkinterDnD.DnDWrapper):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.TkdndVersion = TkinterDnD._require(self)
else:
    class CTk_DnD(ctk.CTk):
        pass

DISCLAIMER_TEXT = """================================================================================
  AudioConverter 音檔轉檔與壓縮大師 - 軟體使用條款與免責聲明協議
  AudioConverter - End User License Agreement & Terms of Disclaimer
  作者 / Author: HCL (https://github.com/HCL0831/AudioConverter)
  版權所有 / Copyright (c) 2026 HCL. All rights reserved.
================================================================================

【繁體中文版 / Traditional Chinese Version】

歡迎使用 AudioConverter 音檔轉檔與壓縮大師（以下簡稱「本軟體」）。本軟體由作者 HCL 開發並免費提供公眾使用。在下載、安裝、執行或使用本軟體前，請詳細閱讀本協議所有條款。當您勾選「我同意」或開始使用本軟體時，即表示您已完整閱讀、理解並無條件同意接受本協議所有條款之約束：

一、軟體授權與現狀交付聲明 (License Grant & "AS IS" Provision)
1. 本軟體為免費軟體（Freeware），作者授予您個人或非商業用途之免費使用權利。
2. 本軟體按「現狀 (AS IS)」及「現有技術水準」提供，不附帶任何形式之明示、默示、法定或擔保責任。
3. 作者明確聲明不提供任何包括但不限於：適銷性、特定用途適用性、無錯誤、無中斷運作、無漏洞或不侵權之保證。

二、完全免責條款與責任限制 (Limitation of Liability)
1. 在適用法律允許的最大範圍內，作者 HCL 在任何情況下均不對使用者或任何第三方因下載、安裝、使用、誤用、無法使用本軟體或依賴本軟體輸出結果所導致之任何形式的直接、間接、附隨、特別、懲罰性或衍生性損害負擔任何法律、合約、侵權或其他形式之賠償責任。
2. 前述免除之損害範圍包括但不限於：影音原始檔案損壞或遺失、資料覆蓋錯誤、轉檔品質瑕疵、系統當機、硬體毀損、業務中斷、利潤損失、商譽受損或第三方索賠。
3. 使用本軟體所產生之所有風險與後果，均由使用者自行全權承擔。

三、使用者資料備份義務 (User Responsibility & Backup Duty)
1. 影音轉檔、編碼壓縮與時間分割屬於磁碟大量讀寫與資料運算行為。使用者有義務在進行任何影音處理前，自行完整備份所有重要的原始檔案。
2. 雖然本軟體預設將產出成果儲存於「output」子資料夾以避免覆蓋原檔，但作者不保證在任何異常中斷、硬碟空間不足或系統錯誤下檔案絕對安全。

四、智慧財產權與合法使用保證 (Intellectual Property & Lawful Use)
1. 本軟體僅供使用者處理擁有合法著作權或已取得權利人合法授權之影音內容。
2. 使用者嚴禁利用本軟體從事任何侵害他人著作權、商標權、營業秘密、隱私權或違反任何國家/地區法令規章之行為。
3. 因使用者不當或非法使用本軟體所引發之任何民事侵權賠償、刑事責任或行政罰鍰，概由使用者獨立承擔所有法律責任，與本軟體作者 HCL 無涉。

五、第三方開源組件聲明 (Third-Party Open Source Components)
1. 本軟體內部調用開源工具 FFmpeg 及相關 Python 第三方函式庫。相關組件之智慧財產權與授權分別歸屬於其原專案擁有者（包括但不限於 LGPL/GPL/MIT/Apache 等授權條款）。

六、條款修改、可分割性與準據法 (Modification & Governing Law)
1. 作者保留隨時修改本條款之權利。
2. 若本協議之任何條款被管轄法院判定為無效或無法執行，其餘條款之效力仍不受任何影響。

--------------------------------------------------------------------------------
【English Version / 英文版條款】

PLEASE READ THIS END USER LICENSE AGREEMENT AND DISCLAIMER ("AGREEMENT") CAREFULLY BEFORE USING AUDIOCONVERTER (THE "SOFTWARE"). BY ACCESSING, RUNNING, OR USING THE SOFTWARE, YOU ACKNOWLEDGE THAT YOU HAVE READ, UNDERSTOOD, AND AGREE TO BE BOUND BY ALL TERMS AND CONDITIONS OF THIS AGREEMENT. IF YOU DO NOT AGREE, PLEASE EXIT AND CEASE ALL USE IMMEDIATELY.

1. LICENSE GRANT & "AS IS" PROVISION
The Software is provided by the author, HCL, as freeware. The Software is provided on an "AS IS" and "AS AVAILABLE" basis, without warranty of any kind, whether express, implied, statutory, or otherwise, including but not limited to the warranties of merchantability, fitness for a particular purpose, title, and non-infringement.

2. LIMITATION OF LIABILITY
TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, IN NO EVENT SHALL THE AUTHOR (HCL) BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, LOSS OF DATA, CORRUPTION OF AUDIO/VIDEO FILES, HARDWARE DAMAGE, SYSTEM CRASHES, BUSINESS INTERRUPTION, OR LOSS OF PROFITS) ARISING OUT OF OR IN CONNECTION WITH THE USE OR INABILITY TO USE THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. YOU ASSUME FULL RESPONSIBILITY FOR ANY RISKS ARISING FROM USING THE SOFTWARE.

3. USER BACKUP OBLIGATION
Audio conversion, compression, and segmenting involve intensive file input/output operations. Users have the sole duty and obligation to perform full and independent backups of all original media files prior to performing any operation with this Software.

4. LAWFUL USE & COPYRIGHT COMPLIANCE
You warrant and represent that you have all necessary rights, titles, licenses, and permissions for any audio, video, or media files processed through this Software. You agree not to use the Software for any unlawful purposes or in any manner that infringes upon the intellectual property or proprietary rights of any third party. The user agrees to indemnify and hold harmless the author (HCL) from any claims or liabilities arising from the user's illegal or infringing use of the Software.

5. THIRD-PARTY LICENSES
This Software integrates and interfaces with third-party open-source components, including FFmpeg (https://ffmpeg.org/) and related Python libraries, subject to their respective open-source licenses.

6. GENERAL & GOVERNING TERMS
The author reserves the right to revise or update this Agreement at any time. If any provision of this Agreement is held invalid, the remainder shall continue in full force and effect.
================================================================================
"""

# Set appearance mode and color theme
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")  

class AudioToolApp(CTk_DnD):
    def __init__(self):
        super().__init__()

        self.geometry("750x620")
        self.resizable(False, False)
        self.center_window()

        self.ffmpeg_path = get_ffmpeg_path()

        self.mode_var = ctk.StringVar(value="compress")
        self.bitrate_var = ctk.StringVar(value="256k")
        self.format_var = ctk.StringVar(value="mp3")
        self.split_size_var = ctk.StringVar(value="190")
        self.recursive_var = ctk.BooleanVar(value=True)
        
        # 檢測使用者是否曾同意過本版本的免責聲明協議
        if is_disclaimer_agreed():
            self.title("音檔壓縮與轉換工具 - by HCL (支援拖曳目錄)")
            self.create_widgets()
        else:
            self.title("使用條款與免責聲明 - AudioConverter (by HCL)")
            self.show_disclaimer_view()

    def center_window(self):
        self.update_idletasks()
        w = 750
        h = 620
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def show_disclaimer_view(self):
        self.disclaimer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.disclaimer_frame.pack(fill="both", expand=True, padx=25, pady=20)

        lbl_title = ctk.CTkLabel(self.disclaimer_frame, text="⚖️ 軟體使用條款與免責聲明協議", font=("Arial", 20, "bold"), text_color="#10b981")
        lbl_title.pack(pady=(5, 5))

        lbl_sub = ctk.CTkLabel(self.disclaimer_frame, text="歡迎使用！首次啟動請詳細閱讀以下條款，勾選並同意後即可開始使用軟體：", font=("Arial", 13))
        lbl_sub.pack(pady=(0, 10))

        # 條款內容框
        self.disclaimer_box = ctk.CTkTextbox(self.disclaimer_frame, width=700, height=360, font=("Arial", 13))
        self.disclaimer_box.pack(pady=5, fill="x")
        self.disclaimer_box.insert("1.0", DISCLAIMER_TEXT)
        self.disclaimer_box.configure(state="disabled")

        # 勾選框
        self.agree_var = ctk.BooleanVar(value=False)
        self.chk_agree = ctk.CTkCheckBox(self.disclaimer_frame, text="我已詳細閱讀、理解並完全同意上述免責聲明與使用條款 (僅需同意一次)", variable=self.agree_var, command=self.on_checkbox_toggle, font=("Arial", 13, "bold"))
        self.chk_agree.pack(pady=12)

        # 按鈕區
        btn_frame = ctk.CTkFrame(self.disclaimer_frame, fg_color="transparent")
        btn_frame.pack(pady=(5, 10))

        self.btn_exit = ctk.CTkButton(btn_frame, text="❌ 不同意並退出", command=self.destroy, width=150, height=38, fg_color="#ef4444", hover_color="#dc2626", font=("Arial", 14, "bold"))
        self.btn_exit.pack(side="left", padx=20)

        self.btn_accept = ctk.CTkButton(btn_frame, text="✅ 我同意並接受", command=self.accept_and_start, width=170, height=38, fg_color="#10b981", hover_color="#059669", font=("Arial", 14, "bold"), state="disabled")
        self.btn_accept.pack(side="left", padx=20)

    def on_checkbox_toggle(self):
        if self.agree_var.get():
            self.btn_accept.configure(state="normal")
        else:
            self.btn_accept.configure(state="disabled")

    def accept_and_start(self):
        save_disclaimer_agreement()
        self.disclaimer_frame.destroy()
        self.title("音檔壓縮與轉換工具 - by HCL (支援拖曳目錄)")
        self.create_widgets()

    def create_widgets(self):
        # 1. Source Directories Selection
        frame_source = ctk.CTkFrame(self)
        frame_source.pack(pady=10, padx=20, fill="x")

        lbl_source = ctk.CTkLabel(frame_source, text="來源資料夾/檔案清單 (可直接拖曳多個資料夾或檔案至下方框中):")
        lbl_source.pack(anchor="w", padx=10, pady=(10, 0))

        self.dir_textbox = ctk.CTkTextbox(frame_source, height=100)
        self.dir_textbox.pack(fill="x", padx=10, pady=5)
        self.dir_textbox.configure(state="normal") 
        
        if TkinterDnD:
            self.dir_textbox.drop_target_register(DND_FILES)
            self.dir_textbox.dnd_bind('<<Drop>>', self.on_drop)
        else:
            self.dir_textbox.insert("1.0", "缺少 tkinterdnd2，無法使用拖曳功能。請確認已安裝。\n")

        btn_frame = ctk.CTkFrame(frame_source, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.chk_recursive = ctk.CTkCheckBox(btn_frame, text="包含所有子資料夾 (遞迴深度搜尋)", variable=self.recursive_var, font=("Arial", 12, "bold"))
        self.chk_recursive.pack(side="left", padx=5)

        ctk.CTkButton(btn_frame, text="清空清單", command=self.clear_source_dirs, width=90, fg_color="#ef4444", hover_color="#dc2626").pack(side="right", padx=5)
        ctk.CTkButton(btn_frame, text="透過視窗加入...", command=self.add_source_dir, width=120).pack(side="right", padx=5)

        # 2. Mode Selection
        frame_mode = ctk.CTkFrame(self)
        frame_mode.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(frame_mode, text="選擇功能:").pack(side="left", padx=10)
        
        ctk.CTkRadioButton(frame_mode, text="壓縮音檔", variable=self.mode_var, value="compress", command=self.update_options).pack(side="left", padx=10)
        ctk.CTkRadioButton(frame_mode, text="影片轉音檔", variable=self.mode_var, value="convert", command=self.update_options).pack(side="left", padx=10)
        ctk.CTkRadioButton(frame_mode, text="分割檔案 (依大小)", variable=self.mode_var, value="split", command=self.update_options).pack(side="left", padx=10)

        # 3. Options Frame
        self.frame_options = ctk.CTkFrame(self)
        self.frame_options.pack(pady=10, padx=20, fill="x")
        
        self.format_label = ctk.CTkLabel(self.frame_options, text="輸出格式:")
        self.format_label.pack(side="left", padx=5, pady=10)
        self.format_dropdown = ctk.CTkComboBox(self.frame_options, values=["mp3", "aac", "wav", "flac", "m4a"], variable=self.format_var, width=80)
        self.format_dropdown.pack(side="left", padx=5, pady=10)

        self.bitrate_label = ctk.CTkLabel(self.frame_options, text="位元率:")
        self.bitrate_label.pack(side="left", padx=5, pady=10)
        self.bitrate_dropdown = ctk.CTkComboBox(self.frame_options, values=["64k", "96k", "128k", "192k", "256k", "320k"], variable=self.bitrate_var, width=80)
        self.bitrate_dropdown.pack(side="left", padx=5, pady=10)

        self.split_label = ctk.CTkLabel(self.frame_options, text="分割大小 (MB):")
        self.split_entry = ctk.CTkEntry(self.frame_options, textvariable=self.split_size_var, width=60)
        
        # 4. Status and Progress
        self.status_label = ctk.CTkLabel(self, text="準備就緒 (處理後的檔案會自動存放於各自資料夾內的 output 資料夾中)")
        self.status_label.pack(pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(self, width=710)
        self.progress_bar.pack(pady=5)
        self.progress_bar.set(0)

        # 5. Action Button (開始批次處理按鈕)
        self.action_button = ctk.CTkButton(self, text="開始批次處理", command=self.start_processing, height=44, font=("Arial", 16, "bold"), fg_color="#059669", hover_color="#047857")
        self.action_button.pack(pady=(15, 10))

        # 6. Author Footer & Disclaimer
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(side="bottom", fill="x", pady=(0, 5), padx=20)

        lbl_author = ctk.CTkLabel(footer_frame, text="AudioConverter v2.0 | Developed by HCL | GitHub: @HCL0831", font=("Arial", 11), text_color="gray")
        lbl_author.pack(side="left")

        btn_disc = ctk.CTkButton(footer_frame, text="📜 免責聲明", command=self.show_disclaimer, width=80, height=22, font=("Arial", 11), fg_color="transparent", text_color="#1f538d", hover_color="#d0d0d0")
        btn_disc.pack(side="right")
        
        self.update_options()

    def show_disclaimer(self):
        top = ctk.CTkToplevel(self)
        top.title("使用條款與免責聲明 (Terms of Service & Disclaimer)")
        top.geometry("650x520")
        top.attributes("-topmost", True)
        top.grab_set()

        lbl = ctk.CTkLabel(top, text="⚖️ 軟體使用條款與免責聲明 (中英雙語完整版)", font=("Arial", 16, "bold"), text_color="#10b981")
        lbl.pack(pady=(12, 6))

        tb = ctk.CTkTextbox(top, width=600, height=400, font=("Arial", 12))
        tb.pack(padx=15, pady=5, fill="both", expand=True)
        tb.insert("1.0", DISCLAIMER_TEXT)
        tb.configure(state="disabled")

        btn = ctk.CTkButton(top, text="關閉 (Close)", command=lambda: [top.grab_release(), top.destroy()], width=120, fg_color="#10b981", hover_color="#059669")
        btn.pack(pady=10)

    def update_options(self):
        mode = self.mode_var.get()
        if mode in ["compress", "convert"]:
            self.split_label.pack_forget()
            self.split_entry.pack_forget()
        elif mode == "split":
            self.split_label.pack(side="left", padx=5, pady=10)
            self.split_entry.pack(side="left", padx=5, pady=10)
            
    def on_drop(self, event):
        data = event.data
        if '{' in data:
            paths = re.findall(r'\{([^}]+)\}', data)
            remaining = re.sub(r'\{([^}]+)\}', '', data).strip().split()
            paths.extend(remaining)
        else:
            paths = data.split()
            
        for path in paths:
            if os.path.exists(path):
                current_text = self.dir_textbox.get("1.0", "end-1c").strip()
                dirs = [d.strip() for d in current_text.split('\n') if d.strip()]
                if path not in dirs:
                    if current_text:
                        self.dir_textbox.insert("end", "\n" + path)
                    else:
                        self.dir_textbox.insert("end", path)

    def add_source_dir(self):
        directory = filedialog.askdirectory(title="選擇來源資料夾")
        if directory:
            current_text = self.dir_textbox.get("1.0", "end-1c").strip()
            dirs = [d.strip() for d in current_text.split('\n') if d.strip()]
            if directory not in dirs:
                if current_text:
                    self.dir_textbox.insert("end", "\n" + directory)
                else:
                    self.dir_textbox.insert("end", directory)

    def clear_source_dirs(self):
        self.dir_textbox.delete("1.0", "end")

    def start_processing(self):
        current_text = self.dir_textbox.get("1.0", "end-1c").strip()
        source_dirs = [d.strip() for d in current_text.split('\n') if d.strip()]

        if not source_dirs:
            messagebox.showerror("錯誤", "請至少加入一個來源資料夾或檔案！(可直接貼上或拖曳路徑)")
            return

        supported_exts = {".mp3", ".wav", ".flac", ".m4a", ".mp4", ".avi", ".mkv", ".ogg", ".wma", ".aac", ".mov"}
        files_to_process = []
        is_recursive = self.recursive_var.get()
        
        for item_path in source_dirs:
            if os.path.isdir(item_path):
                if is_recursive:
                    for root, dirs, files in os.walk(item_path):
                        # 排除 output 資料夾與隱藏資料夾，避免重複遞迴
                        dirs[:] = [d for d in dirs if d.lower() != 'output' and not d.startswith('.')]
                        for f in files:
                            ext = os.path.splitext(f)[1].lower()
                            if ext in supported_exts:
                                files_to_process.append(os.path.join(root, f))
                else:
                    for f in os.listdir(item_path):
                        full_p = os.path.join(item_path, f)
                        if os.path.isfile(full_p):
                            ext = os.path.splitext(f)[1].lower()
                            if ext in supported_exts:
                                files_to_process.append(full_p)
            elif os.path.isfile(item_path):
                ext = os.path.splitext(item_path)[1].lower()
                if ext in supported_exts:
                    files_to_process.append(item_path)
            else:
                messagebox.showwarning("警告", f"找不到指定之路徑: {item_path}")

        if not files_to_process:
            messagebox.showinfo("提示", "在所選的目錄與子資料夾中，沒有找到支援的影音檔案。")
            return

        self.action_button.configure(state="disabled", text="處理中...")
        self.progress_bar.set(0)
        
        threading.Thread(target=self.process_all_files, args=(files_to_process,), daemon=True).start()

    def process_all_files(self, files_list):
        total_files = len(files_list)
        success_count = 0
        error_count = 0

        for idx, file_path in enumerate(files_list):
            filename = os.path.basename(file_path)
            self.update_status(f"處理中 ({idx+1}/{total_files}): {filename}", (idx / total_files))
            
            source_dir = os.path.dirname(file_path)
            output_dir = os.path.join(source_dir, "output")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            success = self.process_single_file(file_path, output_dir)
            if success:
                success_count += 1
            else:
                error_count += 1

        self.update_status(f"處理完成！成功: {success_count}，失敗: {error_count}", 1.0)
        self.after(0, self.on_processing_complete, success_count > 0, f"批次處理結束。\n總共找到 {total_files} 個檔案。\n成功處理了 {success_count} 個檔案。\n發生錯誤 {error_count} 個檔案。")

    def update_status(self, text, progress):
        self.after(0, self.status_label.configure, {"text": text})
        self.after(0, self.progress_bar.set, progress)

    def process_single_file(self, source, output_dir):
        mode = self.mode_var.get()
        fmt = self.format_var.get().lower()
        filename = os.path.basename(source)
        name, _ = os.path.splitext(filename)
        
        codec = "libmp3lame"
        if fmt == "aac" or fmt == "m4a": codec = "aac"
        elif fmt == "wav": codec = "pcm_s16le"
        elif fmt == "flac": codec = "flac"
            
        try:
            if mode == "compress" or mode == "convert":
                output_file = os.path.join(output_dir, f"{name}_output.{fmt}")
                bitrate = self.bitrate_var.get()
                
                cmd = [self.ffmpeg_path, "-y", "-i", source, "-vn", "-c:a", codec]
                if fmt not in ["wav", "flac"]: cmd.extend(["-b:a", bitrate])
                cmd.append(output_file)
                
                return self.run_ffmpeg(cmd)

            elif mode == "split":
                output_pattern = os.path.join(output_dir, f"{name}_part%03d.{fmt}")
                bitrate_str = self.bitrate_var.get()
                target_mb = float(self.split_size_var.get())
                
                bitrate_bps = 128000
                match = re.match(r"(\d+)k", bitrate_str)
                if match: bitrate_bps = int(match.group(1)) * 1000
                if fmt in ["wav", "flac"]: bitrate_bps = 1411000
                    
                target_bits = target_mb * 1024 * 1024 * 8
                segment_time_seconds = int(target_bits / bitrate_bps)
                if segment_time_seconds < 10: segment_time_seconds = 10

                cmd = [self.ffmpeg_path, "-y", "-i", source, "-vn", "-c:a", codec, "-f", "segment", "-segment_time", str(segment_time_seconds)]
                if fmt not in ["wav", "flac"]: cmd.extend(["-b:a", bitrate_str])
                cmd.append(output_pattern)
                
                return self.run_ffmpeg(cmd)
                
        except Exception:
            return False
        return False

    def run_ffmpeg(self, cmd):
        try:
            creationflags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=creationflags)
            process.communicate()
            return process.returncode == 0
        except FileNotFoundError:
            return False

    def on_processing_complete(self, any_success, message):
        self.action_button.configure(state="normal", text="開始批次處理")
        if any_success:
            self.status_label.configure(text_color="green")
            self.clear_source_dirs()  # 轉檔成功後自動清空來源清單路徑
            messagebox.showinfo("處理完成", message)
        else:
            self.status_label.configure(text_color="red")
            messagebox.showwarning("處理結果", message)

if __name__ == "__main__":
    app = AudioToolApp()
    app.mainloop()
