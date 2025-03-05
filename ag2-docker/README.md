# AG2 WebSurferAgent Test

See https://github.com/garyfeng/ag2/issues/1

# Instructions

## Install RealVNC or other VNC viewer (optional)

If you want to seee the WebSurfAgent working the browser in real time, you need to 
- start the docker with the `start.sh` script, which sets up a VNC server and X Window server
- set up a `.env` file to set `BROWSER_HEADLESS=true`; see below
- set up a VNC viewer on your host machine

RealVNC Viewer is free. Run the RealVNC, and connect to `localhost:5900` after launching the agent (below). This will create an entry in the "address book" for you to reuse later. 

First time you connect when no browser is running, it may display a dialogue box saying something like you need a terminal, etc. Ignore it. When the browser launches all will be fine.

## Setting env variables

Create an `.env` file, with content like:

```
ANONYMIZED_TELEMETRY=false
BROWSER_HEADLESS=true
OPENAI_API_KEY=sk-proj-aULK9j0h6z_XXXXXX
```

If you don't have VNC or do not plan to view the browser content, set `BROWSER_HEADLESS=false`. 

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

# Usage

The docker will run the `websurferagent_test.py` script at start up. You will see a bunch of info messages in the terminal, until it stops with `>>`. This is the agent waiting for your input. 

You can say something like `get me top news on Google News`, or `find a flisht from NYC to Boston tomorrow morning`. If you have the VNC set up and the `.env` file setting `BROWSER_HEADLESS=true`, you should now see the browser in action. 

