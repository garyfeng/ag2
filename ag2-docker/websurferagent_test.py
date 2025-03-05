#!/usr/bin/env python3
import asyncio
import nest_asyncio
import os
import sys
import platform
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent
from autogen.tools.experimental import BrowserUseTool

# Patch asyncio to allow nested event loops.
nest_asyncio.apply()

def setup_agents():
    # Load environment variables from .env file.
    load_dotenv()
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        sys.exit("Error: Please set the OPENAI_API_KEY environment variable in your .env file.")
    
    # Configure model and browser settings.
    config_list = [{"model": "gpt-4o-mini", "api_key": OPENAI_API_KEY}]
    llm_config = {"config_list": config_list}
    BROWSER_HEADLESS = os.environ.get("BROWSER_HEADLESS", "True").lower() == "true"
    browser_config = {"headless": BROWSER_HEADLESS}

    # Create agents and register the tool.
    user_proxy = UserProxyAgent(name="user_proxy", human_input_mode=HUMAN_INPUT_MODE)
    assistant = AssistantAgent(name="assistant", llm_config=llm_config)
    browser_use_tool = BrowserUseTool(llm_config=llm_config, browser_config=browser_config)
    browser_use_tool.register_for_execution(user_proxy)
    browser_use_tool.register_for_llm(assistant)
    return user_proxy, assistant, browser_use_tool

async def process_query(query, user_proxy, assistant):
    try:
        # initiate_chat returns a ChatResult object (synchronous), so no await here.
        response = user_proxy.initiate_chat(
            recipient=assistant,
            message=query,
            max_turns=WEBSURFER_MAX_TURNS,
        )
    except Exception as e:
        print(f"Error processing query: {e}")
        return None
    return response

def display_response(response):
    if response is None:
        print("No response received from the agent.")
    elif hasattr(response, 'messages'):
        print("\nWebSurferAgent response:")
        for msg in response.messages:
            print(f"[{msg.source}] {msg.content}")
    else:
        print("\nAgent response:")
        print(response)
    print("\n---\n")

async def main_async(user_proxy, assistant, browser_use_tool):
    try:
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

            response = await process_query(query, user_proxy, assistant)
            display_response(response)
    finally:
        # Cleanup: call aclose() if available; otherwise, use close()
        if hasattr(browser_use_tool, "aclose"):
            await browser_use_tool.aclose()
        elif hasattr(browser_use_tool, "close"):
            browser_use_tool.close()

def main():
    # On Windows, use the selector policy to avoid known issues.
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    user_proxy, assistant, browser_use_tool = setup_agents()

    # Get or create a persistent event loop.
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(main_async(user_proxy, assistant, browser_use_tool))
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

if __name__ == "__main__":
    load_dotenv()
    WEBSURFER_MAX_TURNS = int(os.environ.get("WEBSURFER_MAX_TURNS", 2))
    HUMAN_INPUT_MODE = os.environ.get("HUMAN_INPUT_MODE", "NEVER")
    print(f"WEBSURFER_MAX_TURNS: {WEBSURFER_MAX_TURNS}")
    print(f"HUMAN_INPUT_MODE: {HUMAN_INPUT_MODE}")

    main()
