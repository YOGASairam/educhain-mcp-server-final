# src/tools/mcq_tool.py

from src.services import qna_engine_instance
from typing import Dict, Any
import json # Import json to handle model_dump_json() output

def generate_mcq_questions(topic: str, num: int) -> Dict[str, Any]:
    """
    MCP Tool function to generate multiple-choice questions for a given topic
    using Educhain's QnA engine.

    Args:
        topic: The subject or topic for the MCQs.
        num: The number of MCQs to generate.

    Returns:
        A dictionary containing the generated questions, or an error message.
        The questions are formatted as a list of dictionaries, each with
        'question', 'options', 'answer', and 'explanation'.
    """
    print(f"-> Using Educhain's QnA engine for MCQs on topic: {topic}, number: {num}...")
    try:
        # Educhain's generate_questions returns a Pydantic model (QuestionsResponse).
        # We call .model_dump() to convert it to a dictionary for easier MCP handling.
        # Alternatively, .model_dump_json() returns a JSON string directly.
        # Let's stick to dictionary for now, and MCP server will handle serialization.
        questions_response = qna_engine_instance.generate_questions(topic=topic, num=num)
        
        # The structure from educhain's output might be slightly different.
        # We need to ensure it matches the format expected by your MCP server/Claude Desktop.
        # Educhain's default MCQ output is typically like:
        # {"questions": [{"question": "...", "options": [...], "answer": "...", "explanation": "..."}]}
        # Your previous QnAEngine also produced this, so it should be compatible.
        
        # It's good practice to verify the output structure here.
        # For example, if questions_response is a Pydantic object, questions_response.model_dump()
        # will give you a dictionary.
        result = questions_response.model_dump()
        
        print("-> MCQ Generation Successful via Educhain.")
        return result
    except Exception as e:
        print(f"An error occurred in MCQ generation tool (Educhain): {e}")
        return {"error": str(e)}