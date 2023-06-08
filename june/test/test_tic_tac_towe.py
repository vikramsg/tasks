from typing import List
from src.tic_tac_toe import game_loop
import pytest
from click import testing as click_testing


def test_game_play(game_moves: List[str]) -> None:
    # Given
    test_runner = click_testing.CliRunner()

    # When
    result = test_runner.invoke(game_loop, input="\n".join(game_moves))

    # Then
    assert "Game finished in a draw" in result.output


@pytest.fixture
def game_moves() -> List[str]:
    return ["o", "1,1", "0,0", "1,0", "2,1", "2,2", "0,2", "0,1", "1,2", "2,0"]
