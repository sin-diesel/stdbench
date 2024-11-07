# algobench
Python library designed for benchmarking standard C++ parallel algorithms, algorithm policies on different standard libraries implementations, compilers and architectures.

# Testing in containerized environment
```bash
podman run --interactive --tty --detach \
  --env "TERM=xterm-256color" \
  --mount type=bind,source="$(pwd)" \
  --name cpp \
  --userns keep-id \
  --workdir "$HOME" \
  ghcr.io/rudenkornk/cpp_ubuntu:22.0.19

# Run your command
podman exec --workdir "$(pwd)" cpp bash -c "ls -l"

# Attach to container
podman exec --workdir "$(pwd)" --interactive --tty cpp bash
```
