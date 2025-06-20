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
        global score
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
                for platform in platforms[:]:  # 用[:]避免移除時出錯
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
                        # 步驟10: 如果是只能踩一次的平台，踩到後立即消失
                        if platform.is_breakable:
                            platforms.remove(platform)
                        return  # 一旦碰到平台就結束檢查
            self.on_platform = False

    def check_spring_collision(self, springs):
        """
        檢查主角是否碰到任何彈簧，若碰撞則給予更高的跳躍力
        springs: 彈簧物件列表
        """
        # 只在主角往下掉時檢查碰撞
        if self.velocity_y > 0:
            # 根據下落速度決定檢查點數量，避免高速穿透彈簧
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
                for spring in springs:
                    # 檢查主角底部與彈簧頂部是否重疊，且左右有交集
                    if (
                        check_rect.bottom >= spring.rect.top
                        and check_rect.bottom <= spring.rect.top + 15  # 容錯範圍
                        and check_rect.right > spring.rect.left
                        and check_rect.left < spring.rect.right
                    ):
                        # 主角底部對齊彈簧頂部
                        self.y = spring.rect.top - self.height
                        self.rect.y = self.y
                        # 彈簧給予更高的跳躍力(往上跳25像素)
                        self.velocity_y = -25
                        self.on_platform = True
                        return  # 一旦碰到彈簧就結束檢查


###################### 平台類別 ######################
class Platform:
    def __init__(self, x, y, width, height, color, is_breakable=False):
        """
        初始化平台
        x, y: 平台左上角座標
        width, height: 平台寬高
        color: 平台顏色
        is_breakable: 是否為只能踩一次的消失平台 (預設False)
        """
        self.rect = pygame.Rect(x, y, width, height)  # 平台的矩形範圍
        self.color = color  # 平台顏色
        self.is_breakable = is_breakable  # 是否為只能踩一次的平台

    def draw(self, display_area):
        """
        在指定畫布上繪製平台
        display_area: pygame畫布
        """
        pygame.draw.rect(display_area, self.color, self.rect)


