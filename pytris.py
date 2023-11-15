import pygame as pg;
from pygame import Vector2;
from tetromino import Tetromino, TetrominoType;

class Pytris:
    def __init__(self):
        pg.init();
        self.screen = pg.display.set_mode([300, 600]);
        self.clock = pg.time.Clock();

        self.game_array = [[0 for col in range(10)] for row in range(20)]
        self.falling_tetromino = None;
        self.running = True;

        self.__setup();
        self.__play();
        pg.quit();

    def __setup(self):
        self.falling_tetromino = Tetromino(TetrominoType.I);

    def __play(self):
        while self.running:
            # Read events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False;

            # TODO read slide inputs
            # TODO read rotation inputs

            # Update Logic
            self.falling_tetromino.fall();
            pg.display.flip();
            self.clock.tick(60);

    def output_grid(self):
        output = list(self.game_array);
        tet = self.falling_tetromino.shape;
        for row in range(len(tet)):
            for cell in  
        for block_row in tet:
            for block in block_row 
        print(output);


