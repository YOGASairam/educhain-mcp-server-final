# src/mcp_server.py

import os
from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP # Import FastMCP
import asyncio
import sys # For explicit print flushing

# Ensure services are initialized (Educhain client with LlamaCpp)
import src.services

# Import your tool functions
from src.tools.mcq_tool import generate_mcq_questions
from src.tools.lesson_plan_tool import generate_lesson_plan
from src.tools.flashcard_tool import generate_flashcards

# src/mcp_server.py (Modified section for resource decorator)

# ... (rest of your imports and initial app setup)

# src/mcp_server.py (Modified section for resource decorator)

# ... (rest of your imports and initial app setup)

# Initialize FastMCP server
# The name "educhain_server" will be used in claude_desktop_config.json
mcp = FastMCP("educhain_server")
print("-> EduChain MCP Server (FastMCP) initialized.", file=sys.stderr) # Logging to stderr for Claude Desktop capture

# --- Define MCP Tools and Resources using @mcp.tool() and @mcp.resource() decorators ---

@mcp.tool()
async def generate_mcq_questions_tool(topic: str, num: int) -> Dict[str, Any]:
    """
    Generates multiple-choice questions for a given topic.
    
    Args:
        topic: The subject or topic for the MCQs.
        num: The number of MCQs to generate.

    Returns:
        A dictionary containing a list of questions, each with 'question', 'options', 'answer', and 'explanation'.
    """
    print(f"-> DEBUG [MCP Tool]: Calling generate_mcq_questions with topic='{topic}' and num={num}", file=sys.stderr)
    try:
        result = generate_mcq_questions(topic=topic, num=num)
        print("-> DEBUG [MCP Tool]: MCQ Generation Successful.", file=sys.stderr)
        return result
    except Exception as e:
        print(f"-> DEBUG [MCP Tool]: An error occurred in MCQ generation: {e}", file=sys.stderr)
        return {"error": str(e)}

# MODIFICATION HERE: Change uri to 'generate_lesson_plan/{topic}'
@mcp.resource(uri='generate_lesson_plan/{topic}')
async def generate_lesson_plan_resource(topic: str) -> Dict[str, Any]:
    """
    Generates a comprehensive lesson plan for a specified topic.

    Args:
        topic: The subject or topic for the lesson plan.

    Returns:
        A dictionary representing the lesson plan (e.g., with title, objectives, activities).
    """
    print(f"-> DEBUG [MCP Resource]: Calling generate_lesson_plan with topic='{topic}'", file=sys.stderr)
    try:
        result = generate_lesson_plan(topic=topic)
        print("-> DEBUG [MCP Resource]: Lesson Plan Generation Successful.", file=sys.stderr)
        return result
    except Exception as e:
        print(f"-> DEBUG [MCP Resource]: An error occurred in lesson plan generation: {e}", file=sys.stderr)
        return {"error": str(e)}

@mcp.tool() # Flashcards are typically a tool, as they are "generated"
async def generate_flashcards_tool(topic: str, num: int) -> Dict[str, Any]:
    """
    Generates flashcards (front and back) for a given topic.

    Args:
        topic: The subject or topic for the flashcards.
        num: The number of flashcards to generate.

    Returns:
        A dictionary containing a list of flashcards.
    """
    print(f"-> DEBUG [MCP Tool]: Calling generate_flashcards with topic='{topic}' and num={num}", file=sys.stderr)
    try:
        result = generate_flashcards(topic=topic, num=num)
        print("-> DEBUG [MCP Tool]: Flashcard Generation Successful.", file=sys.stderr)
        return result
    except Exception as e:
        print(f"-> DEBUG [MCP Tool]: An error occurred in flashcard generation: {e}", file=sys.stderr)
        return {"error": str(e)}


# ... (rest of your main server run logic)


# --- Main server run logic ---
if __name__ == "__main__":
    # In FastMCP, you just call mcp.run() with the transport type.
    # 'stdio' means it will communicate over standard input/output streams,
    # which is what Claude Desktop expects when it spawns the process.
    print("-> Starting EduChain MCP Server with STDIO transport...", file=sys.stderr)
    # The 'log_level' argument to run is typically for the server's own internal logging,
    # but we are manually printing to stderr for Claude's log capture.
    mcp.run(transport='stdio')
    print("-> EduChain MCP Server stopped.", file=sys.stderr)