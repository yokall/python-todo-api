# 3rd party modules
from flask import json, Response, make_response, abort

# Data to serve with our API
TODOS = {
    1: {
        "id": 1,
        "title": "Some work",
        "complete": True
    },
    2: {
        "id": 2,
        "title": "Some more work",
        "complete": False
    },
    3: {
        "id": 3,
        "title": "Even more work",
        "complete": False
    }
}


# Create a handler for our read_all (GET) todos


def read_all():
    """
    This function responds to a request for /api/todos
    with the complete lists of todos

    :return:        sorted list of todos
    """
    # Create the list of todos from our data
    return [TODOS[key] for key in sorted(TODOS.keys())]


def read_one(id):
    """
    This function responds to a request for /api/todos/{id}
    with one matching todo from todos
    :param id:   id of todo to find
    :return:        todo matching last name
    """
    # Does the todo exist in todos?
    if id in TODOS:
        todo = TODOS.get(id)

    # otherwise, nope, not found
    else:
        abort(
            404, "Person with last name {id} not found".format(id=id)
        )

    return todo


current_id = 3


def get_next_id():
    global current_id
    current_id += 1
    return current_id


def create(todo):
    """
    This function creates a new todo in the todos structure
    based on the passed in todo data
    :param todo:  todo to create in todos structure
    :return:        201 on success, 406 on todo exists
    """
    id = get_next_id()
    title = todo.get("title", None)
    complete = todo.get("complete", False)

    # Does the todo exist already?
    if id not in TODOS and id is not None:
        TODOS[id] = {
            "id": id,
            "title": title,
            "complete": complete,
        }
        return Response(json.dumps(TODOS[id]), status=201)

    # Otherwise, they exist, that's an error
    else:
        abort(
            406,
            "Todo with id {id} already exists".format(id=id),
        )


def update(id, todo):
    """
    This function updates an existing todo in the todos structure
    :param id:   id of todo to update in the todos structure
    :param todo:  todo to update
    :return:        updated todo structure
    """
    # Does the todo exist in todos?
    if id in TODOS:
        TODOS[id]["title"] = todo.get("title")
        TODOS[id]["complete"] = todo.get("complete")

        return TODOS[id]

    # otherwise, nope, that's an error
    else:
        abort(
            404, "Todo with id {id} not found".format(id=id)
        )


def delete(id):
    """
    This function deletes a todo from the people structure
    :param id:   id of todo to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Does the todo to delete exist?
    if id in TODOS:
        del TODOS[id]
        return make_response(
            "{id} successfully deleted".format(id=id), 200
        )

    # Otherwise, nope, todo to delete not found
    else:
        abort(
            404, "Todo with id {id} not found".format(id=id)
        )
