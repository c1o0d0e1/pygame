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
def main():
    # 背景初始y座標(從底部開始)
    bg_y1 = 0
    bg_y2 = -WIN_HEIGHT
    running = True
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
        pygame.display.update()  # 更新畫面
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
