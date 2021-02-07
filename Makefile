test:
	@poetry run pytest --cov=heaume_infrastructure --cov-config .coveragerc --cov-report=xml --cov-report=term tests/

clean:
	@poetry run black heaume_infrastructure tests
	@poetry run isort heaume_infrastructure tests

check:
	@poetry run pylint heaume_infrastructure tests
	@poetry run black heaume_infrastructure tests --check
	@poetry run isort heaume_infrastructure tests --check

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
