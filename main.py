import pygame
import random
import math
pygame.init()
# Ustawienia ekranu
width, height = 626, 459
screen = pygame.display.set_mode((width, height))
# Wczytanie obrazka tła
background = pygame.image.load('ce3eaae4075199a4b26401742612cb72.jpg')

class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('soldier.png')  # Wczytanie obrazka
        self.image = pygame.transform.scale(self.image, (50, 50))  # Zmiana rozmiaru obrazka
        self.rect = self.image.get_rect()
        self.x = float(x)  # Pozycja x jako wartość zmiennoprzecinkowa
        self.y = float(y)  # Pozycja y jako wartość zmiennoprzecinkowa
        self.alive = True  # Nowy atrybut wskazujący, czy zombie jest żywe
        self.hit = False  # Nowy atry
        self.live=3
soldier=Soldier(626//2,459//2)
bullets = pygame.sprite.Group()
class Bullet(pygame.sprite.Sprite): #Definiujemy klasę Bullet, która dziedziczy po klasie Sprite z biblioteki Pygame.
    # Klasa Sprite jest podstawową klasą dla wszystkich obiektów, które mają być rysowane na ekranie.
    def __init__(self, x, y): #To jest konstruktor klasy Bullet. Przyjmuje dwa argumenty: x i y, które reprezentują początkową pozycję pocisku.
        super().__init__() #Wywołujemy konstruktor klasy nadrzędnej (Sprite), aby zainicjować wszystkie potrzebne atrybuty i metody.
        self.image = pygame.Surface((5, 10)) #Tworzymy nową powierzchnię o wymiarach 5x10 pikseli. Ta powierzchnia reprezentuje obraz pocisku.
        self.image.fill((255, 255, 0))  # Żółty kolor
        self.rect = self.image.get_rect() #Tworzymy prostokątny obszar (rect), który reprezentuje pozycję i rozmiar obrazu pocisku.
        self.rect.centerx = x #Ustawiamy środek prostokąta w osi x na wartość x.
        self.y = y  # Pozycja y jako wartość zmiennoprzecinkowa
    def update(self): #Definiujemy metodę update, która jest wywoływana w każdej klatce, aby zaktualizować stan pocisku.
        self.y -= 0.3  # Aktualizacja pozycji y
        self.rect.y = int(self.y)  # Zaokrąglamy y do najbliższego całkowitego piksela i ustawiamy to jako pozycję y prostokąta.
        # Pygame używa pikseli jako jednostki do rysowania na ekranie, więc musimy zaokrąglić do najbliższego piksela.
        if self.rect.bottom < 0: #Jeśli dolna krawędź prostokąta jest mniejsza od 0 (co oznacza, że pocisk opuścił ekran), wywołujemy metodę kill, która usuwa pocisk.
            self.kill()
bullet_timer = 0
bullet_delay = 500
zombies = pygame.sprite.Group()

# Timer dla zombie
zombie_timer = 0
zombie_delay = 2000  # Czas w milisekundach między pojawianiem się zombie
max_zombies = 7
zombie_delay = 1000  #
class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('zombie.png')  # Wczytanie obrazka zombie
        self.image = pygame.transform.scale(self.image, (50, 50))  # Zmiana rozmiaru obrazka
        self.rect = self.image.get_rect()
        self.x = float(x)  # Pozycja x jako wartość zmiennoprzecinkowa
        self.y = float(y)  # Pozycja y jako wartość zmiennoprzecinkowa
        self.alive = True  # Nowy atrybut wskazujący, czy zombie jest żywe
        self.hit = False  # Nowy atrybut wskazujący, czy zombie zostało trafione
        self.soldier_hit=False
        self.hit_time = 0  # Inicjalizacja czasu trafienia
        self.attack_time = 0  # Inicjalizacja czasu ataku

    def update(self, soldier_x, soldier_y):
        if self.alive and not self.hit:  # Aktualizacja pozycji zombie tylko jeśli jest żywe i nie zostało trafione
            # Obliczenie wektora kierunku w stronę żołnierza
            dir_x = soldier_x - self.x
            dir_y = soldier_y - self.y
            dir_length = math.sqrt(dir_x ** 2 + dir_y ** 2) + 0.0001  # Dodanie małej stałej, aby zapobiec dzieleniu przez zero
            dir_x /= dir_length
            dir_y /= dir_length

            # Przesunięcie zombie w kierunku żołnierza
            self.x += dir_x * 0.08
            self.y += dir_y * 0.08

            # Aktualizacja rect dla rysowania
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)
        elif self.hit and pygame.time.get_ticks() - self.hit_time > 2000:  # Jeśli zombie zostało trafione i upłynęły 2 sekundy
            self.kill()  # Usunięcie zombie
