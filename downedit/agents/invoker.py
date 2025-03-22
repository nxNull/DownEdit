from downedit.agents.registry import get_tool
from downedit.utils import log


async def invoke_tool_async(tool_name: str, tool_args: dict):
    """
    Invokes a tool asynchronously based on the tool name.

    Args:
        tool_name (str): The name of the tool to invoke.
        tool_args (dict): The arguments to pass to the tool.
    """
    tool_class = get_tool(tool_name)


def invoke_tool_sync(tool_name: str, tool_args: dict):
    """
    Invokes a tool synchronously based on the tool name.

    Args:
        tool_name (str): The name of the tool to invoke.
        tool_args (dict): The arguments to pass to the tool.
    """
    tool_class = get_tool(tool_name)

    if tool_class:
        try:
            with tool_class(**tool_args) as tool_instance:
                tool_instance.start()
        except Exception as e:
            pass
            log.error(f"❌ Failed to invoke tool '{tool_name}': {str(e)}")
    else:
        log.error(f"Tool '{tool_name}' not found.")
