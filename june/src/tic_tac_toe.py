from functools import partial
from typing import Dict, Tuple

import click
import numpy as np


def _convert_to_tic_tac_toe_input(
    value: str, game_board: np.ndarray
) -> Tuple[int, int]:
    try:
        values = value.split(",")
        try:
            assert len(values) == 2
        except AssertionError:
            raise ValueError("Please enter exactly two comma-separated integers.")

        tuple_values = (int(values[0]), int(values[1]))

        assert tuple_values[0] >= 0 and tuple_values[0] < 3
        assert tuple_values[1] >= 0 and tuple_values[1] < 3

        try:
            assert game_board[tuple_values] == 0
        except AssertionError:
            raise ValueError("Position already occupied. Chose different position")

    except ValueError as e:
        if "Position already occupied" in e.args[0]:
            raise click.BadParameter(
                "Invalid input. Position already occupied. Chose different position."
            )
        elif "Please enter exactly two comma-separated integers." in e.args[0]:
            raise click.BadParameter(
                "Invalid input. Please enter exactly two comma-separated integers between 0 and 2."
            )

    except AssertionError:
        raise click.BadParameter(
            "Invalid input. "
            "Please enter two comma-separated integers with each integer between 0 and 2."
        )

    return tuple_values


def _is_game_over(
    game_board: np.ndarray, position: Tuple[int, int], player_id: int
) -> int:
    if np.all(game_board[position[0], :] == player_id):
        return 1
    if np.all(game_board[:, position[1]] == player_id):
        return 1
    if np.sum(position) == 2 or position[0] == position[1]:
        if np.all(np.diag(game_board) == player_id):
            return 1
        if np.all(np.diag(np.fliplr(game_board)) == player_id):
            return 1
    return 0


def _show_game_board(
    game_board: np.ndarray, show_game_board_dict: Dict[int, str]
) -> None:
    print("Game Board status")
    line_splitter = "-------------"
    print(line_splitter)
    for row in range(3):
        row_str = "|"
        for col in range(3):
            row_str += f" {show_game_board_dict[game_board[row, col]]} |"
        print(f"{row_str}\n{line_splitter}")


@click.command()
def game_loop() -> None:
    """
    Game loop that runs each move and outputs the game board.
    It stops if the board is full or if a player has won.
    If a player wins, it reports which player has won.
    """
    starting_player = click.prompt(
        "Enter starting input choice",
        type=click.Choice(["o", "x"]),
    )

    next_player = starting_player
    game_board = np.zeros((3, 3), dtype=np.short)
    player_to_number_dict = {"o": 1, "x": 2}
    show_game_board_dict = {0: " ", 1: "o", 2: "x"}
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
        _show_game_board(game_board, show_game_board_dict)
        if _is_game_over(game_board, coordinates, player_to_number_dict[next_player]):
            print(f"Game over. Player {next_player} won.")
            return

        next_player = next_player_dict[next_player]

        moves_counter += 1
        if moves_counter == 9:
            print("Game finished in a draw. Try again.")
            return


if __name__ == "__main__":
    game_loop()
