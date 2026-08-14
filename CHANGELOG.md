# Changelog

All notable changes to `integrify` (the umbrella package) are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/) and this
project follows [Semantic Versioning](https://semver.org/).

## [3.0.0] - 2026-08-13

Re-architected from a single monolithic package into an **umbrella package over a
monorepo of independently-published integrations**. The top-level `integrify`
distribution ships no integration code of its own — install only what you need:

- `pip install integrify` — shared core only
- `pip install integrify[epoint]` — core + EPoint
- `pip install integrify[epoint,lsim]` — core + selected integrations
- `pip install integrify[all]` — every integration

Import paths are unchanged (`integrify.epoint`, `integrify.kapitalbank`, …).

### Changed

- Split into an umbrella plus per-integration distributions (`integrify-epoint`, `integrify-core`, …), each pulled in through its extra.

### Removed

- **Breaking:** replaced the previous monolithic `integrify` (last release 2.2.2); integrations must now be opted into via extras.
- **Breaking:** dropped Python 3.9 (end-of-life) — now requires Python >= 3.10.

[3.0.0]: https://github.com/Integrify-SDK/integrify-python/releases/tag/integrify-3.0.0
