from unittest.mock import patch
from client.repl import *


@patch("builtins.input", side_effect=["Y", "n"])
def test_get_answer(mock_input):
    assert Repl.get_answer()
    assert not Repl.get_answer()
