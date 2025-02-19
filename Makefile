# If you have `direnv` loaded in your shell, and allow it in the repository,
# the `make` command will point at the `scripts/make` shell script.
# This Makefile is just here to allow auto-completion in the terminal.

actions = \
	setup \
	format \
	lint \
	type-check \
	test-live \
	test-local \
	test-github \
	coverage \
	docs \
	docs-serve \
	secure \
	clean \
	new-integration \
	all

.PHONY: $(actions)
$(actions):
	@uv run duty "$@" $(ARGS)
