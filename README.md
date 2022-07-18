# podman-decompose
Convert docker-compose files into podman commands

**Note**: This tool does not yet implement the entire
[docker-compose spec](https://docs.docker.com/compose/compose-file/). It was
created to convert a specific set of files. If you run into issues converting
a given file, start with the assumption that the tool needs to be extended.
Fortunately, that's easy to do.

```
usage: podman-decompose [-h] [-d,--destroy] [--build] [--no-build] path

positional arguments:
  path          The docker-compose file to decompose

optional arguments:
  -h, --help    show this help message and exit
  -d,--destroy  Generate commands to destroy, rather than create
  --build       Include commands to build containers (the default)
  --no-build    Do not include commands to build containers
```
