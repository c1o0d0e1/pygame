###################### 載入套件 ######################
import pygame  # 匯入pygame模組
import sys  # 匯入系統模組
import os  # 匯入os模組，方便處理路徑

###################### 初始化設定 ######################
pygame.init()  # 初始化pygame
FPS = pygame.time.Clock()  # 設定FPS物件，控制遊戲更新速度


###################### 背景圖片載入與視窗設定 ######################
# 取得背景圖片的正確路徑，避免路徑錯誤
bg_img_path = os.path.join("Galaxy Lancer", "image", "space.png")
bg_img_raw = pygame.image.load(bg_img_path)  # 先載入圖片，不用 .convert()
# 以背景圖片的尺寸作為視窗大小
WIN_WIDTH = bg_img_raw.get_width()  # 取得背景圖片寬度
WIN_HEIGHT = bg_img_raw.get_height()  # 取得背景圖片高度
pygame.display.set_caption("Galaxy lancer")  # 設定視窗標題
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # 建立視窗
# 設定好視窗後再 .convert()，避免 pygame.error
bg_img = bg_img_raw.convert()


###################### 主程式 ######################
# ----------------------
# Player (playar) 物件
# ----------------------
class Player:
    """
    playar 玩家物件：
    - 載入三張圖片 (中、左、右)
    - 支援按鍵持續移動 (上下左右)
    - 左/右鍵按下時切換圖片
    - 在視窗邊界停住 (不超出視窗)
    """

    def __init__(self, x, y, speed=5):
        # 載入圖片並設定初始位置
        img_mid_path = os.path.join("Galaxy Lancer", "image", "fighter_M.png")
        img_left_path = os.path.join("Galaxy Lancer", "image", "fighter_L.png")
        img_right_path = os.path.join("Galaxy Lancer", "image", "fighter_R.png")
        # 使用 convert_alpha 保留透明度
        self.img_mid = pygame.image.load(img_mid_path).convert_alpha()
        self.img_left = pygame.image.load(img_left_path).convert_alpha()
        self.img_right = pygame.image.load(img_right_path).convert_alpha()
        self.image = self.img_mid

        self.x = x
        self.y = y
        self.speed = speed

        # 鍵盤狀態
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        # 設定寬高屬性（取代 @property）
        self._update_size()

        # 燃燒器（burner）相關屬性（放在 __init__ 裡）
        burner_path = os.path.join("Galaxy Lancer", "image", "starship_burner.png")
        # 載入燃燒器圖片（保留透明度）
        self.burner_image = pygame.image.load(burner_path).convert_alpha()
        # 燃燒器是否顯示（根據上下左右鍵狀態決定），預設隱藏
        self.show_burner = True  # 預設為 True，因為會在 update 時根據鍵盤狀態更新
        # 燃燒器動畫參數：基準偏移與動畫階段
        self._burner_base_offset_y = self.height  # 燃燒器放在 player 底部
        self._burner_anim_stage = 0
        # 動畫階段循環：上移10, 下移10, 回原位 (相對基準)
        self._burner_anim_offsets = [-10, -5, 0, 5, 10]

    # 使用明確屬性儲存寬高，符合專案中其他類別寫法風格
    # 在初始化與每次切換圖片時更新這兩個屬性
    def _update_size(self):
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, win_width, win_height):
        # 根據鍵盤狀態更新位置
        if self.moving_up:
            self.y -= self.speed
        if self.moving_down:
            self.y += self.speed
        if self.moving_left:
            self.x -= self.speed
        if self.moving_right:
            self.x += self.speed

        # 邊界限制：停在視窗邊界前（不超出）
        if self.x < 0:
            self.x = 0
        if self.x + self.width > win_width:
            self.x = win_width - self.width
        if self.y < 0:
            self.y = 0
        if self.y + self.height > win_height:
            self.y = win_height - self.height

        # 更新燃燒器顯示條件：當按下上、左、右任一鍵（但不是僅按下下鍵）
        # show_burner 在每次 update 時重新計算，確保與鍵盤狀態同步
        self.show_burner = (
            self.moving_up
            or self.moving_left
            or self.moving_right
            or not (self.moving_up or self.moving_left or self.moving_right)
        ) and not self.moving_down

        # 更新燃燒器動畫：不論是否正在顯示，都持續推進動畫階段，
        # 這樣即使 player 停著不動（或瞬間不位移），動畫仍會執行
        self._burner_anim_stage = (self._burner_anim_stage + 1) % len(
            self._burner_anim_offsets
        )

    def draw(self, surface):
        # 若需要顯示燃燒器，將其繪製在 player 下方並根據動畫偏移
        if self.show_burner:
            # 取得目前動畫偏移
            anim_offset = self._burner_anim_offsets[self._burner_anim_stage]
            # 燃燒器顯示位置：x 與 player 對齊 (置中)，y 在 player 底部再加上基準與動畫偏移
            burner_x = int(self.x + (self.width - self.burner_image.get_width()) / 2)
            burner_y = int(self.y + self._burner_base_offset_y + anim_offset)
            surface.blit(self.burner_image, (burner_x, burner_y))
        # 先繪製飛機本體
        surface.blit(self.image, (int(self.x), int(self.y)))


