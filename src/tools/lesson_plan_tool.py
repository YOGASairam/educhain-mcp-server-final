# src/tools/lesson_plan_tool.py

from src.services import content_engine_instance
from typing import Dict, Any
import json # Import json to handle model_dump_json() output

def generate_lesson_plan(topic: str) -> Dict[str, Any]:
    """
    MCP Resource function to generate a comprehensive lesson plan for a specified topic
    using Educhain's Content engine.

    Args:
        topic: The subject or topic for the lesson plan.

    Returns:
        A dictionary representing the lesson plan (e.g., with title, objectives, activities),
        or an error message.
    """
    print(f"-> Using Educhain's Content engine for lesson plan on topic: {topic}...")
    try:
        # Educhain's generate_lesson_plan returns a Pydantic model.
        lesson_plan_response = content_engine_instance.generate_lesson_plan(topic=topic)
        
        # Convert the Pydantic model to a dictionary.
        result = lesson_plan_response.model_dump()
        
        print("-> Lesson Plan Generation Successful via Educhain.")
        return result
    except Exception as e:
        print(f"An error occurred in lesson plan generation tool (Educhain): {e}")
        return {"error": str(e)}