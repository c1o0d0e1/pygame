###################### 載入套件 ######################
import pygame  # 匯入pygame模組
import sys  # 匯入系統模組
import random  # 匯入隨機模組

###################### 初始化設定 ######################
pygame.init()  # 初始化pygame
FPS = pygame.time.Clock()  # 設定FPS物件，控制遊戲更新速度

###################### 遊戲視窗設定 ######################
bg_x = 400  # 視窗寬度
bg_y = 600  # 視窗高度
bg_size = (bg_x, bg_y)
pygame.display.set_caption("Doodle Jump - 步驟6")  # 設定視窗標題
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
        # --- 步驟5新增 ---
        self.velocity_y = 0  # 垂直速度
        self.jump_power = -12  # 跳躍初始力量(負值向上)
        self.gravity = 0.5  # 重力加速度
        self.on_platform = False  # 是否站在平台上
        self.rect = pygame.Rect(
            self.x, self.y, self.width, self.height
        )  # 主角的矩形範圍

    def draw(self, display_area):
        """
        在指定畫布上繪製主角
        display_area: pygame畫布
        """
        pygame.draw.rect(display_area, self.color, self.rect)

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
        self.rect.x = self.x  # 更新rect位置

    def apply_gravity(self):
        """
        應用重力，讓主角自動下落
        """
        self.velocity_y += self.gravity  # 垂直速度增加重力
        self.y += self.velocity_y  # y座標根據速度變化
        self.rect.y = self.y  # 更新rect位置

    def check_platform_collision(self, platforms):
        """
        檢查主角是否落在任一平台上，並處理彈跳
        platforms: 平台物件列表
        """
        # 只在主角往下掉時檢查碰撞
        if self.velocity_y > 0:
            # 根據下落速度決定檢查點數量，避免高速穿透平台
            steps = max(1, int(self.velocity_y // 5))
            for step in range(1, steps + 1):
                # 計算每個檢查點的y座標
                check_y = (
                    self.rect.bottom
                    - self.velocity_y
                    + (self.velocity_y * step / steps)
                )
                check_rect = pygame.Rect(
                    self.rect.left, check_y - self.height, self.width, self.height
                )
                for platform in platforms:
                    # 檢查主角底部與平台頂部是否重疊，且左右有交集
                    if (
                        check_rect.bottom >= platform.rect.top
                        and check_rect.bottom <= platform.rect.top + 15  # 容錯範圍
                        and check_rect.right > platform.rect.left
                        and check_rect.left < platform.rect.right
                    ):
                        self.y = platform.rect.top - self.height  # 主角底部對齊平台頂部
                        self.rect.y = self.y  # 更新rect位置
                        self.velocity_y = self.jump_power  # 彈跳(向上)
                        self.on_platform = True
                        return  # 一旦碰到平台就結束檢查
            self.on_platform = False


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
platform_color = (255, 255, 255)  # 平台顏色(白色)

# 建立平台列表，並隨機生成8~10個平台
platforms = []  # 用來裝所有平台物件的列表
# 先建立底部平台，確保玩家不會掉下去
platform_x = (bg_x - platform_w) // 2  # 平台水平置中
platform_y = bg_y - platform_h - 10  # 平台放在視窗底部上方10像素
base_platform = Platform(platform_x, platform_y, platform_w, platform_h, platform_color)
platforms.append(base_platform)
# 隨機產生其餘平台，y座標依序往上排列，間距60像素
num_platforms = random.randint(8, 10)
for i in range(1, num_platforms):
    x = random.randint(0, bg_x - platform_w)
    y = (bg_y - 100) - (i * 60)
    platform = Platform(x, y, platform_w, platform_h, platform_color)
    platforms.append(platform)


###################### 畫面捲動與平台自動生成 ######################
def update_camera(
    player, platforms, bg_y, bg_x, platform_w, platform_h, platform_color
):
    """
    畫面捲動與平台自動生成/移除
    當玩家上升到畫面中間以上時，固定玩家在畫面中間，並讓平台往下移動。
    當平台掉出畫面底部時自動移除，並在頂端自動生成新平台，保持平台數量。
    """
    screen_middle = bg_y // 2  # 畫面中間y座標
    camera_move = 0  # 相機移動距離
    # 若玩家上升到畫面中間以上，開始畫面捲動
    if player.rect.y < screen_middle:
        camera_move = screen_middle - player.rect.y  # 計算要移動的距離
        player.y += camera_move  # 固定玩家在畫面中間
        player.rect.y = player.y
        # 所有平台往下移動camera_move
        for platform in platforms:
            platform.rect.y += camera_move
    # 移除掉出畫面底部的平台
    platforms[:] = [p for p in platforms if p.rect.top < bg_y]
    # 追蹤目前最高的平台y座標
    y_min = min([p.rect.top for p in platforms]) if platforms else bg_y
    # 保持平台數量(原本8~10個+10個)
    while len(platforms) < num_platforms + 10:
        # 新平台y座標設在最高平台上方60像素
        new_y = y_min - 60
        new_x = random.randint(0, bg_x - platform_w)
        new_platform = Platform(new_x, new_y, platform_w, platform_h, platform_color)
        platforms.append(new_platform)
        y_min = new_y  # 更新最高平台y座標


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

    # --- 步驟6: 應用重力、平台碰撞、畫面捲動與平台自動生成 ---
    player.apply_gravity()  # 主角自動下落
    player.check_platform_collision(platforms)  # 檢查是否落在任一平台上並彈跳
    update_camera(
        player, platforms, bg_y, bg_x, platform_w, platform_h, platform_color
    )  # 畫面捲動與平台管理

    screen.fill((0, 0, 0))  # 填滿黑色背景
    # 呼叫主角的draw方法繪製主角
    player.draw(screen)
    # 繪製所有平台
    for platform in platforms:
        platform.draw(screen)

    pygame.display.update()  # 更新畫面
