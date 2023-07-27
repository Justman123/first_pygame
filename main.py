import pygame

# 파이 게임 초기화
pygame.init()

# 화면 크기 설정
screen_height = 744
screen_width = 1022
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Pang!")

# 배경 만들기
background = pygame.image.load("images/background.png")

# 스테이지 만들기
stage = pygame.image.load("images/stage.png")
stage_size = stage.get_rect().size
stage_height = stage_size[1]

#캐릭터 만들기
character = pygame.image.load("images/character.png")
character_size = character.get_rect().size #캐릭터 이미지 사이즈 구하기
character_width = character_size[0] #캐릭터 가로 크기
character_height = character_size[1] #캐릭터 세로 크기
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height 

# 이동 속도 
character_speed = 0.5

# 이동 좌표
to_x = 0
to_y = 0
# 무기 (플레이어용)
gun = pygame.image.load("images/gun.png")
gun_size = gun.get_rect().size
gun_width = gun_size[0]
gun_height = gun_size[1]
gun_x_pos = character_x_pos + character_width / 2
gun_y_pos = character_y_pos + character_height / 2

# 무기 (발사 구현용)
weapon = pygame.image.load("images/weapon.png")
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한 번에 여러 발 발사 가능
weapons = []


# 무기 이동 속도
weapon_speed = 10

# 공 만들기 (4개 크기에 대해 따로 처리)
ball_imgs = [pygame.image.load("images/balloon1.png"),
             pygame.image.load("images/balloon2.png"),
             pygame.image.load("images/balloon3.png"),
             pygame.image.load("images/balloon4.png")]

# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9] # index 0,1,2,3에 해당하는 값

# 공들
balls = []

balls.append({
    "pos_x" : 50, # 공의 x좌표
    "pos_y": 50, # 공의 y좌표
    "img_idx": 0, # 공의 이미지 인데스
    "to_x": 3, # x축 이동 방향
    "to_y": -6, # y축 이동 방향
    "init_spd_y": ball_speed_y[0]}) # 최초 이동 속도
# FPS 설정
clock = pygame.time.Clock()


# 이벤트 루프
running = True
used_gun = False
while running:
    dt = clock.tick(60)
    for event in pygame.event.get(): # 이벤트 감지
        if event.type == pygame.QUIT: # 종료 이벤트
            running = False
        if event.type == pygame.KEYDOWN: # 키 누름 이벤트
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed
            elif event.key == pygame.K_UP:
                to_y -= character_speed
            elif event.key == pygame.K_DOWN:
                to_y += character_speed
            elif event.key == pygame.K_SPACE: # 무기 발사
                if used_gun != True:
                    print("G키를 눌러 총을 드세요!")
                else:
                    print("빵!")
                    weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                    weapon_y_pos = character_y_pos
                    weapons.append([weapon_x_pos, weapon_y_pos])

            elif event.key == pygame.K_g:
                if used_gun == True:
                    used_gun = False
                else:
                    used_gun = True
        if event.type == pygame.KEYUP: # 키 뗌 이벤트
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0
            elif event.key == pygame.K_SPACE:
                pass
    character_x_pos += to_x * dt
    character_y_pos += to_y * dt
    gun_x_pos += to_x * dt

    #왼쪽, 오른쪽 경계 정하기
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    #위, 아래쪽 경계 정하기
    if character_y_pos < screen_height - character_height - stage_height:
        character_y_pos = screen_height - character_height - stage_height
    elif character_y_pos > screen_height - character_height - stage_height:
        character_y_pos = screen_height - character_height - stage_height

    # 무기 위치 조정
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons] # 무기 위치를 위로 올림
    # 천장에 닿은 무기 없애기
    weapons = [[w[0], w[1]] for w in weapons if w[1]  > 0] 

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        
        ball_size = ball_imgs[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]
        # 가로벽에 닿았을 때 공 이동 위치 변경 (튕겨 나오는 효과)
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1
        # 세로 처리
        # 스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else: # 그 외의 모든 경우에는 아래 방향으로 힘 작용
            ball_val["to_y"] += 0.5
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]
    # 화면에 그리기
    screen.blit(background, (0, 0))
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_imgs[ball_img_idx], (ball_pos_x, ball_pos_y))
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    if (used_gun == True):
        screen.blit(gun, (gun_x_pos, gun_y_pos))
    pygame.display.update()


# 파이게임 종료
pygame.quit()