# src/tools/flashcard_tool.py

from src.services import content_engine_instance
from typing import Dict, Any
import json # Import json to handle model_dump_json() output

def generate_flashcards(topic: str, num: int) -> Dict[str, Any]:
    """
    MCP Tool function to generate flashcards for a given topic
    using Educhain's Content engine.

    Args:
        topic: The subject or topic for the flashcards.
        num: The number of flashcards to generate.

    Returns:
        A dictionary containing the generated flashcards, or an error message.
    """
    print(f"-> Using Educhain's Content engine for flashcards on topic: {topic}, number: {num}...")
    try:
        # Educhain's generate_flashcards returns a Pydantic model.
        flashcards_response = content_engine_instance.generate_flashcards(topic=topic, num=num)
        
        # Convert the Pydantic model to a dictionary.
        result = flashcards_response.model_dump()
        
        print("-> Flashcard Generation Successful via Educhain.")
        return result
    except Exception as e:
        print(f"An error occurred in flashcard generation tool (Educhain): {e}")
        return {"error": str(e)}