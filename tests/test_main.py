import pytest
from unittest.mock import patch
from src.main import main

def test_main_exit(capsys):
    """Выход"""
    with patch('builtins.input', return_value='0'):
        main()
    captured = capsys.readouterr()
    assert "выход из программы" in captured.out.lower()