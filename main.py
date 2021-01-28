from pygame import *
from player import Player
from blocks import Platform, BlockDie, Exit
from monsters import Monster
from monet import Coin
from records_holder import RecordsHolder


# Объявляем переменные
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 600  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
MENU_TEXT_COLOR = (139, 0, 255)
RECORDS_TEXT_COLOR = (255, 255, 0)
GAME_BACKGROUND_COLOR = (0, 0, 0)
TILE_WIDTH = 70
TILE_HEIGHT = 70
TOTAL_LEVELS = 1  # Всего уровней

CONGRATS_BACKGROUND = image.load('blocks_sprites/original.jpg')


class Camera(object):  # класс для отображения уровня большего по размеру чем окно(эффект камеры)
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):  # функция для обьекта класса камеры
    left, top, _, _ = target_rect
    _, _, width, height = camera
    left, top = -left + WIN_WIDTH / 2, -top + WIN_HEIGHT / 2

    left = min(0, left)  # Не движемся дальше левой границы
    left = max(-(camera.width - WIN_WIDTH), left)  # Не движемся дальше правой границы
    top = max(-(camera.height - WIN_HEIGHT), top)  # Не движемся дальше нижней границы
    top = min(0, top)  # Не движемся дальше верхней границы

    return Rect(left, top, width, height)


def load_level(filename):  # загрузка уровня
    filename = "levels/" + filename
    with open(filename, 'r') as mapFile:
        return [line.strip() for line in mapFile]


def draw_pause(screen):  # рисуем паузу
    pause_font = font.Font(None, 50)
    text = pause_font.render("Пауза", True, (255, 255, 255))
    screen.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2,
                       WIN_HEIGHT // 2 - text.get_width() // 2))

    pause_font = font.Font(None, 30)
    text = pause_font.render("Esc - продолжить", True, (255, 255, 255))
    screen.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2,
                       WIN_HEIGHT // 2))


def draw_score(screen, score):
    score_font = font.Font(None, 30)
    text = score_font.render(f"Очки: {score}", True, (0, 255, 0))
    screen.blit(text, (5, 0))


def draw_intermediate_results(screen, current_level, level_score):
    score_font = font.Font(None, 60)
    text = score_font.render(f"Уровень {current_level} пройден!", True, (0, 255, 0))
    screen.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2,
                       WIN_HEIGHT // 2 - text.get_height() // 2))

    score_font = font.Font(None, 30)
    text = score_font.render(f"Набранные очки: {level_score}", True, (0, 255, 0))
    screen.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2,
                       WIN_HEIGHT // 2 + text.get_height() * 2))
    display.update()

    congrats_running = True
    while congrats_running:
        for ev in event.get():
            if ev.type == KEYDOWN and ev.key == K_ESCAPE:
                quit()
            elif ev.type == KEYDOWN and ev.key == K_RETURN:
                congrats_running = False


def draw_final_results(screen, total_score, records_holder):
    screen.blit(CONGRATS_BACKGROUND, (0, 0))

    total_score_font = font.Font(None, 60)
    text = total_score_font.render("Вы успешно прошли все уровни!", True, (0, 255, 0))
    screen.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2,
                       WIN_HEIGHT // 2 - text.get_height() // 2))

    score_font = font.Font(None, 30)
    text = score_font.render(f"Набранные очки за все уровни: {total_score}", True, (0, 255, 0))
    screen.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2,
                       WIN_HEIGHT // 2 + text.get_height() * 2))

    score_font = font.Font(None, 30)
    text = score_font.render("Введите имя: ", True, (0, 255, 255))
    screen.blit(text, (30, 540))

    draw.rect(screen, (0, 0, 0), (45 + text.get_width(), 530, 130, 30))

    nickname = ''
    congrats_running = True
    while congrats_running:
        for ev in event.get():
            if ev.type == QUIT:
                quit()
            elif ev.type == KEYDOWN and ev.key == K_RETURN:
                congrats_running = False
            elif ev.type == KEYDOWN and len(nickname) < 10 and ev.key != K_BACKSPACE:
                nickname += ev.unicode
        text = score_font.render(nickname, True, (255, 255, 255))
        screen.blit(text, (190, 540))
        display.update()
    records_holder.add_new_record([nickname, total_score])


def open_menu(screen, records_holder):
    screen.fill((0, 0, 0))
    menu_font = font.Font(None, 70)
    text = menu_font.render("Trump The Legend", True, Color(MENU_TEXT_COLOR))
    screen.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2,
                       WIN_HEIGHT // 2 - text.get_height() * 2))

    menu_font = font.Font(None, 40)
    text = menu_font.render("Играть", True, Color(MENU_TEXT_COLOR))
    screen.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2,
                       WIN_HEIGHT // 2 - text.get_height() // 2))
    play_btn_rect = (WIN_WIDTH // 2 - text.get_width() // 2,
                     WIN_HEIGHT // 2 - text.get_height() // 2,
                     text.get_width(), text.get_height())

    menu_font = font.Font(None, 40)
    text = menu_font.render("Таблица рекордов", True, Color(MENU_TEXT_COLOR))
    screen.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2,
                       WIN_HEIGHT // 2 + text.get_height()))
    records_btn_rect = (WIN_WIDTH // 2 - text.get_width() // 2,
                        WIN_HEIGHT // 2 + text.get_height(),
                        text.get_width(), text.get_height())

    menu_running = True
    while menu_running:
        for ev in event.get():
            if ev.type == QUIT:
                quit()
            elif ev.type == MOUSEBUTTONDOWN\
                    and play_btn_rect[0] <= ev.pos[0] <= play_btn_rect[0] + play_btn_rect[2]\
                    and play_btn_rect[1] <= ev.pos[1] <= play_btn_rect[1] + play_btn_rect[3]:
                menu_running = False
            elif ev.type == MOUSEBUTTONDOWN\
                    and records_btn_rect[0] <= ev.pos[0] <= records_btn_rect[0] + records_btn_rect[2]\
                    and records_btn_rect[1] <= ev.pos[1] <= records_btn_rect[1] + records_btn_rect[3]:
                open_records_table(screen, records_holder)
                menu_running = False
        display.update()


