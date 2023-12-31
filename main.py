import pygame
import math

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
weapon_height = weapon_size[1]

# 무기는 한 번에 여러 발 발사 가능
weapons = []


# 무기 이동 속도, 
weapon_speed = 10

# 총 회전 각도 변수
gun_rotation_angle = 0
gun_rotation_angles = []
gun_rotation_speed = 45
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

# 사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

# Font 정의
game_font = pygame.font.Font(None, 40)
total_time = 90
start_ticks = pygame.time.get_ticks() # 시작 시간 정의

# 게임 종료 메시지 / TimeOut, Mission Complete, Game Over
game_result = "Game Over"
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
                if used_gun: # 총기 사용 가능일 때
                    gun_rotation_angle += gun_rotation_speed # 30만큼 시계 방향으로
            elif event.key == pygame.K_DOWN:
                to_y += character_speed
                if used_gun: # 총기 사용 가능일 때
                    gun_rotation_angle -= gun_rotation_speed # 30만큼 시계 방향으로
            elif event.key == pygame.K_SPACE: # 무기 발사
                if used_gun != True:
                    print("G키를 눌러 총을 드세요!")
                else:
                    print("빵!")
                    weapon_x_pos = gun_x_pos + (gun_width / 2) - (weapon_width / 2) + math.cos(math.radians(gun_rotation_angle)) * (gun_width / 2)
                    weapon_y_pos = gun_y_pos + (gun_height / 2) - (weapon_height / 2) - math.sin(math.radians(gun_rotation_angle)) * (gun_width / 2)
                    gun_rotation_angles.append(gun_rotation_angle)
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
        gun_x_pos = 0 + character_width / 2
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
        gun_x_pos = screen_width - character_width + 13

    #위, 아래쪽 경계 정하기
    if character_y_pos < screen_height - character_height - stage_height:
        character_y_pos = screen_height - character_height - stage_height
    elif character_y_pos > screen_height - character_height - stage_height:
        character_y_pos = screen_height - character_height - stage_height
    weapons_to_remove = []
    # 무기 위치 조정
    for w_idx, w in enumerate(weapons):
        print("{0}도".format(gun_rotation_angle))
        weapon_xd = math.sin(math.radians(gun_rotation_angles[w_idx]+90)) * weapon_speed
        weapon_yd = math.cos(math.radians(gun_rotation_angles[w_idx]+90)) * weapon_speed
        w[0] += weapon_xd
        w[1] += weapon_yd 
        if w[1] < 0: # 천장에 닿았을 때
            weapons_to_remove.append(w_idx)
        elif w[1] > screen_height - stage_height: # 스테이지에 닿았을 때
            weapons_to_remove.append(w_idx)
        elif w[0] < 0:
            weapons_to_remove.append(w_idx)
        elif w[0] > screen_width:
            weapons_to_remove.append(w_idx)
        
        #     print("조건1")
        # if ((w[1] < screen_height - stage_height) and (0 < w[0] < screen_width - weapon_width)): 
        #     weapons_to_remove.append(w_idx)
        #     print("조건2")
        # weapons = [[w[0], w[1] - weapon_speed] for w in weapons] # 무기 위치를 위로 올림
    #     # 천장에 닿은 무기 없애기 
    # weapons = [[w[0], w[1]] for w in weapons if w[1]  > 0] 
    # weapons = [[w[0], w[1]] for w in weapons if ]
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

    
    # 충돌 처리

    # 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        # 공 rect 정보 업데이트
        ball_rect = ball_imgs[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y
        
        if "split_cooldown" in ball_val:
            continue
        # 공과 캐릭터 충돌 처리
        if character_rect.colliderect(ball_rect):
            running = False
            print("님 죽음 ㅋ")
            break
        # 공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # 해당 무기 없애기 위한 값
                ball_to_remove = ball_idx # 해당 공 없애기 위한 값
                # 가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기
                if ball_img_idx < 3:
                    # 현재 공 크기 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보
                    small_ball_rect = ball_imgs[ball_img_idx + 1].get_rect()
                    smal_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]
                    # 왼쪽으로 튕겨 나가는 작은 공
                    balls.append({
                    "pos_x" : ball_pos_x + (ball_width / 2) - (smal_ball_width / 2), # 공의 x좌표
                    "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # 공의 y좌표
                    "img_idx": ball_img_idx + 1, # 공의 이미지 인데스
                    "to_x": -3, # x축 이동 방향
                    "to_y": -6, # y축 이동 방향
                    "init_spd_y": ball_speed_y[ball_img_idx + 1], })

                    # 오른쪽으로 튕겨 나가는 작은 공
                    balls.append({
                    "pos_x" : ball_pos_x + (ball_width / 2) - (smal_ball_width / 2), # 공의 x좌표
                    "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # 공의 y좌표
                    "img_idx": ball_img_idx + 1, # 공의 이미지 인데스
                    "to_x": 3, # x축 이동 방향
                    "to_y": -6, # y축 이동 방향
                    "init_spd_y": ball_speed_y[ball_img_idx + 1],}) 
                break
        else: # 계속 게임을 진행
            continue # 안쪽 for 문 조건이 맞이 않으면 continue, 바깥 for 문 계속 수행
        break # 안쪽 for 문에서 break만나면 여기로 진입 가능, 2중 문을 한 번에 탈출
    # 충돌된 공 or 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1
    # 모든 공을 없앤 경우 게임 종료
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False
    # 새로 생성된 공들에 대한 쿨다운 확인
    for ball_idx, ball_val in enumerate(balls):
        if "split_cooldown" in ball_val:
            ball_val["split_cooldown"] -= dt
            if ball_val["split_cooldown"] <= 0:
                    del ball_val["split_cooldown"]

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
        gun_rotated_image = pygame.transform.rotate(gun, gun_rotation_angle)
        # gun_rotated_rect = gun_rotated_image.get_rect(center=(gun_x_pos + gun_width / 2, gun_y_pos + gun_height / 2))
        # screen.blit(gun_rotated_image, (gun_x_pos, gun_y_pos))
        screen.blit(gun_rotated_image, (gun_x_pos + gun_width / 2 - gun_rotated_image.get_width() / 2,
        gun_y_pos + gun_height / 2 - gun_rotated_image.get_height() / 2))

        # screen.blit(gun, (gun_x_pos, gun_y_pos))
     
    for idx in reversed(weapons_to_remove):
        print("없앨 공", idx)
        del weapons[idx]
        del gun_rotation_angles[idx]

    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> s
    timer = game_font.render("Time : {0}".format(int(total_time - elapsed_time)), True, (0,0,0))
    screen.blit(timer, (10, 10))

    # 시간 초과했다면
    if total_time - elapsed_time <= 0:
        game_result = "Time_Over"
        running = False
    pygame.display.update()

# 게임 오버 메시지
msg = game_font.render(game_result, True, (255,255,0))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()
# 2초 대기
pygame.time.delay(2000)
# 파이게임 종료
pygame.quit()