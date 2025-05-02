######################載入套件######################
import pygame
import sys


######################物件類別######################
class Brick:
    def __init__(self, x, y, width, height, color):
        """
        初始化磚塊\n
        x, y: 磚塊的左上角座標\n
        width, height: 磚塊的寬度和高度\n
        color: 磚塊的顏色\n
        """
        self.rect = pygame.Rect(x, y, width, height)  # 磚塊的矩形範圍
        self.color = color
        self.hit = False  # 磚塊是否被擊中

    def draw(self, display_area):
        """
        繪製磚塊\n
        display: 顯示的畫布\n
        """
        if not self.hit:
            pygame.draw.rect(display_area, self.color, self.rect)


class Ball:
    def __init__(self, x, y, radius, color):
        """
        初始化球\n
        x, y: 球的圓心座標\n
        radius: 球的半徑\n
        color: 球的顏色\n
        """
        self.x = x  # 球的x座標
        self.y = y  # 球的y座標
        self.radius = radius  # 球的半徑
        self.color = color  # 球的顏色
        self.speed_x = 5  # 球的x速度
        self.speed_y = -5  # 球的y速度
        self.is_moving = False  # 球是否在移動

    def draw(self, display_area):
        """
        繪製球\n
        display_area: 顯示的畫布\n
        """
        pygame.draw.circle(
            display_area, self.color, (int(self.x), int(self.y)), self.radius
        )

    def move(self):
        """
        移動球\n
        """
        if self.is_moving:
            self.x += self.speed_x  # 更新球的x座標
            self.y += self.speed_y  # 更新球的y座標

    def check_collision(self, bg_x, bg_y, bricks, pad):
        """
        檢查碰撞並處理反彈\n
        bg_x, bg_y: 遊戲視窗寬高\n
        bricks: 磚塊列表\n
        pad: 底板物件
        """
        # 檢查與視窗邊緣的碰撞
        if self.x - self.radius < 0 or self.x + self.radius > bg_x:
            self.speed_x = -self.speed_x  # 水平反彈
        if self.y - self.radius <= 0:
            self.speed_y = -self.speed_y  # 垂直反彈
        if self.y + self.radius > bg_y:
            self.is_moving = False  # 球停止移動
        # 改進與底板的碰撞檢測
        if (
            self.y + self.radius >= pad.rect.y
            and self.y + self.radius <= pad.rect.y + pad.rect.height
            and self.x >= pad.rect.x
            and self.x <= pad.rect.x + pad.rect.width
        ):
            self.speed_y = -abs(self.speed_y)  # 垂直反彈
        # 檢查與磚塊的碰撞
        for brick in bricks:
            if not brick.hit:  # 磚塊未被擊中
                # 簡單的矩形碰撞檢測
                # 計算球心到磚塊的距離
                dx = abs(self.x - (brick.rect.x + brick.rect.width / 2))
                dy = abs(self.y - (brick.rect.y + brick.rect.height / 2))

                # 檢查是否碰撞
                if dx < (self.radius + brick.rect.width / 2) and dy <= (
                    self.radius + brick.rect.height / 2
                ):
                    brick.hit = True  # 磚塊被擊中

                    # 計算反彈方向
                    # 從磚塊的哪邊碰撞決定反彈方向
                    if (
                        self.x < brick.rect.x
                        or self.x > brick.rect.x + brick.rect.width
                    ):
                        self.speed_x = -self.speed_x  # 水平反彈
                    else:
                        self.speed_y = -self.speed_y  # 垂直反彈


######################定義函式區######################

######################初始化設定######################
pygame.init()  # 啟動pygame
FPS = pygame.time.Clock()  # 設定FPS
######################載入圖片######################

######################遊戲視窗設定######################
bg_x = 800
bg_y = 600  # 設定視窗大小
bg_size = (bg_x, bg_y)  # 設定視窗大小
pygame.display.set_caption("打磚塊遊戲")  # 設定視窗標題
screen = pygame.display.set_mode(bg_size)  # 建立視窗
######################磚塊######################
bricks_row = 9  # 磚塊行數
bricks_column = 11  # 磚塊列數
bricks_width = 58  # 磚塊寬度
bricks_height = 16  # 磚塊高度
briaks_gap = 2  # 磚塊間距
bricks = []  # 磚塊列表(用來裝磚塊物件的列表)
import random  # 匯入隨機模組

for column in range(bricks_column):  # 磚塊列數
    for row in range(bricks_row):  # 磚塊行數
        x = column * (bricks_width + briaks_gap) + 70  # 磚塊的x座標
        y = row * (bricks_height + briaks_gap) + 60  # 磚塊的y座標
        color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )  # 隨機顏色
        brick = Brick(x, y, bricks_width, bricks_height, color)  # 磚塊物件
        bricks.append(brick)  # 將磚塊物件加入磚塊列表
######################顯示文字設定######################

######################底板設定######################
pad = Brick(
    0, bg_y - 48, bricks_width, bricks_height, (255, 255, 255)
)  # 初始化底板物件
######################球設定######################
ball_radius = 10  # 球的半徑
ball_color = (255, 215, 0)  # 金色
ball = Ball(
    pad.rect.x + pad.rect.width // 2, pad.rect.y - ball_radius, ball_radius, ball_color
)  # 初始化球物件

######################遊戲結束設定######################

######################新增fps#######################
FPS = pygame.time.Clock()  # 設定fps
######################主程式######################
while True:  # 無限迴圈
    FPS.tick(60)  # 設定fps為60
    screen.fill((0, 0, 0))  # 清除畫面
    mos_x, mos_y = pygame.mouse.get_pos()  # 取得滑鼠座標
    pad.rect.x = mos_x - pad.rect.width // 2  # 設定底板的x座標

    if pad.rect.x < 0:
        pad.rect.x = 0  # 如果底板的x座標小於0，則設定為0
    if pad.rect.x + pad.rect.width > bg_x:
        pad.rect.x = bg_x - pad.rect.width  # 限制底板的x座標不超過視窗的寬度

    # 如果球未移動，則跟隨底板移動
    if not ball.is_moving:
        ball.x = pad.rect.x + pad.rect.width // 2  # 設定球的x座標
        ball.y = pad.rect.y - ball_radius  # 設定球的y座標
    else:
        # 如果球在移動，進行移動和碰撞檢查
        ball.move()
        ball.check_collision(bg_x, bg_y, bricks, pad)

    for event in pygame.event.get():  # 取得事件
        if event.type == pygame.QUIT:  # 如果事件是關閉視窗 (X)
            sys.exit()  # 結束程式
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 點擊滑鼠左鍵開始移動球
            print(ball.is_moving)
            if not ball.is_moving:
                ball.is_moving = True

    for brick in bricks:  # 繪製磚塊
        brick.draw(screen)

    pad.draw(screen)  # 繪製底板
    ball.draw(screen)  # 繪製球

    pygame.display.update()  # 更新視窗
