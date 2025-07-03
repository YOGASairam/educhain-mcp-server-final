# AI Intern Assignment: EduChain MCP Server

This repository contains the full implementation for the AI Intern Assignment. The project is an MCP (Model Context Protocol) server that leverages the `educhain` library with a locally hosted Large Language Model (LLM) to generate educational content. This server is designed to expose its functionalities as tools and resources for an MCP host, specifically Claude Desktop.

## Project Overview

The primary objective of this assignment was to build an MCP server capable of providing educational content on demand. The server exposes several tools and resources that can be accessed by a host application like Claude Desktop. All AI content generation is performed locally using the `Mistral-7B-Instruct-v0.2-GGUF` model, ensuring privacy and offline functionality.

---

## Features

The server provides three distinct educational capabilities:

1.  **Multiple-Choice Question (MCQ) Generator** (`generate_mcq_questions_tool`)
    * Generates a specified number of multiple-choice questions on any given topic.
    * Each question typically includes the question text, four options, the correct answer, and an detailed explanation.

2.  **Lesson Plan Generator** (`generate_lesson_plan_resource`)
    * Creates a structured lesson plan for a specified topic.
    * The output typically includes a title, learning objectives, and a list of activities.

3.  **Flashcard Generator** (`generate_flashcards_tool`) - (Bonus Feature)
    * Generates a set of flashcards (front and back) for a given topic.

---

## Technical Implementation and Architecture

This project implements an MCP server using the official Model Context Protocol (MCP) Python SDK, specifically `FastMCP`, to communicate with Claude Desktop via the `stdio` (Standard Input/Output) transport mechanism. The core content generation logic is powered by the `educhain` Python library, which is integrated with a local `llama-cpp-python` instance running the `Mistral-77B-Instruct-v0.2-GGUF` model.

### Key Components:

* **`educhain` Library Integration:** The `educhain` library's `QnAEngine` and `ContentEngine` are utilized for content generation. The local LLM is passed to `educhain` via `LLMConfig` to ensure all content generation leverages the local model.
* **`llama-cpp-python` for Local LLM:** This library provides Python bindings for `llama.cpp`, enabling efficient inference with GGUF models on local hardware (CPU, and optionally GPU if configured). The `Mistral-7B-Instruct-v0.2-Q4_K_M.gguf` model is used for content generation.
* **`FastMCP` Server (MCP Python SDK):** This is the core of the MCP server. It handles the communication protocol with Claude Desktop. Tools and resources are registered using `@mcp.tool()` and `@mcp.resource()` decorators, automatically generating their schemas.
* **STDIO Transport:** Claude Desktop is configured to spawn this server and communicate with it over standard input/output streams. This allows Claude Desktop to manage the server process and capture its logs effectively.
* **Structured Output Handling:** EduChain's engines return Pydantic models, which are then converted to standard Python dictionaries using `.model_dump()` before being sent as JSON responses by the MCP server. This ensures compatibility with the client's expectations.

### Architecture Flow:

1.  **Server Startup:** When Claude Desktop needs to use a tool, it spawns `src/mcp_server.py`.
2.  **Model Loading:** `src/services.py` initializes the `llama-cpp-python` instance (loading the GGUF model into memory once) and then creates an `educhain.Educhain` client, configured to use this local LLM.
3.  **Tool/Resource Discovery:** Claude Desktop queries the spawned server over STDIO to get the definitions of available tools and resources (provided by `FastMCP` from the decorated functions in `src/mcp_server.py`).
4.  **Tool/Resource Execution:** When a user prompts Claude Desktop to use a tool (e.g., "Generate a lesson plan..."), Claude sends the request to the spawned server.
5.  **Content Generation:** The corresponding decorated function in `src/mcp_server.py` calls the relevant `educhain` engine function (`qna_engine_instance.generate_questions` or `content_engine_instance.generate_lesson_plan`/`generate_flashcards`).
6.  **Response:** The generated content (as a dictionary) is returned by the `FastMCP` server back to Claude Desktop, which then formats it for the user.
7.  **Logging:** All server-side print statements directed to `sys.stderr` are captured by Claude Desktop and written to its internal log files (`mcp-server-educhain_server.log`).

### Justification for Architecture:

This architecture directly addresses the assignment's requirements:
* **Local LLM Integration:** Achieved via `llama-cpp-python` and `educhain`'s `LLMConfig`.
* **MCP Server:** Implemented using the `FastMCP` SDK.
* **Tool and Resource Exposure:** Defined and exposed as per MCP specification.
* **Robustness:** By adhering to the intended `stdio` transport and utilizing the structured `FastMCP` decorators, the integration is more stable and aligned with the official guidelines for Claude Desktop interactions.

---

## Setup and Usage Instructions

Follow these steps to get the EduChain MCP Server up and running locally.

### 1. Clone the Repository

First, clone this project repository to your local machine:

```bash
git clone [https://github.com/YOGASairam/claude_educhain_mcp_server.git](https://github.com/YOGASairam/claude_educhain_mcp_server.git)
cd claude_educhain_mcp_server