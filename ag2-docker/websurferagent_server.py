# demo.py
from dotenv import load_dotenv
import os
import sys

# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    sys.exit("Error: Please set the OPENAI_API_KEY environment variable in your .env file.")


# LLM configuration for AG2
llm_config = {
    "config_list": [{"model": "gpt-4o-mini", "api_key": api_key}]
}

# Import AG2 agents
from autogen.agents.experimental import WebSurferAgent
from autogen import UserProxyAgent

# Initialize the WebSurferAgent
websurfer = WebSurferAgent(
    name="WebSurfer",
    system_message="You are a web browsing agent that can search the internet and complete tasks.",
    llm_config=llm_config,
    web_tool="browser_use",
)

# Initialize the human agent (UserProxyAgent)
human = UserProxyAgent(name="human", human_input_mode="ALWAYS")

print("Welcome to the AG2 WebSurfer demo!")
print("Registered tools:", websurfer.tools)

for tool in websurfer.tools:
    # print(f"Tool name: {tool.function.get('name') if hasattr(tool, 'function') else 'unknown'}")
    print(f"Tool name: {tool.name}")

print("Enter a task for the WebSurferAgent (or type 'exit' to quit):")

while True:
    try:
        query = input(">> ")
    except EOFError:
        print("Input stream closed. Exiting.")
        break
    if query.strip().lower() in ("exit", "quit"):
        print("Exiting demo.")
        break

    # Initiate conversation: human sends a message to the WebSurferAgent
    response = human.initiate_chat(
        recipient=websurfer,
        tools=websurfer.tools,
        message=query,
        max_turns=5  # Adjust this if you need a longer conversation
    )
    
    if response is None:
        print("No response received from the agent.")
        continue

    # Depending on the AG2 version, the response may have a 'messages' attribute.
    if hasattr(response, 'messages'):
        print("\nWebSurferAgent response:")
        for msg in response.messages:
            print(f"[{msg.source}] {msg.content}")
    else:
        print("\nAgent response:")
        print(response)
        
    print("\n---\n")
