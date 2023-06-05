from typing import Optional, Tuple
import click
import numpy as np
from functools import partial

_PLAYER_TO_NUMBER = {"o": 1, "x": 2}
_NEXT_PLAYER = {"o": "x", "x": "o"}


def _convert_to_tic_tac_toe_input(
    value: str, game_board: np.array
) -> Optional[Tuple[int, int]]:
    try:
        values = value.split(",")
        tuple_values = (int(values[0]), int(values[1]))

        assert tuple_values[0] >= 0 and tuple_values[0] < 3
        assert tuple_values[1] >= 0 and tuple_values[1] < 3

        try:
            assert game_board[tuple_values] == 0
        except AssertionError:
            raise AssertionError("Position already occupied. Chose different position")

        return tuple_values
    except ValueError:
        raise click.BadParameter(
            "Invalid input. Please enter two comma-separated integers."
        )
    except IndexError:
        raise click.BadParameter(
            "Invalid input. Please enter exactly two comma-separated integers."
        )
    except AssertionError as e:
        if "Position already occupied" in e.args[0]:
            raise click.BadParameter(
                "Invalid input. Position already occupied. Chose different position."
            )
        else:
            raise click.BadParameter(
                "Invalid input. Please enter two comma-separated integers with each integer between 0 and 2."
            )


def _is_game_over(game_board: np.array, position: Tuple[int, int]) -> None:
    # Return bool
    pass


def _show_game_board(game_board: np.array) -> None:
    show_game_board_dict = {0: " ", 1: "X", 2: "O"}

    print("Game Board status")
    line_splitter = "-------------"
    print(line_splitter)
    for row in range(3):
        row_str = "|"
        for col in range(3):
            row_str += f" {show_game_board_dict[game_board[row, col]]} |"
        print(f"{row_str}\n{line_splitter}")


@click.command()
def game_loop():
    starting_player = click.prompt(
        "Enter starting input choice. It can be either 'o' or 'x'.",
        type=click.Choice(["o", "x"]),
    )

    next_player = starting_player
    game_board = np.zeros((3, 3), dtype=np.short)
    player_to_number_dict = {"o": 1, "x": 2}
    next_player_dict = {"o": "x", "x": "o"}

    moves_counter = 0

    while True:
        injected_tic_tac_toe_input_checker_func = partial(
            _convert_to_tic_tac_toe_input, game_board=game_board
        )
        coordinates = click.prompt(
            "Enter the row and column on the Tic Tac Toe board (x,y)",
            type=click.STRING,
            value_proc=injected_tic_tac_toe_input_checker_func,
        )

        game_board[coordinates] = player_to_number_dict[next_player]
        _show_game_board(game_board)

        next_player = next_player_dict[next_player]

        moves_counter += 1
        if moves_counter == 9:
            print("Game finished in a draw. Try again.")
            return


if __name__ == "__main__":
    game_loop()
