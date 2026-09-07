# Pikmin Control Center

作者：Ody Liao。此公開庫僅提供 Control Center 的簽章 APK、版本資訊與更新說明；不包含私人原始碼、簽章私鑰、GPS 清單或裝置紀錄。

## 下載與更新

[下載最新版 APK](https://github.com/odyliao-lab/pikmin-control-center-releases/releases/latest)

0.8.0 起：「系統 → 版本更新」可檢查、下載並交由 Android 確認安裝。自動檢查預設開啟，可自行關閉；開啟 App 時最多每日一次，不會自動下載或靜默安裝。旧版本請先從 Releases 手動下載並覆蓋安裝一次。

同套件、同簽章的正常升級會保留設定和紀錄。若出現簽章不符，請勿直接解除安裝，先備份並確認來源。批次／花田工作及停止清理未完成時，不允許安裝更新。

## 適用範圍

- Android 9 以上；目前主要驗證環境為已 root 的 Android 14。
- 遊戲相關功能需要相容的 Pikmin Bloom v152、Magisk／Zygisk 與獨立 native module（目前搭配 1.4.22）。安裝本 APK 不會自動安裝或升級上述環境。
- 支援精華、附近派遣、返程領取、育苗、批次探險與花田採果控制；GPS 飛行仍需另行設定相容的 GPS JoyStick。
- APK 仍含既有 GPS Copy 相容資產，但本更新機制只更新 Control Center，不安裝／啟停 Magisk module；並非任意 Android／遊戲版本都已驗證。

## 隱私與驗證

檢查更新只讀取本庫公開版本資料；下載只存取 GitHub 發布資產。App 不上傳遊戲帳號、座標、裝置識別碼或操作紀錄。GitHub 作為連線服務仍會接收一般網路請求資訊，例如 IP 位址。

每個版本提供 SHA-256 檔案校驗值。APK 簽章憑證 SHA-256：

`9080c5d8c9a138a3a8eb42ec65755cf2abd64b881a7bf398feabe3547b934a7e`

版本依 `versionCode` 遞增判斷，不以版本文字排序；不提供自動降版。同一發布版本不替換 APK，修正另發新版。

非官方 fan-made 工具，與遊戲權利人無隸屬關係。介面插圖為 AI 生成的同人裝飾，角色及相關商標屬各自權利人；不宣稱擁有角色權利。使用輔助工具可能違反遊戲服務條款，請自行評估使用風險。
