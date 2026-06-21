import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

PRESETS = {
    "orchestrator": "@preset/career-os-orchestrator",
    "fit": "@preset/career-os-fit",
    "gap": "@preset/career-os-gap",
    "shift": "@preset/career-os-shift",
    "academic": "@preset/career-os-academic",
    "report": "@preset/career-os-report",
    "parser": "@preset/career-os-parser",
}

def call_agent(agent_name, messages):

    preset = PRESETS[agent_name]

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": preset,
            "messages": messages
        }
    )

    response.raise_for_status()

    return response.json()

# EXAMPLE #
#result = call_agent(
#    "fit",
#   [
#        {
#            "role": "user",
#            "content": student_json
#        }
#    ]
#)
