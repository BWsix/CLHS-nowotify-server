# CLHS nowotify - server

使用 Discord / Line 及時接收壢中官網公告

**前往[設定頁面][clhs_nowotify]**  
**前往[CLHS nowotify - client][repo_client]**

## 目錄

- [運作原理](#theory)
- [特色](#features)
- [安裝教學](#tutorial)
- [特別感謝](#credit)

## 運作原理<a id="theory"></a>

CLHS nowotify 使用 python 伺服器監聽壢中官網  
在發現公告內容有更新時，使用 `discord webhook` / `line notify` 將最新公告推送給用戶

因為經費有限，伺服器只在每日早上 7 點到晚上 7 點運作 (歡迎贊助 👍)

### 架構圖

> ![](https://i.imgur.com/dPgNcP8.png)  
> **client** : react app deployed on Github pages  
> **server** : python server hosted on Heroku

## 特色<a id="features"></a>

### 快速、簡單的安裝

可以在[設定頁面][clhs_nowotify]依照教學登錄資訊(discord / line)後啟用

> 因為 line notify 只能從電腦版網站做設定，如果要使用 line 接收通知請記得使用電腦安裝

### 客製化設定

目前可以設定的項目有 :

- 公告的來源(首頁 / 新生專區)
- 只接收釘選公告(有紅色 `HOT!` 標籤的)
- 是否過濾特定公告(有關公務人員 / 標案等)

## 安裝教學<a id="tutorial"></a>

關於安裝教學可以在設定頁面看到，或是在[這裡][repo_client]查看

## 特別感謝<a id="credit"></a>

[@storiesbang][@storiesbang]: 系統測試和提供更新方向

以及所有 CLHS nowotify 的用戶，謝謝你們的支持

[clhs_nowotify]: https://bwsix.github.io/CLHS-nowotify/
[repo_client]: https://github.com/BWsix/CLHS-nowotify
[@storiesbang]: https://github.com/storiesbang
