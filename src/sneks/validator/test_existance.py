from sneks.engine import registrar
from sneks.interface.snek import Snek
from sneks.validator import main


def test_import():
    submission_files = registrar.get_submission_files(main.get_prefix())
    print(submission_files)
    assert 1 == len(submission_files)
    name = registrar.get_submission_name(main.get_prefix())
    assert main.get_prefix().parts[-1] == name
    registrar.load_module(main.get_prefix())


def test_class_exists():
    _, snek = registrar.get_custom_snek(main.get_prefix())
    assert issubclass(snek, Snek)
