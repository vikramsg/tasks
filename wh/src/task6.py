from typing import Dict
import requests


def _get_todo_response(url: str) -> Dict:
    response = requests.get(url)

    return response.json()


def find_incomplete_tasks(todo_json: Dict) -> None:
    # Initialize a counter for completed todos
    completed_todos = 0

    # Iterate over the todos
    for todo in todo_json:
        # If the todo is completed, increment the counter
        if todo["completed"]:
            completed_todos += 1

    print(f"Number of completed todos: {completed_todos}")


if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/todos"
    todo_json = _get_todo_response(url)
    find_incomplete_tasks(todo_json)
