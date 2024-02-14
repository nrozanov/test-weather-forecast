# Solution for https://github.com/SeitaBV/assignment-data-engineering?tab=readme-ov-file

## Development setup

### Install virtual environment

- Install [poetry](https://python-poetry.org/docs/#installation) on your machine
- You will need Python version 3.10 for this project
- Go into project directory and install all packages with **poetry**:
    ```
    poetry install --no-root
    ```

  This will create a new virtual environment and install all project dependencies there

- Configure your IDE of choice to use newly created virtual environment

### Commands

Enter virtual env:

`poetry shell`

Run development server:

`python manage.py`

or

`./manage.py`

Query examples:

`curl -v 'http://127.0.0.1:8000/weather/forecasts/2021-09-10%2017%3A00%3A00%2B00/2021-09-11%2017%3A00%3A00%2B00/'`

`curl -v 'http://127.0.0.1:8000/weather/forecasts/2021-09-10%2017%3A00%3A00%2B00/'`

Run tests:

`pytest`

## Documentation

The documentation for this project can be found on the /docs handler of the server. To access it, start the server and navigate to http://localhost:8000/docs in your web browser.
