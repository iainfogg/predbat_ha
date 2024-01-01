# Predbat HA

## Important

The `scripts/develop` script will fail unless you first run `pip install git+https://github.com/boto/botocore`

See <https://github.com/home-assistant/core/issues/95192> for info.

## TO DO

- Amend binary sensors and switches to work from the controller
instead of the coordinator
- Amend sensors to work with multiple devices rather than just
a single one
- Create sensors / config for Predbat control
- Build out config which allows selection of inverter manufacturer
- Build an options flow with options to suit the manufacturer
- Allow creation of an inverter object which matches the type of
inverter selected in the config
- Add services for sections of the processing
- Work out what entities are actually needed (and which ones can just be saved
as state without going in the entity registry)
- Work out approach to get original Predbat code working within this context

## Developing on Predbat HA

Write up how to get a dev instance running, including
how to set up on a Windows machine with WSL, installing Docker,
using Devcontainer extension, running in run/debug modes.
