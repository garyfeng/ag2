from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve your API key from the environment
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY in your .env file.")

from autogen.agents.experimental import WebSurferAgent

def main():
    llm_config = {
        "config_list": [{"model": "gpt-4o-mini", "api_key": api_key}]
    }
    websurfer = WebSurferAgent(
        name="WebSurfer",
        system_message="You are an assistant with browsing capability.",
        llm_config=llm_config,
        web_tool="browser_use",
    )
    result = websurfer.run(
        message="Search for latest AI news",
        tools=websurfer.tools,
        max_turns=2,
        user_input=False,
    )
    print("Result:", result.summary)

if __name__ == "__main__":
    main()
