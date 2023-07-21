from typing import Any, Dict, List

import requests


def _get_todo_response(url: str) -> Any:
    response = requests.get(url)

    return response.json()


def find_incomplete_tasks(todo_json: List[Dict]) -> None:
    completed_todos = 0
    total_todos = len(todo_json)

    completed_todos = sum([1 if todo["completed"] else 0 for todo in todo_json])

    print(
        f"Total number of todos: {total_todos}. Number of completed todos: {completed_todos}"
    )


if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/todos"
    todo_json = _get_todo_response(url)
    find_incomplete_tasks(todo_json)
