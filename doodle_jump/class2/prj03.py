###################### 載入套件 ######################
import pygame  # 匯入pygame模組
import sys  # 匯入系統模組

###################### 初始化設定 ######################
pygame.init()  # 初始化pygame
FPS = pygame.time.Clock()  # 設定FPS物件，控制遊戲更新速度

###################### 遊戲視窗設定 ######################
bg_x = 400  # 視窗寬度
bg_y = 600  # 視窗高度
bg_size = (bg_x, bg_y)
pygame.display.set_caption("Doodle Jump - 步驟3")  # 設定視窗標題
screen = pygame.display.set_mode(bg_size)  # 建立視窗


###################### 主角類別 ######################
class Player:
    def __init__(self, x, y, width, height, color):
        """
        初始化主角
        x, y: 主角左上角座標
        width, height: 主角寬高
        color: 主角顏色
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 5  # 主角移動速度(每次移動5像素)

    def draw(self, display_area):
        """
        在指定畫布上繪製主角
        display_area: pygame畫布
        """
        pygame.draw.rect(
            display_area, self.color, (self.x, self.y, self.width, self.height)
        )

    def move(self, direction, bg_x):
        """
        控制主角左右移動，並實現穿牆效果
        direction: -1(左移) 或 1(右移)
        bg_x: 視窗寬度
        """
        self.x += direction * self.speed  # 根據方向與速度調整x座標
        # 穿牆效果：如果主角完全移出左邊界，從右側出現
        if self.x + self.width < 0:
            self.x = bg_x
        # 穿牆效果：如果主角完全移出右邊界，從左側出現
        if self.x > bg_x:
            self.x = -self.width


###################### 平台類別 ######################
class Platform:
    def __init__(self, x, y, width, height, color):
        """
        初始化平台
        x, y: 平台左上角座標
        width, height: 平台寬高
        color: 平台顏色
        """
        self.rect = pygame.Rect(x, y, width, height)  # 平台的矩形範圍
        self.color = color  # 平台顏色

    def draw(self, display_area):
        """
        在指定畫布上繪製平台
        display_area: pygame畫布
        """
        pygame.draw.rect(display_area, self.color, self.rect)


###################### 主角設定 ######################
player_w = 30  # 主角寬度
player_h = 30  # 主角高度
player_color = (0, 255, 0)  # 主角顏色(綠色)
# 主角初始位置：底部中間，底部上方50像素
player_x = bg_x // 2 - player_w // 2
player_y = bg_y - player_h - 50
# 建立主角物件
player = Player(player_x, player_y, player_w, player_h, player_color)

###################### 平台設定 ######################
platform_w = 60  # 平台寬度
platform_h = 10  # 平台高度
platform_x = (bg_x - platform_w) // 2  # 平台水平置中
platform_y = bg_y - platform_h - 10  # 平台放在視窗底部上方10像素
platform_color = (255, 255, 255)  # 平台顏色(白色)
# 建立平台物件
platform = Platform(platform_x, platform_y, platform_w, platform_h, platform_color)

###################### 主程式 ######################
while True:
    FPS.tick(60)  # 每秒最多更新60次，讓遊戲流暢且不會過快
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 按下視窗關閉鍵(X)
            pygame.quit()
            sys.exit()

    # 取得目前按下的按鍵狀態
    keys = pygame.key.get_pressed()
    # 如果按下左方向鍵，主角向左移動
    if keys[pygame.K_LEFT]:
        player.move(-1, bg_x)
    # 如果按下右方向鍵，主角向右移動
    if keys[pygame.K_RIGHT]:
        player.move(1, bg_x)

    screen.fill((0, 0, 0))  # 填滿黑色背景
    # 呼叫主角的draw方法繪製主角
    player.draw(screen)
    # 呼叫平台的draw方法繪製平台
    platform.draw(screen)

    pygame.display.update()  # 更新畫面
