import pathlib

from sneks.core.cell import Cell
from sneks.core.direction import Direction
from sneks.engine import registrar
from sneks.interface.snek import Snek
from sneks.validator import main


def get_prefix():
    return pathlib.Path(main.path_to_test)


def test_import():
    submission_files = registrar.get_submission_files(get_prefix())
    print(submission_files)
    assert 1 == len(submission_files)
    name = registrar.get_submission_name(get_prefix())
    assert get_prefix().parts[-1] == name
    registrar.load_module(get_prefix())


def test_class_exists():
    _, snek = registrar.get_custom_snek(get_prefix())
    assert issubclass(snek, Snek)


def test_basic_functionality():
    _, snek_class = registrar.get_custom_snek(get_prefix())
    snek = snek_class()
    snek.food = [Cell(0, 0)]
    snek.body = [Cell(1, 1)]
    assert snek.get_next_direction() in Direction
