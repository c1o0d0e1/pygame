###################### 載入套件 ######################
import pygame  # 匯入pygame模組
import sys  # 匯入系統模組

###################### 初始化設定 ######################
pygame.init()  # 初始化pygame

###################### 遊戲視窗設定 ######################
bg_x = 400  # 視窗寬度
bg_y = 600  # 視窗高度
bg_size = (bg_x, bg_y)
pygame.display.set_caption("Doodle Jump - 步驟1")  # 設定視窗標題
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

    def draw(self, display_area):
        """
        在指定畫布上繪製主角
        display_area: pygame畫布
        """
        pygame.draw.rect(
            display_area, self.color, (self.x, self.y, self.width, self.height)
        )


###################### 主角設定 ######################
player_w = 30  # 主角寬度
player_h = 30  # 主角高度
player_color = (0, 255, 0)  # 主角顏色(綠色)
# 主角初始位置：底部中間，底部上方50像素
player_x = bg_x // 2 - player_w // 2
player_y = bg_y - player_h - 50
# 建立主角物件
player = Player(player_x, player_y, player_w, player_h, player_color)

###################### 主程式 ######################
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 按下視窗關閉鍵(X)
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))  # 填滿黑色背景
    # 呼叫主角的draw方法繪製主角
    player.draw(screen)

    pygame.display.update()  # 更新畫面
