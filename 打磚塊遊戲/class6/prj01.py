######################載入套件######################
import pygame
import sys
import random  # 匯入隨機模組


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


class Bomb:
    def __init__(self, center_col, y_type, is_super=False):
        self.center_col = center_col
        self.y_type = y_type  # 'bottom', 'middle', 'super'
        self.is_super = is_super
        if y_type == "bottom":
            self.center_row = bricks_row
        elif y_type == "middle":
            self.center_row = bricks_row // 2
        elif y_type == "super":
            self.center_row = bricks_row // 2
            self.center_col = bricks_column // 2
        self.affected = set()
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                r = self.center_row + dr
                c = self.center_col + dc
                if 0 <= r < bricks_row and 0 <= c < bricks_column:
                    self.affected.add((r, c))
        self.visible = True

    def get_center(self):
        x = self.center_col * (bricks_width + briaks_gap) + 70 + bricks_width // 2
        if self.y_type == "bottom":
            y = (bricks_row) * (bricks_height + briaks_gap) + 60 + bricks_height // 2
        else:
            y = (
                (self.center_row) * (bricks_height + briaks_gap)
                + 60
                + bricks_height // 2
            )
        return x, y

    def draw(self, display_area, shake_offset=(0, 0)):
        if not self.visible:
            return
        x, y = self.get_center()
        x += shake_offset[0]
        y += shake_offset[1]
        radius = 18 if not self.is_super else 36
        # 畫黑色圓球
        pygame.draw.circle(display_area, (30, 30, 30), (x, y), radius)
        # 畫導火線
        pygame.draw.line(
            display_area,
            (180, 180, 180),
            (x, y - radius),
            (x, y - radius - 14),
            4 if not self.is_super else 8,
        )
        # 畫火花
        pygame.draw.circle(
            display_area,
            (255, 200, 0),
            (x, y - radius - 18),
            6 if not self.is_super else 12,
        )


######################定義函式區######################

######################初始化設定######################
pygame.init()  # 啟動pygame
FPS = pygame.time.Clock()  # 設定FPS
# 新增遊戲狀態與生命次數
lives = 3  # 玩家生命次數
max_lives = 3
score = 0  # 分數初始化
game_over = False  # 遊戲是否結束


def reset_game():
    global bricks, score, lives, game_over, ball, pad
    # 重設磚塊
    bricks.clear()
    for column in range(bricks_column):
        for row in range(bricks_row):
            x = column * (bricks_width + briaks_gap) + 70
            y = row * (bricks_height + briaks_gap) + 60
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            brick = Brick(x, y, bricks_width, bricks_height, color)
            bricks.append(brick)
    # 重設分數與生命
    score = 0
    lives = max_lives
    game_over = False
    # 重設底板與球
    pad.rect.x = 0
    pad.rect.y = bg_y - 48
    ball.x = pad.rect.x + pad.rect.width // 2
    ball.y = pad.rect.y - ball_radius
    ball.is_moving = False
    ball.speed_x = 5
    ball.speed_y = -5
    # 重設炸彈
    place_bombs()


# 新增炸彈初始化
bombs = []


