import pygame as pg;
import os;
from enum import Enum;

class Pytris:
    def __init__(self):
        pg.init();
        self.screen = pg.display.set_mode([300, 600]);
        self.running = True;
        self.clock = pg.time.Clock();

        self.__setup();
        self.__play();
        pg.quit();

    def __setup(self):
        # TODO temp testing
        self.test_tet = Tetromino(TetrominoType.I);
        # TODO add more stuff I think

    def __play(self):
        while self.running:
            # Read events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False;

            # TODO temp testing
            self.test_tet.draw(self.screen);

            # Update Logic
            pg.display.flip();
            self.clock.tick(60);

# Sprites won't be changing images, so we can use them through Enum
class TetrominoType(Enum):
    # TODO switch to each image
    I = pg.image.load(os.path.join('assets', 'Tetrominos.png'));
    O = pg.image.load(os.path.join('assets', 'Tetrominos.png'));
    L = pg.image.load(os.path.join('assets', 'Tetrominos.png'));
    J = pg.image.load(os.path.join('assets', 'Tetrominos.png'));
    S = pg.image.load(os.path.join('assets', 'Tetrominos.png'));
    Z = pg.image.load(os.path.join('assets', 'Tetrominos.png'));
    T = pg.image.load(os.path.join('assets', 'Tetrominos.png'));

class Tetromino(pg.sprite.Sprite):
    def __init__(self, tetromino_type: TetrominoType):
        self.type = tetromino_type;
        self.image = tetromino_type.value.convert_alpha();
        # TODO most likely needs adjustment
        self.rect = self.image.get_rect();
        self.rect.centerx = 150;
        self.rect.centery = 300;

    def draw(self, screen):
        screen.blit(self.image, self.rect);

game: Pytris = Pytris();