###################### 彈簧類別 ######################
class Spring:
    def __init__(self, x, y, width=20, height=10, color=(255, 255, 0)):
        """
        初始化彈簧道具
        x, y: 彈簧左上角座標 (通常在平台上方)
        width, height: 彈簧寬高 (預設20x10)
        color: 彈簧顏色 (預設黃色)
        """
        self.rect = pygame.Rect(x, y, width, height)  # 彈簧的矩形範圍
        self.color = color  # 彈簧顏色

    def draw(self, display_area):
        """
        在指定畫布上繪製彈簧
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
springs = []  # 用來裝所有彈簧物件的列表
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
    # 初始化時只產生白色平台，不判斷score
    is_breakable = False
    plat_color = platform_color
    platform = Platform(x, y, platform_w, platform_h, plat_color, is_breakable)
    platforms.append(platform)
    # 步驟8: 以20%機率在平台上方生成彈簧，並避免與平台重疊
    if random.random() < 0.2:
        spring_x = x + (platform_w - 20) // 2  # 彈簧水平置中於平台
        spring_y = y - 10  # 彈簧放在平台上方
        spring = Spring(spring_x, spring_y)
        springs.append(spring)


###################### 畫面捲動與平台自動生成 ######################
def update_camera(
    player, platforms, bg_y, bg_x, platform_w, platform_h, platform_color
):
    """
    畫面捲動與平台自動生成/移除，並計算分數
    當玩家上升到畫面中間以上時，固定玩家在畫面中間，並讓平台往下移動。
    當平台掉出畫面底部時自動移除，並在頂端自動生成新平台，保持平台數量。
    並根據相機移動距離累加分數。
    """
    global score, springs  # 使用全域分數與彈簧列表
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
        # 所有彈簧也要跟著平台一起往下移動
        for spring in springs:
            spring.rect.y += camera_move
        # 分數計算：每上升10像素加1分
        if camera_move > 0:
            score += int(camera_move / 10)
    # 移除掉出畫面底部的平台
    platforms[:] = [p for p in platforms if p.rect.top < bg_y]
    # 移除掉出畫面底部的彈簧
    springs[:] = [s for s in springs if s.rect.top < bg_y]
    # 追蹤目前最高的平台y座標
    y_min = min([p.rect.top for p in platforms]) if platforms else bg_y
    # 保持平台數量(原本8~10個+10個)
    while len(platforms) < num_platforms + 10:
        # 新平台y座標設在最高平台上方60像素
        new_y = y_min - 60
        new_x = random.randint(0, bg_x - platform_w)
        # 步驟10: 分數超過100分後，20%機率生成紅色只能踩一次的平台
        is_breakable = False
        plat_color = platform_color
        if score > 100 and random.random() < 0.2:
            is_breakable = True
            plat_color = (255, 0, 0)
        new_platform = Platform(
            new_x, new_y, platform_w, platform_h, plat_color, is_breakable
        )
        platforms.append(new_platform)
        # 步驟8: 以20%機率在新平台上方生成彈簧
        if random.random() < 0.2:
            spring_x = new_x + (platform_w - 20) // 2
            spring_y = new_y - 10
            spring = Spring(spring_x, spring_y)
            springs.append(spring)
        y_min = new_y  # 更新最高平台y座標


###################### 全域變數 ######################
score = 0  # 當前分數
highest_score = 0  # 最高分數
initial_player_y = player_y  # 玩家初始高度
game_over = False  # 遊戲是否結束

###################### 字型設定 ######################
font = pygame.font.Font("C:/Windows/Fonts/msjh.ttc", 28)  # 使用微軟正黑體顯示分數
big_font = pygame.font.Font("C:/Windows/Fonts/msjh.ttc", 48)  # 遊戲結束大字體


###################### 遊戲重置函式 ######################
def reset_game():
    """
    重設遊戲狀態，讓遊戲重新開始
    """
    global score, game_over, initial_player_y, platforms, player, springs
    # 重設主角位置與速度
    player.x = player_x
    player.y = player_y
    player.rect.x = player_x
    player.rect.y = player_y
    player.velocity_y = 0
    # 重新生成平台
    platforms.clear()
    springs.clear()  # 重新生成彈簧
    base_platform = Platform(
        platform_x, platform_y, platform_w, platform_h, platform_color
    )
    platforms.append(base_platform)
    for i in range(1, num_platforms):
        x = random.randint(0, bg_x - platform_w)
        y = (bg_y - 100) - (i * 60)
        # 遊戲重置時只產生白色平台
        is_breakable = False
        plat_color = platform_color
        platform = Platform(x, y, platform_w, platform_h, plat_color, is_breakable)
        platforms.append(platform)
        # 步驟8: 以20%機率在平台上方生成彈簧
        if random.random() < 0.2:
            spring_x = x + (platform_w - 20) // 2
            spring_y = y - 10
            spring = Spring(spring_x, spring_y)
            springs.append(spring)
    score = 0
    initial_player_y = player_y
    game_over = False


###################### 主程式 ######################
while True:
    FPS.tick(60)  # 每秒最多更新60次，讓遊戲流暢且不會過快
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 按下視窗關閉鍵(X)
            pygame.quit()
            sys.exit()
        # 遊戲結束時，按下任意鍵重新開始
        if game_over and event.type == pygame.KEYDOWN:
            reset_game()

    # 取得目前按下的按鍵狀態
    keys = pygame.key.get_pressed()
    if not game_over:
        # 如果按下左方向鍵，主角向左移動
        if keys[pygame.K_LEFT]:
            player.move(-1, bg_x)
        # 如果按下右方向鍵，主角向右移動
        if keys[pygame.K_RIGHT]:
            player.move(1, bg_x)

        # --- 步驟9: 先檢查彈簧碰撞，再檢查平台碰撞 ---
        player.apply_gravity()  # 主角自動下落
        player.check_spring_collision(springs)  # 先偵測彈簧碰撞，給予超高跳躍力
        player.check_platform_collision(platforms)  # 再偵測平台碰撞，給予一般跳躍力
        update_camera(
            player, platforms, bg_y, bg_x, platform_w, platform_h, platform_color
        )  # 畫面捲動、平台管理與分數計算

        # 遊戲結束判定：主角掉出畫面底部
        if player.rect.top > bg_y and not game_over:
            game_over = True
            if score > highest_score:
                highest_score = score

    screen.fill((0, 0, 0))  # 填滿黑色背景
    # 呼叫主角的draw方法繪製主角
    player.draw(screen)
    # 繪製所有平台
    for platform in platforms:
        platform.draw(screen)
    # 步驟8: 繪製所有彈簧
    for spring in springs:
        spring.draw(screen)

    # 顯示分數與最高分數
    score_text = font.render(f"分數: {score}", True, (255, 255, 0))
    high_text = font.render(f"最高分: {highest_score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(high_text, (10, 50))

    # 遊戲結束畫面
    if game_over:
        over_text = big_font.render("遊戲結束", True, (255, 0, 0))
        restart_text = font.render("按任意鍵重新開始", True, (255, 255, 255))
        screen.blit(over_text, (bg_x // 2 - over_text.get_width() // 2, bg_y // 2 - 60))
        screen.blit(
            restart_text, (bg_x // 2 - restart_text.get_width() // 2, bg_y // 2)
        )

    pygame.display.update()  # 更新畫面
