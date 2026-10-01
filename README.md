# Pikmin Control Center

作者：Ody Liao。此公開庫提供正式簽章APK、更新索引與版本說明，不公開產品原始碼、簽章私鑰、私人GPS清單或裝置紀錄。

## 下載與更新

[下載最新版](https://github.com/odyliao-lab/pikmin-control-center-releases/releases/latest)。目前版本以Releases與`update.properties`為準，各版已驗／待驗範圍見Release說明，不表示所有功能全面穩定。

在控制中心「系統 → 版本更新」檢查、下載，再由Android確認安裝。自動檢查預設開啟，可自行關閉；不靜默安裝。同套件、同簽章的正常升級保留設定與紀錄，若簽章不符請勿直接移除安裝，先備份並核對來源。工作或停止清理未完成時會阻擋更新。

## 環境與核心

- APK最低Android9，主要裝置驗證為已root的Android14／arm64／Magisk／Zygisk。
- 遊戲相關功能目前只支援Pikmin Bloom **153.0**，不是任意遊戲版本。0.15.20配對統一核心**1.5.33/code101**，包含原生自動化及GPS Copy。
- APK內附配對核心；可在系統頁安裝，但仍需Root／Magisk權限、重開手機，開遊戲後核對同PID載入。只安裝APK不代表核心已更新或功能已驗收。
- GPS移動依賴獨立安裝並設定的相容GPS JoyStick；不包含第三方安裝檔。沿路採果先要求定位服務已啟動，結束不關閉JoyStick服務。
- 功能包括原生派遣／領取、育苗、批次／花田採果、餵食／收花瓣與實驗Health Connect步數工具。步數寫入成功不等同遊戲採計。

## 發布安全與隱私

更新只讀公開索引、下載GitHub資產；App不向此倉庫上傳遊戲帳號、座標或裝置紀錄，GitHub仍接收一般連線資訊（例如IP）。

APK簽章憑證SHA-256：

`9080c5d8c9a138a3a8eb42ec65755cf2abd64b881a7bf398feabe3547b934a7e`

版本依`versionCode`遞增，不自動降版、不替換同版APK。新版使用不可變更Release，附件含APK雜湊、版本說明及`build-provenance.json`（來源提交／依賴／CI識別，不含原始碼或金鑰）。更新索引經PR及`release-index`檢查通過才合併，檢查匿名下載雜湊、簽章與版本遞增。此庫僅保留必要的無機密發布驗證腳本／workflow。

非官方fan-made工具。Root、模擬定位、自動化或人工健康資料可能違反相關服務條款，請自行評估帳號與裝置風險。角色與商標屬各權利人，介面AI插圖不表示官方隸屬或角色權利。
