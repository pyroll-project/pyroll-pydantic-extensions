set default-list

format:
    treefmt

test key="":
    uv run pytest -k "{{ key }}"
