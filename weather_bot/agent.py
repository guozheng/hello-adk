# @title Import libraries
import os
import asyncio
from google.adk.agents.llm_agent import Agent
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

import warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.INFO)

import dotenv
dotenv.load_dotenv()

def get_weather(city: str) -> dict:
    city_normalized = city.lower().replace(" ", "")

    mock_weather = {
        "newyork": {
            "status": "success",
            "report": "Sunny with a chance of rain"
        },
        "paris": {
            "status": "success",
            "report": "Cloudy with a chance of snow"
        },
        "tokyo": {
            "status": "success",
            "report": "Rainy with a chance of sun"
        }
    }
    
    if city_normalized in mock_weather:
        return mock_weather[city_normalized]
    
    return {
        "status": "error",
        "message": "City not found"
    }


APP_NAME = "weather_agent"
USER_ID = "user_id"
SESSION_ID = "session_id"

root_agent = Agent(
    model='gemini-2.5-flash',
    name=APP_NAME,
    description='A helpful weather assistant.',
    instruction='Find the weather for a given city.',
    tools=[
        get_weather
    ]
)

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service
)

async def run_query(query: str, user_id: str, session_id: str):
    content = types.Content(
        role='user',
        parts=[
            types.Part(
                text=query
            )
        ]
    )

    # default response
    response = "no response from agent"

    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response:
            if event.content and event.content.parts:
                response = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                response = f"Agent escalated: {event.error_message} or 'No specific message'"
            else:
                response = "No response from agent"
            break

    logging.info(f"Agent response: {response}")

async def main():
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    logging.info(f"Session created: app_name={APP_NAME}, user_id={USER_ID}, session_id={SESSION_ID}")

    await run_query("What is the weather like in New York?", USER_ID, SESSION_ID)
    await run_query("What is the weather like in Paris?", USER_ID, SESSION_ID)
    await run_query("What is the weather like in Tokyo?", USER_ID, SESSION_ID)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Error: {e}")