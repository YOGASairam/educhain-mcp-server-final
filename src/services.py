# src/services.py

from langchain_community.llms import LlamaCpp
from educhain import Educhain, LLMConfig # Import Educhain and LLMConfig
from src.config import MODEL_PATH

"""
Initializes the local LLM (LlamaCpp) and sets up the Educhain client
with this local model. This module provides the central access points
for Educhain's content and Q&A generation engines.
"""

print("-> Initializing AI model and Educhain client...")

# Load the LLM only once when the server starts
# We use a larger context (n_ctx) for potentially long lesson plans or complex questions.
llm_instance = LlamaCpp(model_path=MODEL_PATH, n_ctx=4096, verbose=False)

# Create an LLMConfig for Educhain to use the custom LlamaCpp model
llm_config = LLMConfig(custom_model=llm_instance)

# Initialize the Educhain client with your custom LlamaCpp LLM
educhain_client = Educhain(llm_config)

# Expose the Educhain's built-in engines
qna_engine_instance = educhain_client.qna_engine
content_engine_instance = educhain_client.content_engine

print("-> AI Services (Educhain with LlamaCpp) are ready.")