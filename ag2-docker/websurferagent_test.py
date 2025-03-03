from dotenv import load_dotenv
import os
import sys
from autogen import AssistantAgent, UserProxyAgent
from autogen.tools.experimental import BrowserUseTool

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") 
if not OPENAI_API_KEY:
    sys.exit("Error: Please set the OPENAI_API_KEY environment variable in your .env file.")
config_list = [{"model": "gpt-4o-mini", "api_key": OPENAI_API_KEY}]

llm_config = {
    "config_list": config_list,
}

BROWSER_HEADLESS = os.environ.get("BROWSER_HEADLESS", "False").lower() == "true"
browser_config={"headless": BROWSER_HEADLESS}

user_proxy = UserProxyAgent(name="user_proxy", human_input_mode="NEVER")
assistant = AssistantAgent(name="assistant", llm_config=llm_config)

browser_use_tool = BrowserUseTool(
    llm_config=llm_config,
    browser_config=browser_config,
)

browser_use_tool.register_for_execution(user_proxy)
browser_use_tool.register_for_llm(assistant)


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
    response = user_proxy.initiate_chat(
        recipient=assistant,
        message=query,
        max_turns=2,
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
