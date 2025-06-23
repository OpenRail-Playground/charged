all: setup_environment

clean:
	rm -rf .venv

setup_environment: check
	curl -LsSf https://astral.sh/uv/install.sh | sh \
	&& uv sync \
	&& uv run pre-commit install \
	&& git config --local include.path ./gitconfig.local \

check: uvx_exists is_git

uvx_exists: ; @which uvx > /dev/null

is_git: ; @git rev-parse --git-dir > /dev/null

notebook:
	uv run python -m notebook

strip:
	find . -name '*.ipynb' -exec uv run nbstripout {} +