class Hearth(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('hearth.png')  # Wczytanie obrazk
        self.image = pygame.transform.scale(self.image, (30, 30))  # Zmiana rozmiaru obrazka
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
hearths=pygame.sprite.Group()
heart_delay=5000
heart_timer=0

def check_bullet_zombie_collisions(bullets, zombies):
    # Sprawdzenie, czy jakiekolwiek pociski zderzyły się z zombie
    # Ale rozważamy tylko zombie, które są jeszcze żywe
    alive_zombies = [zombie for zombie in zombies if zombie.alive]
    collisions = pygame.sprite.groupcollide(bullets, alive_zombies, True, False)
    # Dla każdego pocisku, który trafił
    for zombies_hit in collisions.values():
        # Dla każdego zombie, które zostało trafione
        for zombie in zombies_hit:
            # Zmiana obrazka zombie na zmarla wersje
            zombie.image = pygame.image.load('death_zombie.png')  # Wczytanie czerwonego obrazka zombie
            zombie.image = pygame.transform.scale(zombie.image, (50, 50))  # Zmiana rozmiaru obrazka
            zombie.alive = False  # Ustawienie zombie jako nieżywe
            zombie.hit = True  # Ustawienie zombie jako trafione
            zombie.hit_time = pygame.time.get_ticks()
def check_soldier_zombie_collisions(soldier, zombies):
    for zombie in zombies:
        if not zombie.hit and soldier.rect.colliderect(zombie.rect) and pygame.time.get_ticks() - zombie.attack_time > 2000:
            soldier.live -= 1
            zombie.soldier_hit = True  # Zaznacz zombie jako trafione
            zombie.hit_time = pygame.time.get_ticks()  # Zaktualizuj czas trafienia
            zombie.attack_time = pygame.time.get_ticks()  # Zaktualizuj czas ataku
            if soldier.live==0:
                soldier.image=pygame.image.load('death_body.png')
                soldier.image = pygame.transform.scale(soldier.image, (50, 50))
def check_soldier_hearth_collisions(soldier,hearths):
    collisions=pygame.sprite.spritecollide(soldier,hearths,True)
    for heart in collisions:
        soldier.live+=1




font = pygame.font.Font(None, 36)  # Utworzenie czcionki (None oznacza domyślną czcionkę, 36 to rozmiar)
game_over_font = pygame.font.Font(None, 100)  # Utworzenie czcionki (None oznacza domyślną czcionkę, 500 to rozmiar)
end_text = game_over_font.render("Koniec gry", True, (255,0,0))  # Użyj game_over_font zamiast font
text_rect = end_text.get_rect(center=(width / 2, height / 2))
continue_font = pygame.font.Font(None, 50)  # Utwórz nową czcionkę o rozmiarze 50
continue_text = continue_font.render("Naciśnij spację, aby kontynuować", True, (255,0,0))
continue_text_rect = continue_text.get_rect(center=(width / 2, height / 2 + 100))
def reset_game():
    # Resetuj stan gry do stanu początkowego
    soldier.live = 3
    soldier.x=626//2
    soldier.y=459//2# Przywróć zdrowie żołnierza
    zombies.empty()  # Usuń wszystkie zombie
    bullets.empty()
    soldier.image = pygame.image.load('soldier.png')
    soldier.image = pygame.transform.scale(soldier.image, (50, 50))

game_over=False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_SPACE:  # Jeśli gra jest zakończona i gracz naciska spację, zresetuj grę
                reset_game()
                game_over = False
            if event.key == pygame.K_SPACE and pygame.time.get_ticks() - bullet_timer > bullet_delay:  # Naciśnij SPACJĘ, aby strzelać
                bullet = Bullet(soldier.x + 31, soldier.y)
                bullets.add(bullet)
                bullet_timer = pygame.time.get_ticks()
    if pygame.time.get_ticks() - zombie_timer > zombie_delay and len(zombies) < max_zombies:
        side = random.choice(['top', 'left', 'right'])  # Losowo wybierz stronę
        if side == 'top':
            x = random.randrange(width)
            y = 0
        elif side == 'left':
            x = 0
            y = random.randrange(height)
        elif side == 'right':
            x = width
            y = random.randrange(height)
        zombie = Zombie(x, y)  # Zombie pojawia się na wybranej stronie ekranu
        zombies.add(zombie)
        zombie_timer = pygame.time.get_ticks()
    if pygame.time.get_ticks()-heart_timer> heart_delay:
        hp=Hearth(random.randrange(width),random.randrange(height))
        hearths.add(hp)
        heart_timer=pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        soldier.x -= 0.2
    if keys[pygame.K_RIGHT]:
        soldier.x += 0.2
    if keys[pygame.K_UP]:
        soldier.y -= 0.2
    if keys[pygame.K_DOWN]:
        soldier.y += 0.2
    # Zapewnienie, że zolnierz nie opuści ekranu
    soldier.x = max(min(soldier.x, width - soldier.rect.width), 0)
    soldier.y = max(min(soldier.y, height - soldier.rect.height), 0)

    # Aktualizacja pozycji rect żołnierza
    soldier.rect.topleft = (soldier.x, soldier.y)

    screen.blit(background, (0, 0))  # Rysowanie tła
    screen.blit(soldier.image, (soldier.x, soldier.y))  # Rysowanie zolnierza
    lives_text = font.render(f'ZYCIE: {soldier.live}', True, (255, 255, 255))  # Utworzenie powierzchni z tekstem
    if game_over:
        continue
    if soldier.live == 0:
        screen.blit(end_text, text_rect)
        screen.blit(continue_text,continue_text_rect)
        game_over = True
    screen.blit(lives_text, (10, 10))  # Wyświetlenie tekstu na ekranie
    bullets.update()
    for zombie in zombies:
        zombie.update(soldier.x, soldier.y)
    for bullet in bullets:
        screen.blit(bullet.image, bullet.rect)
    for zombie in zombies:
        screen.blit(zombie.image, zombie.rect)
    for hearth in hearths:
        screen.blit(hearth.image,hearth.rect)
    check_bullet_zombie_collisions(bullets, zombies)
    check_soldier_zombie_collisions(soldier,zombies)
    check_soldier_hearth_collisions(soldier,hearths)
    pygame.display.flip()  # Aktualizacja ekranu
pygame.quit()




