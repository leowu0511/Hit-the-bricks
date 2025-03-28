import pygame
import random
import math
import tkinter as tk
from tkinter import ttk

# 初始化
pygame.init()
pygame.mixer.init()  # 初始化音效

# 設定遊戲窗口
WIDTH, HEIGHT = 800, 350
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("消磚塊遊戲")

# 顏色設置
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)
BLUE = (0, 0, 255)

# 板子的設置
paddle_width, paddle_height = 100, 20
paddle_x, paddle_y = WIDTH // 2 - paddle_width // 2, HEIGHT - paddle_height - 10
paddle_speed = 10  # 板子的速度

# 球的設置
ball_radius = 10
initial_balls = 1  # 開局的球數量
ball_speed = 3  # 初始球的速度
max_ball_speed = 10  # 最大球速

# 磚塊的設置
brick_width = 60
brick_height = 20
brick_padding = 10
special_brick_chance = 0.1

# 分數設置
score = 0
level = 1  # 初始關卡

# 載入音效檔案
pop_sound = pygame.mixer.Sound("pop.mp3")

def create_ball_with_angle(x, y, angle):
    angle_rad = math.radians(angle)
    return {
        "x": x, 
        "y": y, 
        "dx": ball_speed * math.cos(angle_rad),
        "dy": -ball_speed * math.sin(angle_rad)
    }

def create_bricks():
    return [
        {
            "rect": pygame.Rect(
                j * (brick_width + brick_padding) + 50, 
                i * (brick_height + brick_padding) + 50, 
                brick_width, 
                brick_height
            ), 
            "is_special": random.random() < special_brick_chance
        } 
        for i in range(5) for j in range(10)
    ]

def create_ball_at_position(x, y):
    angle = random.choice([45, 135])
    return create_ball_with_angle(x, y, angle)

def draw_bricks(screen, bricks):
    for brick in bricks:
        color = RED if brick["is_special"] else GREEN
        pygame.draw.rect(screen, color, brick["rect"])

def handle_ball_collision_with_brick(ball, bricks, score, balls):
    ball_rect = pygame.Rect(ball["x"] - ball_radius, ball["y"] - ball_radius, 2 * ball_radius, 2 * ball_radius)
    
    for brick in bricks[:]:
        if ball_rect.colliderect(brick["rect"]):
            ball["dy"] = -ball["dy"]  # 反彈
            bricks.remove(brick)  # 移除磚塊

            # 播放音效
            pop_sound.play()

            # 如果是紅色磚塊，生成兩顆球
            if brick["is_special"]:
                new_ball1 = create_ball_at_position(brick["rect"].centerx, brick["rect"].centery)
                new_ball2 = create_ball_at_position(brick["rect"].centerx, brick["rect"].centery)
                balls.append(new_ball1)
                balls.append(new_ball2)

            score += 1  # 每消除一個磚塊得10分
    
    return score

def open_settings():
    global paddle_speed, initial_balls, special_brick_chance
    
    settings_window = tk.Tk()
    settings_window.title("Settings")
    settings_window.geometry("300x300")
    
    def update_values():
        global paddle_speed, initial_balls, special_brick_chance
        paddle_speed = int(paddle_speed_var.get())
        initial_balls = int(initial_balls_var.get())
        special_brick_chance = float(special_brick_chance_var.get())
    
    def update_paddle_speed_label(val):
        paddle_speed_label.config(text=f"Paddle Speed: {int(float(val))}")
    
    def update_initial_balls_label(val):
        initial_balls_label.config(text=f"Initial Balls: {int(float(val))}")
    
    def update_special_brick_chance_label(val):
        special_brick_chance_label.config(text=f"Special Brick Chance: {float(val):.2f}")
    
    # 變數
    paddle_speed_var = tk.DoubleVar(value=paddle_speed)
    initial_balls_var = tk.DoubleVar(value=initial_balls)
    special_brick_chance_var = tk.DoubleVar(value=special_brick_chance)
    
    # 標題
    tk.Label(settings_window, text="Game Settings", font=("Arial", 14, "bold")).pack(pady=10)
    
    # 板子速度
    paddle_speed_label = tk.Label(settings_window, text=f"Paddle Speed: {int(paddle_speed)}")
    paddle_speed_label.pack()
    paddle_scale = ttk.Scale(settings_window, from_=5, to=20, variable=paddle_speed_var, 
                              orient="horizontal", command=update_paddle_speed_label)
    paddle_scale.pack(pady=5)
    
    # 初始球數
    initial_balls_label = tk.Label(settings_window, text=f"Initial Balls: {int(initial_balls)}")
    initial_balls_label.pack()
    initial_balls_scale = ttk.Scale(settings_window, from_=1, to=100, variable=initial_balls_var, 
                                     orient="horizontal", command=update_initial_balls_label)
    initial_balls_scale.pack(pady=5)
    
    # 特殊磚塊機率
    special_brick_chance_label = tk.Label(settings_window, text=f"Special Brick Chance: {special_brick_chance:.2f}")
    special_brick_chance_label.pack()
    special_brick_chance_scale = ttk.Scale(settings_window, from_=0.01, to=1, variable=special_brick_chance_var, 
                                            orient="horizontal", command=update_special_brick_chance_label)
    special_brick_chance_scale.pack(pady=5)
    
    # 確定按鈕
    ttk.Button(settings_window, text="Apply", command=lambda: [update_values(), settings_window.destroy()]).pack(pady=10)
    
    settings_window.mainloop()