# ----------------------
# Bullet 物件
# ----------------------
class Bullet:
    """
    Bullet 子彈物件：
    - 載入單一子彈圖片 (bullet.png)
    - 由玩家位置產生，x,y 為子彈左上角座標
    - 每次更新向上移動固定像素 (dy=10)
    - 當超出視窗上方時，回傳 False 表示可從管理清單移除
    """

    # 以 class-level 儲存圖片，避免每次產生都重複載入
    _image = None

    def __init__(self, x, y, dy=10):
        # 延後載入圖片，第一次建立子彈時載入一次
        if Bullet._image is None:
            img_path = os.path.join("Galaxy Lancer", "image", "bullet.png")
            Bullet._image = pygame.image.load(img_path).convert_alpha()
        self.image = Bullet._image
        self.x = x
        self.y = y
        self.dy = dy
        # 儲存寬高以便碰撞或邊界判斷
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        # 向上移動 (y 減少)
        self.y -= self.dy

    def draw(self, surface):
        # 將子彈繪製在指定座標（通常為整數座標）
        surface.blit(self.image, (int(self.x), int(self.y)))


# 背景初始y座標(從底部開始)
bg_y1 = 0
bg_y2 = -WIN_HEIGHT
running = True
# 建立 playar 物件，初始位置放在視窗中央偏下
playar = Player(WIN_WIDTH // 2, WIN_HEIGHT - 120, speed=6)
# 子彈管理清單：存放目前畫面上的 Bullet 物件
# 子彈管理清單，儲存目前所有在畫面內的子彈物件
bullets = []
import random


# ----------------------
# Enemy 物件
# ----------------------
class Enemy:
    """
    敵人物件：
    - 使用外部兩張圖 `enemy1.png` 與 `enemy2.png` (class-level快取)
    - 由畫面頂端往下移動，速度為每秒 50 像素（整個程式以 60 FPS 更新）
    - 當被 Bullet 擊中或到底部時，回到頂端並隨機 x 座標重生
    """

    _images = []

    def __init__(self, x, y, speed_per_sec=50):
        # 延遲載入圖片；只載入一次
        if not Enemy._images:
            p1 = os.path.join("Galaxy Lancer", "image", "enemy1.png")
            p2 = os.path.join("Galaxy Lancer", "image", "enemy2.png")
            Enemy._images = [
                pygame.image.load(p1).convert_alpha(),
                pygame.image.load(p2).convert_alpha(),
            ]
        # 隨機選一張圖片作為該敵人外觀
        self.image = random.choice(Enemy._images)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x
        self.y = y
        # 每次 update 的像素移動量（依 FPS 換算）
        # speed_per_sec 是每秒的像素，遊戲以 60 FPS 更新，故每次更新移動 speed_per_sec/60
        self.dy = speed_per_sec / 60.0

    def update(self):
        self.y += self.dy

    def draw(self, surface):
        surface.blit(self.image, (int(self.x), int(self.y)))

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)


