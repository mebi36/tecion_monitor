.PHONY: black
black:
	black -l 79 company/*.py
	black -l 79 home/*.py
	black -l 79 monitor/*.py
	black -l 79 item/*.py
	black -l 79 yser/*.py