def place_bombs():
    global bombs, bomb_area_all
    bombs = []
    used = set()
    # 先產生2顆 bottom 炸彈
    count = 0
    while count < 2:
        center_col = random.randint(1, bricks_column - 2)
        y_type = "bottom"
        bomb = Bomb(center_col, y_type)
        bomb_area = bomb.affected
        if not any((r, c) in used for (r, c) in bomb_area):
            bombs.append(bomb)
            used.update(bomb_area)
            count += 1
    # 再產生2顆 middle 炸彈
    count = 0
    while count < 2:
        center_col = random.randint(1, bricks_column - 2)
        y_type = "middle"
        bomb = Bomb(center_col, y_type)
        bomb_area = bomb.affected
        if not any((r, c) in used for (r, c) in bomb_area):
            bombs.append(bomb)
            used.update(bomb_area)
            count += 1
    # 新增1顆超級炸彈在正中央
    super_bomb = Bomb(bricks_column // 2, "super", is_super=True)
    bombs.append(super_bomb)
    bomb_area_all = used | super_bomb.affected


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

# 產生磚塊時跳過炸彈九宮格
for column in range(bricks_column):
    for row in range(bricks_row):
        if "bomb_area_all" in globals() and (row, column) in bomb_area_all:
            continue
        x = column * (bricks_width + briaks_gap) + 70
        y = row * (bricks_height + briaks_gap) + 60
        color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        brick = Brick(x, y, bricks_width, bricks_height, color)
        bricks.append(brick)

place_bombs()  # 將 place_bombs() 呼叫移到這裡

######################顯示文字設定######################
font_path = "C:/Windows/Fonts/msjh.ttc"
font = pygame.font.Font(font_path, 32)

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
# 主程式區
explosions = []
shake_frames = 0
victory = False
while True:  # 無限迴圈
    FPS.tick(60)  # 設定fps為60
    # 畫面震動特效
    shake_offset = (0, 0)
    if shake_frames > 0:
        shake_offset = (random.randint(-12, 12), random.randint(-12, 12))
        shake_frames -= 1
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
        # 檢查炸彈碰撞
        bomb_exploded = False
        for bomb in bombs:
            if not bomb.visible:
                continue
            for r, c in bomb.affected:
                idx = c * bricks_row + r
                if 0 <= idx < len(bricks):
                    brick = bricks[idx]
                    dx = abs(ball.x - (brick.rect.x + brick.rect.width / 2))
                    dy = abs(ball.y - (brick.rect.y + brick.rect.height / 2))
                    if (
                        not brick.hit
                        and dx < (ball.radius + brick.rect.width / 2)
                        and dy <= (ball.radius + brick.rect.height / 2)
                    ):
                        # 超級炸彈爆炸
                        if bomb.is_super:
                            for b in bombs:
                                b.visible = False
                            for b in bricks:
                                b.hit = True
                            bx, by = bomb.get_center()
                            explosions.append(
                                {"x": bx, "y": by, "frame": 0, "super": True}
                            )
                            shake_frames = 20
                            victory = True
                        else:
                            for rr, cc in bomb.affected:
                                idx2 = cc * bricks_row + rr
                                if 0 <= idx2 < len(bricks):
                                    bricks[idx2].hit = True
                            bomb.visible = False
                            bx, by = bomb.get_center()
                            explosions.append(
                                {"x": bx, "y": by, "frame": 0, "super": False}
                            )
                            shake_frames = 8
                        bomb_exploded = True
                        break
                if bomb_exploded:
                    break
            if bomb_exploded:
                break
        # 檢查碰撞時取得本次擊中磚塊數
        hit_count = 0
        for brick in bricks:
            if not brick.hit:
                dx = abs(ball.x - (brick.rect.x + brick.rect.width / 2))
                dy = abs(ball.y - (brick.rect.y + brick.rect.height / 2))
                if dx < (ball.radius + brick.rect.width / 2) and dy <= (
                    ball.radius + brick.rect.height / 2
                ):
                    brick.hit = True
                    hit_count += 1
                    if (
                        ball.x < brick.rect.x
                        or ball.x > brick.rect.x + brick.rect.width
                    ):
                        ball.speed_x = -ball.speed_x
                    else:
                        ball.speed_y = -ball.speed_y
        score += hit_count
        ball.check_collision(bg_x, bg_y, bricks, pad)
        if not ball.is_moving and not victory:
            lives -= 1
            if lives <= 0:
                game_over = True

    for event in pygame.event.get():  # 取得事件
        if event.type == pygame.QUIT:  # 如果事件是關閉視窗 (X)
            sys.exit()  # 結束程式
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 第一次按下滑鼠左鍵時直接開始遊戲
            if not ball.is_moving and score == 0 and not game_over:
                ball.is_moving = True
            # 遊戲結束時按下滑鼠重新開始
            elif not ball.is_moving and game_over:
                reset_game()
            # 遊戲進行中球掉落後按下滑鼠才繼續
            elif not ball.is_moving and not game_over and score > 0:
                ball.is_moving = True

    for brick in bricks:  # 繪製磚塊
        brick.draw(screen)
    # 繪製炸彈
    for bomb in bombs:
        bomb.draw(screen, shake_offset)
    # 繪製爆炸特效
    for explosion in explosions[:]:
        frame = explosion["frame"]
        x = explosion["x"] + shake_offset[0]
        y = explosion["y"] + shake_offset[1]
        if explosion.get("super"):
            # 超級炸彈爆炸：更大更亮
            if frame < 20:
                pygame.draw.circle(screen, (255, 255, 0), (x, y), 80 + frame * 2)
                pygame.draw.circle(screen, (255, 0, 0), (x, y), 40 + frame)
                explosion["frame"] += 1
            else:
                explosions.remove(explosion)
        else:
            if frame < 10:
                pygame.draw.circle(screen, (255, 255, 0), (x, y), 30 + frame * 2)
                pygame.draw.circle(screen, (255, 0, 0), (x, y), 15 + frame)
                explosion["frame"] += 1
            else:
                explosions.remove(explosion)
    pad.draw(screen)
    ball.draw(screen)
    # 顯示分數在左上角
    score_text = font.render(f"分數: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    # 顯示剩餘生命
    lives_text = font.render(f"生命: {lives}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 50))
    # 顯示遊戲結束
    if game_over:
        over_text = font.render("遊戲結束", True, (255, 0, 0))
        screen.blit(over_text, (bg_x // 2 - 100, bg_y // 2 - 32))
    # 顯示勝利
    if victory:
        victory_text = font.render("勝利!", True, (0, 255, 0))
        screen.blit(victory_text, (bg_x // 2 - 100, bg_y // 2 - 32))
    pygame.display.update()
