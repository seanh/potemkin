.PHONY: dev
dev:
	tox -e py36-dev

.PHONY: shell
shell:
	tox -e py36-shell

.PHONY: sql
sql:
	sqlite3 potemkin.sqlite

.PHONY: clean
clean:
	rm -rf .tox
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
