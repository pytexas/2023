# conference.pytexas.org
Website for the Annual PyTexas Conference

## Local Dev

* Install [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
* Use the following two commands to start the devserver:
    ```bash
    poetry install
    poetry run make devserver
    ```
* Navigate to `http://localhost:8000` to find your site. Do *not* use `http://127.0.0.1:8000` as it will result in a broken pipe error and will not hot-reload.