Sure, let's update the README:

---

# aosync

## Description

This cli tool provides a way to import any existing AppOptics dashboard or create/update existing dashboards and charts based on the YAML specification. It also supports functionality like being able to define a dynamic tag that can be applied to all charts consistently. More functionalities can be supported based on best practices.

## Installation

You can use Docker to run aosync. If Docker is not already installed on your system, you can download it from [Docker's official website](https://www.docker.com/products/docker-desktop).

## Available Commands

1. **pull**
   - Description: This command pulls a dashboard from AppOptics and exports it into a YAML file. The dashboard ID and output file path need to be specified as arguments. The AppOptics token can be passed as an option or set as an environment variable 'APPOPTICS_TOKEN'.
   - Usage: `pull <dashboard_id> <output>`
   - Options: `--appoptics_token=<appoptics_token>`
   - Example: `pull 123 ./dashboard.yaml --appoptics_token=xyz`

2. **sync**
   - Description: This command reads a dashboard from a YAML file and synchronizes it with the AppOptics server. The input file path needs to be specified as an argument. The AppOptics token can be passed as an option or set as an environment variable 'APPOPTICS_TOKEN'.
   - Usage: `sync <input>`
   - Options: `--appoptics_token=<appoptics_token>`
   - Example: `sync ./dashboard.yaml --appoptics_token=xyz`

## Usage

You can run aosync using Docker. Here are some example commands:

```bash
# Build the Docker image
docker build -t aosync:latest .

# Pull a dashboard and export it to a YAML file
docker run --rm -v "$HOME:$HOME" -e APPOPTICS_TOKEN='your_token' aosync:latest pull 123 $HOME/dashboard.yaml

# Synchronize a dashboard from a YAML file
docker run --rm -v "$HOME:$HOME" -e APPOPTICS_TOKEN='your_token' aosync:latest sync $HOME/dashboard.yaml
```

## License

MIT

---

Note: In the Docker run commands, we're using `-v "$HOME:$HOME"` to mount the host's home directory to the same path in the Docker container. This allows the container to access the host's file system for reading the YAML file and writing the output. Make sure to replace `'your_token'` with your actual AppOptics token.
