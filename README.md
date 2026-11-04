# 研究生生存指南

一份給研究所新生的「實驗室迷因小報」：用米白報紙、紅黑大字與便利貼，把讀論文、課堂報告與每週規劃整理成能執行的小步驟。標題輕鬆吐槽日常，內文維持實用與友善。內容為一般學習建議與明確標示的假設案例，並非作者親身經驗或校方規定。

本專案的核心不是一次性網頁，而是讓 AI 依照 [AGENTS.md](AGENTS.md) 持續新增風格一致、格式固定的指南。純 HTML / CSS，不需要 npm、建置工具、API 金鑰或後端。

## 本機瀏覽與檢查

直接用瀏覽器開啟 `index.html` 即可。也可以在專案資料夾執行：

```sh
python -m http.server 8000 --bind 127.0.0.1
```

開啟 <http://127.0.0.1:8000>，結束時按 Ctrl+C。Python 只用於選用的本機伺服器與檢查，不是網站的執行需求。

修改後執行：

```sh
python checks.py
```

檢查使用 Python 3.9 以上版本的標準函式庫，涵蓋頁面標題、單一主標題、文章五段格式、首頁入口、相對連結與錨點。它不是完整 HTML 或無障礙驗證器；請另用瀏覽器確認手機寬度、桌機版面與鍵盤 Tab 導覽。專案初始無套件管理器或 CI；無需安裝測試框架。

## 讓 AI 新增下一篇

可將這段交給 AI：

> 請先閱讀 AGENTS.md，再參考 guides/reading-papers.html，新增一篇「第一次和指導教授討論研究」。採用明確標示的假設情境，不虛構我的個人經驗；沿用共用樣式與五段文章格式，在首頁加入入口，最後執行 python checks.py 並回報結果。不要提交、推送或部署。

規則會告訴 AI 檔案放哪裡、文章寫什麼、如何沿用視覺、哪些事需要作者確認，以及如何驗證新增頁面。若新增文章後首頁仍有數量或順序文字，也要同步更新。

## 發布至 GitHub Pages

已部署至 <https://forggy0113.github.io/grad-survival-guide/>，發布來源為 `main` 分支的根目錄。已實際檢查公開首頁與三篇指南、手機與桌機寬度及文章往返導覽。以下保留發布流程，供日後重建或更新使用。

1. 在 GitHub 建立公開 Repository，例如 `grad-survival-guide`。上傳本資料夾的專案檔案，確保 `index.html` 位於 Repository 根目錄；不要上傳個資、密鑰或不屬於專案的課堂資料。`.nojekyll` 是用來略過 Jekyll 的空檔案，使用 Git 上傳時一併保留。
2. 前往 Repository 的 **Settings → Pages → Build and deployment**，將 Source 設為 **Deploy from a branch**，選擇實際存放檔案的分支（通常為 `main`）及 **/(root)**，按 Save。
3. 等待 GitHub 的部署作業完成，使用 Pages 顯示的網址實際打開首頁與三篇文章。典型網址為 `https://你的帳號.github.io/grad-survival-guide/`，以設定頁顯示的真實網址為準。
4. 將真實 Repository 與網站連結補入下方繳交文字；確認公開網址不用登入也能瀏覽。後續更新同一分支即可觸發重新部署。

操作參考：[GitHub 官方發布來源設定](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。網站採相對路徑，可部署在 Repository 子路徑，不需要自訂網域或 Actions 設定檔。
