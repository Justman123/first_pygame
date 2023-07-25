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
background = pygame.image.load("pygame_project/images/background.png")

# 스테이지 만들기
stage = pygame.image.load("pygame_project/images/stage.png")
stage_size = stage.get_rect().size
stage_height = stage_size[1]

#캐릭터 만들기
character = pygame.image.load("pygame_project/images/character.png")
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
gun = pygame.image.load("pygame_project/images/gun.png")
gun_size = gun.get_rect().size
gun_width = gun_size[0]
gun_height = gun_size[1]
gun_x_pos = character_x_pos + character_width / 2
gun_y_pos = character_y_pos + character_height / 2

# 무기 (발사 구현용)
weapon = pygame.image.load("pygame_project/images/weapon.png")
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한 번에 여러 발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 10

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
                weapon_x_pos = character_x_pos + character_width / 2

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
    screen.blit(background, (0, 0))
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    if (used_gun == True):
        screen.blit(gun, (gun_x_pos, gun_y_pos))
    pygame.display.update()


# 파이게임 종료
pygame.quit()