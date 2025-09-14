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
- 在`Galaxy Lancer\class3\prj03.py`寫入下程式碼:
- 載入`Galaxy Lancer\image\enemy1.png`和`Galaxy Lancer\image\enemy2.png`圖片(都要建立物件)
- 會每隔 60 像素產生一個敵人(enemy1.png 或 enemy2.png)(隨機定位 x 座標)
- 敵人會從畫面頂端往下移動
- 敵人移動速度為每秒 20 像素
- 當 Bullet 物件碰到敵人時,或移動到畫面底端時,敵人會消失並重新從頂端出現(無限循環和隨機定位 x 座標)