def open_records_table(screen, records_holder):
    screen.fill((0, 0, 0))
    records_font = font.Font(None, 70)
    text = records_font.render("Таблица рекордов:", True, Color(MENU_TEXT_COLOR))
    screen.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2,
                       WIN_HEIGHT // 20))

    records_font = font.Font(None, 50)
    for i in range(10):
        text = records_font.render(" ".join(records_holder.records[i]), True, Color(RECORDS_TEXT_COLOR))
        screen.blit(text, (WIN_WIDTH // 5,
                           WIN_HEIGHT // 12 + text.get_height() * 1.4 * (i + 1)))

    records_font = font.Font(None, 40)
    text = records_font.render("Выйти", True, Color(MENU_TEXT_COLOR))
    screen.blit(text, (WIN_WIDTH // 20,
                       WIN_HEIGHT // 2 + text.get_height() * 9))
    back_btn_rect = (WIN_WIDTH // 20, WIN_HEIGHT // 2 + text.get_height() * 9, text.get_width(), text.get_height())

    records_running = True
    while records_running:
        for ev in event.get():
            if ev.type == QUIT:
                quit()
            elif ev.type == MOUSEBUTTONDOWN and back_btn_rect[0] <= ev.pos[0] <= back_btn_rect[0] + back_btn_rect[2]\
                    and back_btn_rect[1] <= ev.pos[1] <= back_btn_rect[1] + back_btn_rect[3]:
                records_running = False
                open_menu(screen, records_holder)
        display.update()


def main():
    init()
    screen = display.set_mode(DISPLAY)
    display.set_caption("Trump The Legend")  # Пишем в шапку

    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание заднего фона

    records_holder = RecordsHolder()
    open_menu(screen, records_holder)

    bg.fill(Color(GAME_BACKGROUND_COLOR))  # Заливаем фон сплошным цветом

    current_level = -1  # уровень на данный момент (!!!)
    hero = Player(70, 70)  # создаем героя по (x,y) координатам

    while current_level < TOTAL_LEVELS - 1:

        current_level += 1

        left = right = False  # по умолчанию — стоим
        up = False
        is_on_pause = False  # проверка на паузу

        entities = sprite.Group()  # Все объекты
        obstacles = []  # то, во что мы будем врезаться или опираться
        coins = []  # список для монет
        exits = []  # список для выходов
        monsters = sprite.Group()  # все монстры

        entities.add(hero)

        levels = [load_level(f'level{i + 1}.txt') for i in range(TOTAL_LEVELS)]

        x = y = 0  # координаты
        for row in levels[current_level]:  # вся строка
            for col in row:  # каждый символ
                if col == "-":  # знак для платформ
                    pf = Platform(x, y)
                    entities.add(pf)
                    obstacles.append(pf)
                elif col == "*":  # для шипов
                    bd = BlockDie(x, y)
                    entities.add(bd)
                    obstacles.append(bd)
                elif col == "m":  # для монет
                    mn = Coin(x, y)
                    entities.add(mn)
                    coins.append(mn)
                elif col == "e":  # для монстров
                    en = Monster(x, y)
                    entities.add(en)
                    obstacles.append(en)
                    monsters.add(en)
                elif col == "!":  # для выходов
                    ex = Exit(x, y)
                    entities.add(ex)
                    exits.append(ex)
                elif col == "h":  # для героя
                    hero.teleporting(x, y)

                x += TILE_WIDTH  # блоки платформы ставятся на ширине блоков
            y += TILE_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля

        total_level_width = len(levels[current_level][0]) * TILE_WIDTH  # Высчитываем фактическую ширину уровня
        total_level_height = len(levels[current_level]) * TILE_HEIGHT  # высоту

        camera = Camera(camera_configure, total_level_width, total_level_height)
        timer = time.Clock()

        running = True
        while running:  # Основной цикл программы
            timer.tick(30)  # fps
            monsters.update(obstacles)

            for e in event.get():  # Обрабатываем события
                if e.type == QUIT:
                    running = False
                    quit()
                if e.type == KEYDOWN and e.key == K_UP:
                    up = True
                if e.type == KEYUP and e.key == K_UP:
                    up = False

                if e.type == KEYDOWN and e.key == K_LEFT:
                    left = True
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    right = True

                if e.type == KEYUP and e.key == K_RIGHT:
                    right = False
                if e.type == KEYUP and e.key == K_LEFT:
                    left = False

                if e.type == KEYDOWN and e.key == K_ESCAPE:  # Esc - управляющая клавиша паузы
                    is_on_pause = 1 - is_on_pause
                    for obj in obstacles:  # останавливаем всех монстров в зависимости от состояния
                        if obj.__class__ == Monster:
                            obj.stop(is_on_pause)

            screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
            if not is_on_pause:
                hero.update(left, right, up, obstacles, coins, levels[current_level])  # передвижение
                camera.update(hero)
            for e in entities:
                screen.blit(e.image, camera.apply(e))
            if is_on_pause:
                draw_pause(screen)

            if hero.exited(exits):
                running = False

            if running:
                draw_score(screen, hero.level_scores)

            display.update()  # обновление и вывод всех изменений на экран

        draw_intermediate_results(screen, current_level + 1, hero.level_scores)
        hero.zeroize_level_score()

    draw_final_results(screen, hero.total_scores, records_holder)


if __name__ == "__main__":
    main()