# 建立敵人列表：每隔 60 像素產生一個敵人（在垂直方向的間隔）
# 這裡將依照畫面高度每 60 像素放一個敵人，初始 y 可以從 -height 到 0 分散
enemies = []
# 每隔 60 像素產生一個敵人，速度每秒 50 像素
spacing = 60
for start_y in range(0, WIN_HEIGHT, spacing):
    ex = random.randint(0, max(0, WIN_WIDTH - 40))
    ey = start_y - random.randint(0, WIN_HEIGHT // 2)
    enemies.append(Enemy(ex, ey, speed_per_sec=50))
while running:
    FPS.tick(60)  # 每秒最多更新60次
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # 按下(X)鍵結束遊戲
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                running = False
            # 空白鍵發射子彈：子彈初始座標以玩家中心上方為準
            if event.key == pygame.K_SPACE:
                # 空白鍵：產生一顆子彈。
                # 子彈 x 座標置中於玩家機身中間，y 座標從玩家前方開始（以玩家的 y 為基準）
                # 若圖片尚未載入（第一次按下），Bullet 會在建構函式中載入圖片，
                # 這裡先以 playar.x 作為暫時值，之後 Bullet 會以正確圖片寬度置中。
                if Bullet._image is not None:
                    bx = playar.x + playar.width // 2 - Bullet._image.get_width() // 2
                else:
                    bx = playar.x + playar.width // 2
                by = playar.y
                bullets.append(Bullet(bx, by, dy=10))
            # 處理玩家按鍵按下
            if event.key == pygame.K_UP:
                playar.moving_up = True
            if event.key == pygame.K_DOWN:
                playar.moving_down = True
            if event.key == pygame.K_LEFT:
                playar.moving_left = True
                # 切換到向左圖片
                playar.image = playar.img_left
                playar._update_size()
            if event.key == pygame.K_RIGHT:
                playar.moving_right = True
                # 切換到向右圖片
                playar.image = playar.img_right
                playar._update_size()
        # 處理玩家按鍵放開
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                playar.moving_up = False
            if event.key == pygame.K_DOWN:
                playar.moving_down = False
            if event.key == pygame.K_LEFT:
                playar.moving_left = False
                # 放開左鍵後，如果右鍵沒有按下，回到中立圖片
                if not playar.moving_right:
                    playar.image = playar.img_mid
                    playar._update_size()
            if event.key == pygame.K_RIGHT:
                playar.moving_right = False
                # 放開右鍵後，如果左鍵沒有按下，回到中立圖片
                if not playar.moving_left:
                    playar.image = playar.img_mid
                    playar._update_size()
    # 填滿黑色背景
    screen.fill((0, 0, 0))
    # 顯示並滾動背景圖片(往上移動)
    bg_y1 += 10  # 每次往下移動10像素(視覺上背景往上，fps=60)
    bg_y2 += 10
    # 當一張背景完全移出視窗，重設其y座標到另一張之上
    if bg_y1 >= WIN_HEIGHT:
        bg_y1 = bg_y2 - WIN_HEIGHT
    if bg_y2 >= WIN_HEIGHT:
        bg_y2 = bg_y1 - WIN_HEIGHT
    # 繪製兩張背景圖片，產生無縫滾動效果
    screen.blit(bg_img, (0, bg_y1))
    screen.blit(bg_img, (0, bg_y2))
    # 更新並繪製 playar（在背景之上）
    playar.update(WIN_WIDTH, WIN_HEIGHT)
    playar.draw(screen)
    # 更新並繪製子彈：從後往前掃描以利刪除已離開畫面的子彈
    for i in range(len(bullets) - 1, -1, -1):
        b = bullets[i]
        b.update()
        # 如果子彈已完全移出視窗上方，從清單中移除
        if b.y + b.height < 0:
            bullets.pop(i)
            continue
        b.draw(screen)
    # 更新並繪製敵人
    for e in enemies:
        e.update()
        # 如果敵人抵達畫面底部，則重新出現在頂端並隨機 x
        if e.y > WIN_HEIGHT:
            e.y = -e.height
            e.x = random.randint(0, max(0, WIN_WIDTH - e.width))
            # 隨機換圖
            e.image = random.choice(Enemy._images)
            e.width = e.image.get_width()
            e.height = e.image.get_height()
        # 檢查是否與任何子彈碰撞
        er = e.rect()
        hit = False
        for bi in range(len(bullets) - 1, -1, -1):
            b = bullets[bi]
            br = pygame.Rect(int(b.x), int(b.y), b.width, b.height)
            if er.colliderect(br):
                # 碰撞：移除子彈並重生敵人
                bullets.pop(bi)
                e.y = -e.height
                e.x = random.randint(0, max(0, WIN_WIDTH - e.width))
                e.image = random.choice(Enemy._images)
                e.width = e.image.get_width()
                e.height = e.image.get_height()
                hit = True
                break
        if not hit:
            e.draw(screen)
    pygame.display.update()  # 更新畫面
pygame.quit()
sys.exit()
