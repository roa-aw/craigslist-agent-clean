# Craigslist Vehicle Sales Agent

## Project Overview

This project implements an AI-powered vehicle sales assistant using the Craigslist Cars & Trucks dataset. The system allows users to interact with a conversational agent and search a real vehicle inventory using natural language queries.

The agent can understand requests such as:

* "Do you have any Honda Civics under $15,000?"
* "Show me trucks newer than 2015."
* "What is the average price of a Toyota Tacoma?"

Instead of relying only on pre-trained model knowledge, the agent uses custom Python tools to query a live inventory stored in SQLite and then converts the results into natural language responses.

---

## System Design

The project is organized into four main components:

### 1. Data Layer

The Craigslist Cars & Trucks dataset is downloaded from Kaggle and processed using Python and Pandas.

Responsibilities:

* Load the raw CSV dataset
* Remove invalid records
* Clean unrealistic prices and years
* Store the cleaned data in SQLite
* Create indexes for efficient searches

Files:

* `db/setup.py`
* `db/__init__.py`

---

### 2. Inventory Search Tools

Custom Python functions provide structured access to the inventory.

Implemented tools:

* `search_inventory()`
* `get_similar()`
* `get_makes()`
* `get_price_range()`

These tools return JSON-compatible results that can be consumed by the AI agent.

Files:

* `tools/search.py`
* `tools/__init__.py`

---

### 3. AI Agent

The AI agent uses OpenAI Function Calling.

Responsibilities:

* Understand user requests
* Decide when a tool should be called
* Extract parameters automatically
* Execute inventory searches
* Convert JSON results into natural language responses

Files:

* `agent/agent.py`
* `agent/__init__.py`

---

### 4. User Interface

A command-line interface (CLI) provides multi-turn conversations.

Features:

* Interactive chat
* Conversation memory
* Reset command
* Exit command
* Rich console formatting

File:

* `cli.py`

---

## Technologies Used

* Python
* OpenAI API
* SQLite
* Pandas
* Rich
* python-dotenv
* Git
* GitHub

---

## Installation Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd craigslist-agent-clean
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Download the dataset

Download the Craigslist Cars & Trucks dataset from Kaggle:

https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data

Place the file here:

```text
data/vehicles.csv
```

### 4. Build the database

```bash
python db/setup.py
```

This creates:

```text
db/inventory.db
```

### 5. Configure the OpenAI API key

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

The API key is loaded automatically using `python-dotenv`.

### 6. Run the application

```bash
python cli.py
```

---

## Required Dependencies

Main dependencies:

* openai
* pandas
* rich
* python-dotenv

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## Example Conversations

### Example 1

User:

```text
Do you have any Honda Civics under $15,000?
```

Agent:

```text
I found several Honda Civic listings under $15,000.
Here are some matching vehicles...
```

### Example 2

User:

```text
What is the average price of a used Toyota Tacoma?
```

Agent:

```text
The average price of a Toyota Tacoma in the inventory is approximately ...
```

### Example 3

User:

```text
Show me trucks from 2015 or newer in California.
```

Agent:

```text
I found several matching vehicles...
```

---

## Development Process

The project was developed incrementally using Git and GitHub.

Major development stages:

1. Project scaffold and repository setup
2. Dataset cleaning and SQLite database generation
3. Inventory search implementation
4. Additional search tools and utilities
5. OpenAI function-calling integration
6. CLI implementation
7. Testing and debugging
8. Documentation and final improvements

Meaningful commits were used throughout development to track progress and fixes.

---

## Challenges Encountered

Several challenges were encountered during development:

* Managing a large dataset (~1.4 GB)
* Organizing the project into multiple packages
* Fixing import issues after refactoring
* Handling dataset path changes after moving files
* Building efficient inventory searches
* Integrating OpenAI function calling with custom tools

---

## What I Learned

Through this project I learned:

* How LLM tool calling works
* How to build AI agents that can take actions
* How to integrate external data sources with language models
* How to use SQLite as an inventory backend
* How to structure larger Python projects
* How to manage software development using Git and GitHub

---

## Role of Python, AI, and GitHub

### Python

Python was used for data processing, database management, tool implementation, and the command-line interface.

### AI Components

The OpenAI model acts as the reasoning layer. It determines when inventory tools should be called and converts structured results into natural language responses.

### GitHub

GitHub was used for version control, collaboration, backup, and tracking project development through a meaningful commit history.

---

## Repository

GitHub Repository:

https://github.com/roa-aw/craigslist-agent-clean


