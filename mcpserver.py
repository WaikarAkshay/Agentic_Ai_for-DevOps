from fastmcp import FastMCP
import subprocess
mcp = FastMCP("Docker agent")

@mcp.tool()
def inspect_containers(container_name) -> str:
    """Get detailed info about a Docker container (state, config, network)."""
    result=subprocess.run(["docker","inspect", container_name], capture_output=True, text=True)
    return result.stdout + result.stderr

@mcp.tool()
def list_container() -> str:
    """Get list of a Docker container. (running and stopped)"""
    result= subprocess.run(["docker","ps","-a"], capture_output=True, text=True)
    return result.stdout or result.stderr

@mcp.tool()
def container_logs(container_name) -> str:
    """Get 50 lines of logs from a Docker container."""
    result= subprocess.run(["docker","logs",container_name], capture_output=True, text=True)
    return result.stdout + result.stderr

if __name__ == "__main__":
    mcp.run()