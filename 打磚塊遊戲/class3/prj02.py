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


######################定義函式區######################

######################初始化設定######################
pygame.init()  # 啟動pygame
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

######################球設定######################

######################遊戲結束設定######################

######################主程式######################
while True:  # 無限迴圈
    for event in pygame.event.get():  # 取得事件
        if event.type == pygame.QUIT:  # 如果事件是關閉視窗 (X)
            sys.exit()  # 結束程式
        for brick in bricks:  # 繪製磚塊
            brick.draw(screen)
    pygame.display.update()  # 更新視窗
