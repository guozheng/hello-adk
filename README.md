# Hello ADK

This is a simple project to demonstrate the use of the Google ADK.

## Setup

```bash
uv sync
```

## Create a New Agent

To create a new agent, run:

```bash
adk create <directory>
```

This will create a new agent in the root directory.

## Run Agents on the Command Line

Each agent is in its own directory. To run an agent, navigate to the directory and run:

```bash
adk run <directory>
```

## Run Agents on the Web

```bash
adk web --port <port>
```

Navigate to http://localhost:<port> in your browser.

## Run Agents with .py Directly

For some agent that has main(), you can run it directly with:

```bash
uv run <directory>/agent.py
```

The behavior might be different from running the agent with adk run.