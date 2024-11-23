# algobench
Python library designed for benchmarking standard C++ parallel algorithms, algorithm policies on different standard libraries implementations, compilers and architectures.

## Testing in containerized environment
### Pull container image

podman pull docker.io/sindiesel/cpp_ubuntu:22.0.20

```bash
podman run --interactive --tty --detach \
  --env "TERM=xterm-256color" \
  --mount type=bind,source="$(pwd)",target="$(pwd)" \
  --name cpp \
  --userns keep-id \
  --workdir "$HOME" \
  cpp_ubuntu:22.0.20

# Allow non-root user
podman exec --user root cpp bash -c "chown $(id --user):$(id --group) $HOME"

# Run your command
podman exec --workdir "$(pwd)" cpp bash -c "ls -l"

# Attach to container
podman exec --workdir "$(pwd)" --interactive --tty cpp bash
```
