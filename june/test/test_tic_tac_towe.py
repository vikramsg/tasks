from typing import List
from src.tic_tac_toe import game_loop
import pytest
from click import testing as click_testing


@pytest.mark.parametrize(
    "moves, expected_msg",
    [
        (
            ["o", "1,1", "0,0", "1,0", "2,1", "2,2", "0,2", "0,1", "1,2", "2,0"],
            "Game finished in a draw",
        ),
        (
            ["x", "0,0", "1,1", "1,2", "1,0", "0,1", "0,2", "2,1", "2,0"],
            "Game over. Player o won.",
        ),
        (
            ["o", "2,1", "1,0", "2,2", "0,1", "2,0"],
            "Game over. Player x won.",
        ),
    ],
)
def test_game_play(moves: List[str], expected_msg) -> None:
    # Given
    test_runner = click_testing.CliRunner()

    # When
    result = test_runner.invoke(game_loop, input="\n".join(moves))

    # Then
    assert expected_msg in result.output
