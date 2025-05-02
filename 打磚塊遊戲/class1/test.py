######################匯入模組######################
import pygame
import sys
import random

######################初始化######################
pygame.init()  # 啟動pygame
width = 1000  # 設定視窗寬度
height = 600  # 設定視窗高度
######################建立視窗及物件######################
# 設定視窗大小
screen = pygame.display.set_mode((width, height))  # 建立視窗
# 設定視窗標題
pygame.display.set_caption("繪畫")  # 設定視窗標題
######################建立畫布######################
# 建立畫布
bg = pygame.Surface((width, height))  # 建立畫布
# 畫布為白色
bg.fill((255, 255, 255))
# 畫布為白色
######################循環偵測######################
paint = False  # 畫圖狀態
color = (0, 0, 0)  # 畫圖顏色 (R, G, B)
while True:  # 無限迴圈
    x, y = pygame.mouse.get_pos()  # 取得滑鼠座標
    for event in pygame.event.get():  # 取得事件
        if event.type == pygame.QUIT:  # 如果事件是關閉視窗 (X)
            sys.exit()  # 結束程式

        if event.type == pygame.MOUSEBUTTONDOWN:  # 如果事件是滑鼠按下
            paint = not (paint)  ## 切換畫圖狀態

        if paint:  # 繪圖狀態 (切換畫圖狀態)
            pygame.draw.circle(bg, color, (x, y), 10, 0)  # 跟隨滑鼠位置畫圓

        if paint == False:
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
        # 隨機顏色

    # 畫布顯示在視窗左上角
    screen.blit(bg, (0, 0))  # 畫布顯示在視窗左上角
    # 更新視窗
    pygame.display.update()  # 更新視窗
