# 🎵 AudioConverter 音檔轉檔與壓縮大師

<div align="center">

![Author](https://img.shields.io/badge/Author-HCL-059669.svg?style=for-the-badge&logo=github&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6.svg?style=for-the-badge&logo=windows&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Embedded-007808.svg?style=for-the-badge&logo=ffmpeg&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Repository-181717.svg?style=for-the-badge&logo=github&logoColor=white)

**一套由 HCL 獨立開發製作的現代化影音轉檔、音訊壓縮與長音檔分割神器**

🔗 **GitHub 專案網址**：[https://github.com/HCL0831/AudioConverter](https://github.com/HCL0831/AudioConverter)

</div>

---

## 📑 目錄

- [專案簡介](#-專案簡介)
- [核心功能](#-核心功能)
- [支援格式](#-支援格式)
- [快速開始](#-快速開始)
  - [方法一：免安裝單機版 (推薦)](#方法一免安裝單機版-推薦)
  - [方法二：Python 原始碼執行](#方法二python-原始碼執行)
- [專案目錄結構](#-專案目錄結構)
- [手動打包為 EXE](#-手動打包為-exe)
- [詳細操作手冊](#-詳細操作手冊)
- [開源許可與聲明](#-開源許可與聲明)

---

## 💡 專案簡介

**AudioConverter (音檔轉檔與壓縮大師)** 專為大量影音檔案處理設計，旨在解決日常中遇到的音檔過大無法上傳、格式不相容、需要從影片擷取聲音，或是長語音檔超過 AI 語音辨識（如 OpenAI Whisper 25MB/200MB 限制）等問題。

本專案具備以下優勢：
- **免安裝單一執行檔**：已完整封裝 Python 直譯器與 FFmpeg 轉檔引擎，開箱即用。
- **現代化桌面 GUI**：採用 CustomTkinter 美觀深色/淺色主題，支援直接拖曳資料夾或檔案。
- **子目錄遞迴掃描**：支援自動深入所有子資料夾批次轉檔，並各自存放於 `output/` 目錄。
- **批次自動化**：支援同時處理多個資料夾，自動在各資料夾建立 `output/` 存放成果。

---

## ⚡ 核心功能

| 功能名稱 | 說明 | 適用場景 |
| :--- | :--- | :--- |
| **🗜️ 音檔壓縮 (Compress)** | 自由調整位元率（64k ~ 320k），在維持高音質下大幅降低檔案體積。 | 節省儲存空間、符合 Email/通訊軟體傳送大小。 |
| **🎬 影片轉音檔 (Extract)** | 高速從各類影片中抽取音軌，轉換為指定音訊格式。 | 擷取會議影片錄音、MV 轉 MP3、課程音檔抽取。 |
| **✂️ 檔案分割 (Split)** | 依指定目標大小（如 190MB、1GB）自動計算並將大檔案切割為多個小片段。 | 突破 AI 語音轉文字、雲端硬碟單檔上傳大小限制。 |

---

## 🎧 支援格式

- **輸入影音格式**：`.mp3`、`.wav`、`.flac`、`.m4a`、`.mp4`、`.avi`、`.mkv`、`.ogg`、`.wma`、`.aac`、`.mov` 等主流格式
- **輸出音訊格式**：
  - `MP3`（通用度最高，支援自訂位元率）
  - `AAC` / `M4A`（高效率壓縮格式）
  - `WAV`（無損未壓縮 PCM）
  - `FLAC`（無損壓縮格式）

---

## 🚀 快速開始

### 方法一：免安裝單機版 (推薦 ⭐)
1. 直接在 Windows 電腦上下載並雙擊 [`音檔轉檔與壓縮大師.exe`](音檔轉檔與壓縮大師.exe)。
2. **無需安裝 Python、無需安裝 FFmpeg、無需任何配置**即可立即開始轉檔。

---

### 方法二：Python 原始碼執行

#### 1. 環境需求
- Python 3.10 或以上版本
- Windows 作業系統

#### 2. 安裝套件
```bash
pip install -r requirements.txt
```

#### 3. 啟動方式
- 在終端機輸入：
  ```bash
  python main.py
  ```

---

## 📂 專案目錄結構

```text
AudioConverter/
├── main.py                # 桌面 GUI 主程式 (CustomTkinter + TkinterDnD)
├── build.py               # PyInstaller 自動打包核心腳本
├── requirements.txt       # Python 相依套件清單
├── version_info.txt       # Windows EXE 版權與版本中繼檔
├── 音檔轉檔與壓縮大師.exe  # 獨立免安裝執行檔
├── 免責聲明.md            # 中英雙語法律免責聲明與協議
├── LICENSE                # MIT 授權條款
└── 操作手冊.html          # 清新自然風格 視覺化大圖操作手冊
```

---

## 🛠️ 手動打包為 EXE

若您自行修改了原始碼，可使用內建的自動化打包工具重新編譯：

1. 在終端機執行：
   ```bash
   python build.py
   ```
2. 打包程式會自動在暫存目錄完成編譯，並將最新的 `音檔轉檔與壓縮大師.exe` 複製到專案根目錄。

---

## 📖 詳細操作手冊

如需各功能詳細步驟教學、參數設定建議與故障排除，請直接雙擊開啟：
- 🌐 **[視覺化大圖操作手冊 (操作手冊.html)](操作手冊.html)**（具備 Mermaid UML 操作流程圖、音質速查表與常見問題解答）

---

## ❓ 常見問題 (FAQ)

### Q1：為什麼雙擊 .exe 之後，需要等幾秒才會跳出視窗？
- **正常自解壓與安全分析**：本軟體為免安裝 Python/FFmpeg 的單一執行檔（約 60MB），首次或每次啟動時 Windows 會在背景自動解壓至暫存區並進行安全檢查。
- **加速小撇步**：若目前放置於網路磁碟（如 NAS/Samba 或 `T:` 槽），**建議複製至本機「桌面」或「C: 槽」執行**，速度可提升 2～3 倍！

### Q2：支援子資料夾與拖曳嗎？
- **支援！** 預設勾選「包含所有子資料夾 (遞迴深度搜尋)」，拖入包含多層子目錄的資料夾，軟體會自動全部抓取轉檔，並各自輸出至該子資料夾的 `output/` 目錄中。

---

## 👨‍💻 作者資訊 (Author)

- **開發者 (Developer)**: **HCL**
- **GitHub 專案庫**: [https://github.com/HCL0831/AudioConverter](https://github.com/HCL0831/AudioConverter)
- **個人主頁**: [https://github.com/HCL0831](https://github.com/HCL0831)

## ⚖️ 免責聲明 (Disclaimer)

> [!IMPORTANT]
> **使用前請注意：**
> 1. **現狀提供 (AS-IS)**：本軟體由作者 **HCL** 免費分享提供，不提供任何明示或默示的擔保。
> 2. **免除損害賠償責任**：作者不對因使用或無法使用本軟體導致之任何資料遺失、原始檔案損毀、硬體異常或商業損失承擔任何法律與賠償責任。
> 3. **使用者備份義務**：轉檔、壓縮與分割屬於磁碟讀寫運算，**使用者請務必於操作前自行備份重要影音原始檔案**。
> 4. **合法使用規範**：本工具僅供合法影音處理用途，使用者須確保所處理之檔案具備合法著作權或授權。
> 
> 詳細完整條款請參閱 👉 **[免責聲明與使用條款 (免責聲明.md)](免責聲明.md)**。

---

## 📄 開源許可 (License)

- 本專案採用 [MIT License](LICENSE) 授權。
- 底層音訊轉換技術基於 [FFmpeg](https://ffmpeg.org/)。
- Copyright (c) 2026 HCL. All rights reserved.
