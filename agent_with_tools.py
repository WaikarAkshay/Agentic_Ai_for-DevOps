import ollama 
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool
import subprocess

@tool()
def inspect_containers(container_name) -> str:
    """Get detailed info about a Docker container (state, config, network)."""
    result=subprocess.run(["docker","inspect", container_name], capture_output=True, text=True)
    return result.stdout + result.stderr

@tool()
def list_container() -> str:
    """Get list of a Docker container. (running and stopped)"""
    result= subprocess.run(["docker","ps","-a"], capture_output=True, text=True)
    return result.stdout or result.stderr

@tool()
def container_logs(container_name) -> str:
    """Get 50 lines of logs from a Docker container."""
    result= subprocess.run(["docker","logs",container_name], capture_output=True, text=True)
    return result.stdout + result.stderr

SYSTEM_PROMPT="""
You are an intelligent Docker assistant that helps users inspect and debug containers using a fixed set of tools.

Core Behavior:
- You operate strictly as a tool-using agent.
- You must NOT guess or fabricate any container information.
- Always call the appropriate tool when information is required.
- Prefer tool usage over assumptions.

Available Tools:
1. list_container()
   Returns a list of all available containers.

2. inspect_containers(container_name)
   Returns detailed metadata and configuration of a container.

3. container_logs(container_name)
   Returns runtime logs of a container.



Container Name Handling:
- If a container name is required but not provided:
  - Call list_containers() first.
  - Select the most relevant container based on context.
  - If ambiguity remains, ask the user for clarification.

Response Style:
- Be concise, technical, and action-oriented.
- Summarize tool outputs into clear insights instead of dumping raw data unless explicitly requested.
- Highlight key issues such as errors, restart loops, misconfigurations, and port conflicts.

Error Handling:
- If a tool fails or returns no data:
  - Clearly inform the user.
  - Suggest next steps (e.g., verify container name, check if container is running).

Safety Constraints:
- Do NOT perform destructive or state-changing actions (e.g., stop, remove, restart containers).
- Only observe and report.
- Do NOT hallucinate logs, container states, or configurations.

Goal:
Help the user quickly understand their Docker environment and diagnose issues using accurate, tool-backed insights.
"""
llm=ChatOllama(model="mistral:latest", temperature=0.9)
tools=[list_container, inspect_containers, container_logs ]
agent = create_agent(llm, tools)
print("\nMulti-Tool DevOps Agent")
print("-" * 40)
print("I can troubleshoot Docker and Kubernetes.")
print("Type 'stop' to exit.\n")
while True:
    user_input=input(">> ")
    if user_input=="stop" or user_input=="exit":
        break
    else:
        result=agent.invoke(
            {
                "messages": [{
                    "role": "user", 
                    "content": user_input
                    }]}
            )
        print(result["messages"][-1].content)
        print()
