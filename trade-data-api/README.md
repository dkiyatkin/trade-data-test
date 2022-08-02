# trade-data-api

## Install dependencies
```sh
pipenv install --dev
```

## Start the server
```sh
pipenv run uvicorn app.main:app --reload
```

## Run tests
```sh
pipenv run pytest
```

## Format code
```sh
pipenv run black .
```

## Type check
```sh
pipenv run mypy app
```
