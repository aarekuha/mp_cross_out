.PHONY: run

prepare:
	@rm -rf venv || true
	@python -m venv venv
	@source venv/bin/activate && pip install -r requirements.txt

run:
	bash -c 'source venv/bin/activate && gunicorn -c gunicorn_config.py app:app 2>&1 | python3 process_logs.py || true'
	@echo '======='
	@echo 'error.out and example.out - filled'
	@echo '======='
