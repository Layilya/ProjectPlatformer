import pytest
import pygame
from Game_main123 import *

@pytest.fixture
def snake():
    return Snake()

def test_snake_initial_position(snake):
    assert snake.rect.x == 20
    assert snake.rect.y == 0

def test_snake_image_loading(snake):
    assert isinstance(snake.image, pygame.Surface)

def test_snake_image_size(snake):
    assert snake.image.get_width() == 100
    assert snake.image.get_height() == 100