# 按鈕區域
start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
settings_button = pygame.Rect(WIDTH - 120, HEIGHT - 50, 100, 40)

def draw_start_screen(screen):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 72)
    small_font = pygame.font.Font(None, 36)
    
    title_text = font.render("Hit the Bricks!", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    
    pygame.draw.rect(screen, GREEN, start_button)
    start_text = small_font.render("Start Game", True, BLACK)
    screen.blit(start_text, (start_button.x + 25, start_button.y + 10))
    
    pygame.draw.rect(screen, BLUE, settings_button)
    settings_text = small_font.render("Settings", True, WHITE)
    screen.blit(settings_text, (settings_button.x + 10, settings_button.y + 10))
    
    pygame.display.update()

def start_screen():
    running = True
    while running:
        draw_start_screen(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    running = False  # 開始遊戲
                elif settings_button.collidepoint(event.pos):
                    open_settings()

def game_loop():
    global paddle_x, ball_speed, score, level
    clock = pygame.time.Clock()
    running = True
    bricks = create_bricks()

    # 根據 initial_balls 創建初始球
    balls = [create_ball_with_angle(paddle_x + paddle_width // 2, paddle_y - ball_radius, random.choice([45, 135])) 
             for _ in range(initial_balls)]

    while running:
        screen.fill(WHITE)
        pygame.draw.rect(screen, GREEN, (paddle_x, paddle_y, paddle_width, paddle_height))

        # 繪製磚塊
        draw_bricks(screen, bricks)

        # 顯示分數
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # 顯示當前關卡
        level_text = font.render(f"Level: {level}", True, BLACK)
        screen.blit(level_text, (WIDTH - 150, 10))

        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 處理鍵盤輸入
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
            paddle_x += paddle_speed

        # 處理每顆球的移動
        for ball in balls[:]:
            ball["x"] += ball["dx"]
            ball["y"] += ball["dy"]

            # 牆壁碰撞
            if ball["x"] - ball_radius <= 0:
                ball["x"] = ball_radius
                ball["dx"] = abs(ball["dx"])
            elif ball["x"] + ball_radius >= WIDTH:
                ball["x"] = WIDTH - ball_radius
                ball["dx"] = -abs(ball["dx"])

            # 頂部牆壁碰撞
            if ball["y"] - ball_radius <= 0:
                ball["y"] = ball_radius
                ball["dy"] = abs(ball["dy"])

            # 板子碰撞
            if (paddle_x <= ball["x"] <= paddle_x + paddle_width) and \
               (paddle_y <= ball["y"] + ball_radius <= paddle_y + paddle_height):
                paddle_center = paddle_x + paddle_width / 2
                relative_intersection = (ball["x"] - paddle_center) / (paddle_width / 2)
                
                angle_factor = max(-1, min(1, relative_intersection))
                
                speed = math.sqrt(ball["dx"]**2 + ball["dy"]**2)
                ball["dx"] = speed * angle_factor
                ball["dy"] = -math.sqrt(max(0, speed**2 - ball["dx"]**2))
                
                #ball["dx"] += random.uniform(-0.1, 0.1)

            # 碰到磚塊
            score = handle_ball_collision_with_brick(ball, bricks, score, balls)

            # 如果磚塊全部消除，生成新的磚塊並進入下一關
            if len(bricks) == 0:
                bricks = create_bricks()
                level += 1  # 升級關卡
                ball_speed = min(ball_speed + 0.5, max_ball_speed)  # 每過一關增加球的速度，且不能超過最大速度

        # 檢查是否有球掉落
        balls = [ball for ball in balls if ball["y"] < HEIGHT]

        # 如果所有球都掉落，遊戲結束
        if not balls:
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("Game Over!", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 30))
            pygame.display.flip()
            pygame.time.wait(3000)  # 等待3秒
            running = False

        # 繪製每顆球
        for ball in balls:
            pygame.draw.circle(screen, GRAY, (int(ball["x"]), int(ball["y"])), ball_radius)

        # 更新螢幕
        pygame.display.update()
        clock.tick(60)  # 設定遊戲更新頻率為每秒60幀

# 執行開始畫面
start_screen()

# 開始遊戲
game_loop()

# 關閉 pygame
pygame.quit()