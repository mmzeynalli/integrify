# If you have `direnv` loaded in your shell, and allow it in the repository,
# the `make` command will point at the `scripts/make` shell script.
# This Makefile is just here to allow auto-completion in the terminal.

args = $(foreach a,$($(subst -,_,$1)_args),$(if $(value $a),$a="$($a)"))

_coverage_args = title
_docs_serve_args = lang
_new_integration_args = name
_test_args = live

actions = \
	setup \
	format \
	lint \
	type-check \
	test \
	coverage \
	docs \
	docs-serve \
	secure \
	clean \
	new-integration \
	all

.PHONY: $(actions)
$(actions):
	@uv run --no-sync duty $@ $(call args,_$@)

