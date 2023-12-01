_default:
  just --list

# run linting and typecheking over the solutions
@lint:
	black solutions
	ruff solutions --fix
	pyright

