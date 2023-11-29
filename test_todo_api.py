import requests
import uuid

ENDPOINT = "https://todo.pixegami.io"


def test_can_call_endpoint():
    # check that endpoint is available
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_can_create_task():
    # create new task
    # check that the task was created
    payload = get_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200

    create_task_data = create_task_response.json()
#    print(create_task_data)

    task_id = create_task_data['task']['task_id']

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200

    get_task_response = get_task_response.json()
    assert get_task_response['content'] == payload['content']
    assert get_task_response['user_id'] == payload['user_id']
    assert get_task_response['is_done'] == payload['is_done']


def test_can_update_task():
    # create task
    payload = get_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()['task']['task_id']
    # update the task
    new_payload = {
        'user_id': payload['user_id'],
        'content': 'new content',
        'task_id': task_id,
        'is_done': True
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200

    # get and validate the changes
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload['content']
    assert get_task_data['is_done'] == new_payload['is_done']


def test_can_list_tasks():
    # check current number of tasks for user
    user_id = get_payload()['user_id']
    initial_tasks = get_tasks_list(user_id)
    assert initial_tasks.status_code == 200
#    print(user_id)
    initial_number_tasks = len(initial_tasks.json()['tasks'])
    print(initial_number_tasks)
    # create N tasks
    n = 3
    for i in range(n):
        payload = get_payload()
        payload['user_id'] = user_id
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200
    # get tasks from server and check count
    list_task_response = get_tasks_list(user_id)
    assert list_task_response.status_code == 200
    list_task_data = list_task_response.json()

    tasks = len(list_task_data['tasks'])
    assert tasks == initial_number_tasks + n


def test_delete_task():
    # create task
    payload = get_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()['task']['task_id']
    # delete the task
    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200
    # try to get task
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404


def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)


def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")


def get_tasks_list(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")


def update_task(payload):
    return requests.put(ENDPOINT + "/update-task", json=payload)


def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")


def get_payload():
    user_id = f"test_{uuid.uuid4().hex}"
    content_test = f"test_{uuid.uuid4().hex}"
    return {
        "content": content_test,
        "user_id": user_id,
        "is_done": False
    }
