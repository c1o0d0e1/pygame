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
######################建立畫布######################
# 建立畫布
bg = pygame.Surface((width, height))  # 建立畫布
# 畫布為白色
bg.fill((255, 255, 255))  # 畫布為白色
######################繪製圖形######################
# 畫圓形 (畫布, 顏色, 圓心座標, 半徑)
pygame.draw.circle(bg, (0, 0, 255), (200, 100), 30, 0)  # 畫圓形
pygame.draw.circle(bg, (0, 0, 255), (400, 100), 30, 0)  # 畫圓形
# 畫矩形 (畫布, 顏色, 矩形座標, 寬度, 高度)
pygame.draw.rect(bg, (0, 255, 0), (270, 130, 60, 40), 5)  # 畫矩形
# 畫橢圓(畫布, 顏色, [x, y, 寬, 高], 線寬)
pygame.draw.ellipse(bg, (255, 0, 0), [130, 160, 60, 35], 5)  # 畫橢圓
pygame.draw.ellipse(bg, (255, 0, 0), [400, 160, 60, 35], 5)  # 畫橢圓
# 畫線, (畫布, 顏色, 起點座標, 終點座標, 線寬)
pygame.draw.line(bg, (255, 0, 255), (280, 220), (320, 220), 3)  # 畫線
# 畫多邊形 (畫布, 顏色, [[x1, y2], [x2, y2][x3, y3]], 線寬)
# pygame.draw.polygon(bg, (100, 200, 45), [[100, 100], [0, 200], [200, 200]], 0)  # 畫多邊形
# 畫多邊形
# 畫弧 (畫布, 顏色, [x, y, 寬, 高], 起始角度, 結束角度, 線寬)
# pygame.draw.arc(bg, (255, 10, 0), [100, 100, 100, 50], math.radians(180), math.radians(0), 5)  # 畫弧
######################循環偵測######################
while True:  # 無限迴圈
    x, y = pygame.mouse.get_pos()  # 取得滑鼠座標
    for event in pygame.event.get():  # 取得事件
        if event.type == pygame.QUIT:  # 如果事件是關閉視窗 (X)
            sys.exit()  # 結束程式

        if event.type == pygame.MOUSEBUTTONDOWN:  # 如果事件是滑鼠按下
            print("滑鼠按下")  # 印出滑鼠按下
            print(f"滑鼠座標: {x}, {y}")  # 印出滑鼠座標

    # 畫布顯示在視窗左上角
    screen.blit(bg, (0, 0))  # 畫布顯示在視窗左上角
    # 更新視窗
    pygame.display.update()  # 更新視窗
