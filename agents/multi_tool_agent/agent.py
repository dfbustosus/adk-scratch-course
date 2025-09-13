"""Example ADK agent using google-adk Quickstart pattern.

Run from repo root:
  - pip install google-adk
  - adk web    # dev UI
  - adk run multi_tool_agent  # CLI
"""

from __future__ import annotations

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent


def get_weather(city: str) -> dict:
    """Return a simple hard-coded weather report for a city.

    Args:
        city: City name, case-insensitive.

    Returns:
        A dict with either {"status": "success", "report": ...} or
        {"status": "error", "error_message": ...}.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25°C "
                "(77°F)."
            ),
        }

    return {
        "status": "error",
        "error_message": f"Weather information for '{city}' is not available.",
    }


def get_current_time(city: str) -> dict:
    """Return the current time for a supported city.

    Args:
        city: City name, case-insensitive.

    Returns:
        A dict with either {"status": "success", "report": ...} or
        {"status": "error", "error_message": ...}.
    """
    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f"The current time in {city} is "
        f"{now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"
    )
    return {"status": "success", "report": report}


# ADK discovers this root_agent when running `adk web` / `adk run`
root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent that answers questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the "
        "time and weather in a city."
    ),
    tools=[get_weather, get_current_time],
)
