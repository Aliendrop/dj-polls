BACK = back/
MANAGE = python $(BACK)manage.py


all: test

test:
	@$(MANAGE) test api --verbosity 0

dev:
	@$(MANAGE) runserver

mmg:
	@$(MANAGE) makemigrations

mg:
	@$(MANAGE) migrate
