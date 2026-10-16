# Tasks API

> **Practice repo** for the DevOps track, Course 3, Lesson 5: *Merge, squash or rebase? Forks and upstream*. Three pull requests were merged here three different ways (a merge commit, squash and merge, rebase and merge), so you can compare the history each leaves with `git log --oneline --graph`. The real project is [devops-tasks-api](https://github.com/agl-learn-examples/devops-tasks-api).

A tiny to-do list REST API in Python and Flask. It is the running example for the **DevOps track on [agentlabs learn](https://learning.myagentlabs.ai)**: every course adds one layer to this same project, from running it on your laptop to Git, Docker, Compose, CI, nginx, the cloud and Kubernetes.

## Run it

    python3 -m venv .venv
    . .venv/bin/activate
    pip install -r requirements.txt
    flask --app app run

Then, in a second terminal:

    curl localhost:5000/health

## Endpoints

| method | path | does |
|---|---|---|
| GET | /health | `{"status": "ok"}` |
| GET | /tasks | list tasks |
| POST | /tasks | create a task: `{"title": "..."}` → 201 |
| GET | /tasks/&lt;id&gt; | one task, or 404 |
| PUT | /tasks/&lt;id&gt; | replace a task |
| DELETE | /tasks/&lt;id&gt; | delete a task → 204 |

## Tests

    pytest

Tasks are stored in `tasks.db` (SQLite) next to `app.py`.
