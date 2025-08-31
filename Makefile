# @ na frente do comando suprime a exibição do comando no terminal

run:
	@poetry run uvicorn store.main:app --reload

pre-commit-install:
	@poetry run pre-commit install

pre-commit-run:
	@poetry run pre-commit run --all-files

test:
	@poetry run pytest