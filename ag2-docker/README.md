# AG2 WebSurferAgent Test

See https://github.com/garyfeng/ag2/issues/1

# Instructions

## Install RealVNC or other VNC viewer

RealVNC Viewer is free.

## Build the docker image

```sh
docker build -t ag2-vnc .       
```

## Run the docker image

First set up your OpenAI API key in the `.env` file

```
OPENAI_API_KEY=sk-proj-aULK9j0h6zXXXXXX
```

Then run the docker, exposing the VNC port. This docker command picks up the `.env` vars by default. Also note that we need `-it` for the user's input.

```sh
docker run -it -p 5900:5900 ag2-vnc
```