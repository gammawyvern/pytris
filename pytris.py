import pygame as pg;
from tetromino import Tetromino, TetrominoType;

class Pytris:
    def __init__(self):
        pg.init();
        self.screen = pg.display.set_mode([300, 600]);
        self.clock = pg.time.Clock();

        self.running = True;

        self.game_array = [[0 for col in range(10)] for row in range(20)]
        for row in self.game_array:
            print(row);

        self.__setup();
        self.__play();
        pg.quit();

    def __setup(self):
        self.test_tet = Tetromino(TetrominoType.I);

    def __play(self):
        while self.running:
            # Read events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False;

            # Update Logic
            pg.display.flip();
            self.clock.tick(60);

