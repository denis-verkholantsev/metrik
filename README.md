# metrik
## Стек
* FastAPI
* EdgeDB
* Docker
* Prometheus
* Grafana
## Описание
Система для структуризации знаний с помощью графов.
Сценарий в контексте образования:
* пользователь создает граф - дерево знаний
* создает в нем узлы - навыки
* навыки можно оценить, например, по вашему знанию этого skill'а или по степени его важности
* в навыке можно указать:
  * необходимые знания, которые нужно получить, чтобы считать его изученным
  * дополнительные материалы
  * ссылки
* любой навык можно связать с другим

Оценки skill'ов  и граф могут быть как публичными, так и нет.
Публичный граф пользователь может скопировать к себе для собственного использования.

Перед запуском убедитесь, что у вас установлены:
- Python3.10
- [poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://docs.docker.com/engine/install/)
- [EdgeDB](https://www.edgedb.com/install)
- [Make](https://www.gnu.org/software/make/)

* скопируйте себе данный репозиторий (рекомендуется использовать `ssh`):

    ```sh
    git clone git@gitlab.com:spbu-practice-fall-2023/server.git
    ```
* Перейдя в директорию репозитория создайте виртуальное окружение с Python3.10 любым
   удобным способом (`virtualenv`, `poetry`, `pyenv`) и активируйте окружение

    ```sh
    python3.10 -m venv .venv
    source .venv/bin/activate
    ```

* Установите зависимости

    ```sh
    poetry install
    ```

* Установите `pre-commit` хуки

    ```sh
    make install-pre-commit
    ```

* Сделайте несколько копий настроек `debug.env`, `test.env` и `docker.env`:

    ```sh
    make copy-config
    ```

* Запустите локальный экземпляр EdgeDB в Docker

    ```sh
    make dc-edgedb
    ```

1. Свяжите локальный EdgeDB проект с удаленным экземпляром EdgeDB в Docker

    ```sh
    make link-edgedb-dc
    ```

* Убедитесь, что во всех файлах настроек находятся данные соответствующие вашему
   окружению, например хосты и порты для подключения к БД соответствуют локально
   развернутым

* Запустите сервис

    Запустить сервис можно либо в debug режиме VS Code (конфигурация Debug FastAPI, F5),
    либо локально через Makefile, либо в Docker:

    ```sh
    make run        # local
    make dc-server  # Docker
    ```
