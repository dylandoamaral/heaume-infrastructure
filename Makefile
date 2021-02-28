lint:
	@poetry run pylint heaume_infrastructure tests

isort:
	@poetry run isort heaume_infrastructure tests

format:
	@poetry run black heaume_infrastructure tests

tidy: isort format

check: lint
	@poetry run black heaume_infrastructure tests --check
	@poetry run isort heaume_infrastructure tests --check

test:
	@poetry run pytest --cov=heaume_infrastructure --cov-config .coveragerc --cov-report=xml --spec tests

layer:
	mkdir tmp; \
	cd tmp; \
	python -m venv .venv; \
	. .venv/bin/activate; \
	pip install -r ../heaume_infrastructure/shared/layer/requirements.txt; \
	mkdir python; \
	cp -r .venv/lib64/python3.8/site-packages/* python; \
	zip -r heaume_layer.zip python; \
	mv heaume_layer.zip ../heaume_infrastructure/shared/layer/heaume_layer.zip; \
	cd ..; \
	rm -r tmp
