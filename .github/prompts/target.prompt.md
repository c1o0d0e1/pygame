---
mode: agent
tools:
  [
    "codebase",
    "editFiles",
    "fetch",
    "problems",
    "runCommands",
    "search",
    "searchResults",
    "terminalLastCommand",
    "terminalSelection",
    "usages",
  ]
---

# 開發步驟

- 遵守開發規範
- 新增一個遊戲名為 `Galaxy lancer` 的遊戲在 `Galaxy Lancer\class1\prj01.py` 裡，並以 pygame 實作
- 將背景設為黑色，並使用 `Galaxy Lancer\image\space.png` 當作背景圖片，且以往上轉動的方式顯示(FPS 60)
- 執行時將一直以往上轉動的方式顯示背景圖片，直到(X)鍵被按下
