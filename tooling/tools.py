"""
C.3 Tools Layer (v1)
--------------------
This is the first tiny version of the "Tools Layer".
Right now it only has:
  - list_tools()
  - run(tool_name, payload)
Later, Forge will use this to try tools in Meta-C3 simulation mode.
"""

import json

# ------------------------------------------------------------
# The registry of tools.
# For now just two tiny demo tools.
# Later: codegen, file ops, search, sandbox exec, etc.
# ------------------------------------------------------------
TOOL_REGISTRY = {}

def register_tool(name, func):
    """Add a tool to the registry."""
    TOOL_REGISTRY[name] = func

# ------------------------------------------------------------
# Example tool 1: echo text back
# ------------------------------------------------------------
def tool_echo(payload):
    return {
        "tool": "echo",
        "input": payload,
        "output": payload
    }

# ------------------------------------------------------------
# Example tool 2: reverse a string
# ------------------------------------------------------------
def tool_reverse(payload):
    if not isinstance(payload, str):
        return {"error": "tool_reverse only works on strings."}
    return {
        "tool": "reverse",
        "input": payload,
        "output": payload[::-1]
    }

# Register demo tools
register_tool("echo", tool_echo)
register_tool("reverse", tool_reverse)

# ------------------------------------------------------------
# Public API
# ------------------------------------------------------------
def list_tools():
    """Return available tool names."""
    return list(TOOL_REGISTRY.keys())

def run(tool_name, payload):
    """
    Run a tool by name.
    If unknown, return a friendly JSON error.
    """
    if tool_name not in TOOL_REGISTRY:
        return {
            "error": f"Tool '{tool_name}' not found.",
            "available_tools": list(TOOL_REGISTRY.keys())
        }
    try:
        tool_fn = TOOL_REGISTRY[tool_name]
        return tool_fn(payload)
    except Exception as e:
        return {
            "error": "Tool crashed.",
            "exception": str(e)
        }

# ------------------------------------------------------------
# CLI mode
# usage:
#     python3 -m tooling.tools echo "hello"
# ------------------------------------------------------------
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print(json.dumps({
            "usage": "python3 -m tooling.tools <tool_name> <payload>"
        }, indent=2))
        sys.exit(0)
    name = sys.argv[1]
    payload = " ".join(sys.argv[2:])
    result = run(name, payload)
    print(json.dumps(result, indent=2))
