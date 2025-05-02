######################匯入模組######################
import pygame
import sys

######################初始化######################
pygame.init()  # 啟動pygame
width = 640  # 設定視窗寬度
height = 320  # 設定視窗高度
######################建立視窗及物件######################
# 設定視窗大小
screen = pygame.display.set_mode((width, height))  # 建立視窗
# 設定視窗標題
pygame.display.set_caption("my game")  # 設定視窗標題
######################循環偵測######################
while True:  # 無限迴圈
    for event in pygame.event.get():  # 取得事件
        if event.type == pygame.QUIT:  # 如果事件是關閉視窗 (X)
            sys.exit()  # 結束程式
