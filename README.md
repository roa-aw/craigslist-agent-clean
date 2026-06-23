# Craigslist Vehicle Sales Agent

## Project Summary

This project was developed as part of the WEX 427 Workplace Experience course. The goal was to build an AI-powered sales agent that can answer customer questions about vehicle inventory using real data rather than relying only on the model's built-in knowledge.

The project uses the Craigslist Cars & Trucks dataset from Kaggle as a simulated vehicle inventory. The dataset is cleaned and stored in a SQLite database, and the AI agent can query this inventory through custom Python tools. When a user asks a question such as:

> "Do you have any Honda Civics under $15,000?"

the agent identifies the relevant search parameters, queries the inventory, and presents the results in a natural conversational format.

The project demonstrates the integration of Python, SQLite, OpenAI Function Calling, and GitHub within a single application.

---

## System Design

The application consists of four main components.

### 1. Data Processing Layer

The Craigslist vehicle dataset is downloaded from Kaggle and processed using Pandas.

Responsibilities:

* Reading the raw CSV file
* Removing invalid and incomplete records
* Filtering unrealistic prices and years
* Creating a clean SQLite database
* Generating indexes to improve query performance

Files:

* `db/setup.py`
* `db/__init__.py`

---

### 2. Inventory Search Tools

The inventory tools provide a structured interface between the language model and the database.

Implemented tools:

* `search_inventory()`
* `get_similar()`
* `get_makes()`
* `get_price_range()`

These functions query the SQLite database and return structured JSON responses that can be used by the AI agent.

Files:

* `tools/search.py`
* `tools/__init__.py`

---

### 3. AI Agent

The AI agent uses OpenAI Function Calling to decide when a tool should be used.

Responsibilities:

* Understanding user requests
* Extracting search parameters
* Selecting the appropriate tool
* Executing inventory searches
* Converting structured results into natural language responses

Files:

* `agent/agent.py`
* `agent/__init__.py`

---

### 4. User Interface

The application includes a command-line chat interface that supports multi-turn conversations.

Features:

* Interactive chat experience
* Conversation memory
* Reset conversation command
* Exit command
* Rich terminal formatting

File:

* `cli.py`

---

## Project Structure

```text
craigslist-agent-clean/
├── agent/
│   ├── agent.py
│   └── __init__.py
├── db/
│   ├── setup.py
│   └── __init__.py
├── tools/
│   ├── search.py
│   └── __init__.py
├── data/
│   └── vehicles.csv
├── cli.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

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

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/roa-aw/craigslist-agent-clean.git
cd craigslist-agent-clean
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Download the dataset

Download the Craigslist Cars & Trucks dataset from Kaggle:

https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data

Place the dataset file in:

```text
data/vehicles.csv
```

Note: The dataset is not included in this repository because of its size.

### 4. Build the inventory database

```bash
python db/setup.py
```

This creates:

```text
db/inventory.db
```

### 5. Configure the OpenAI API key

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
```

The project uses `python-dotenv` to load the API key automatically.

### 6. Run the application

```bash
python cli.py
```

---

## Required Dependencies

The project uses the following main libraries:

```text
openai>=1.0.0
pandas>=2.0.0
rich>=13.0.0
python-dotenv>=1.0.0
```

Install them with:

```bash
pip install -r requirements.txt
```

---

## Example Conversations

### Example 1

**User**

```text
Do you have any Honda Civics under $15,000?
```

**Agent**

```text
I found several Honda Civic listings under $15,000.
Here are some matching vehicles along with their prices and locations.
```

---

### Example 2

**User**

```text
What is the average price of a used Toyota Tacoma?
```

**Agent**

```text
The average price of a Toyota Tacoma in the current inventory is approximately ...
```

---

### Example 3

**User**

```text
Show me trucks from 2015 or newer in California.
```

**Agent**

```text
I found several matching vehicles that meet your criteria.
```

---
## Sample Output

### Inventory Search

The screenshot below demonstrates the AI agent extracting multiple search parameters from a natural language request and querying the inventory database.

![Ford Search](images/ford-search.png)

### Price Analysis

The screenshot below demonstrates the AI agent using inventory statistics to answer pricing questions.

![Price Analysis](images/price-analysis.png)

### Multi-Turn Conversation

The screenshot below demonstrates conversation memory and context awareness across multiple user interactions.

![Conversation Memory](images/bmw-newer.png)
## Development Process

I developed this project incrementally and tracked progress using Git and GitHub. The implementation was divided into several stages:

1. Creating the project structure and repository
2. Loading and cleaning the Craigslist dataset
3. Building the SQLite inventory database
4. Implementing inventory search tools
5. Adding OpenAI Function Calling support
6. Developing the AI agent
7. Creating the command-line interface
8. Testing and debugging
9. Writing documentation and finalizing the project

A meaningful commit history was maintained throughout the project to document progress and changes.

---

## Challenges Encountered

Several challenges were encountered during development:

* Working with a large dataset (approximately 1.4 GB)
* Designing efficient inventory search queries
* Organizing the project into separate modules
* Resolving import and package structure issues
* Managing dataset and database file paths
* Integrating custom Python tools with OpenAI Function Calling

These challenges helped improve my understanding of project organization, debugging, and AI integration.

---

## What I Learned

Through this project I learned:

* How AI agents interact with external tools
* How OpenAI Function Calling works
* How to connect language models to real-world data sources
* How to use SQLite as a lightweight backend database
* How to structure medium-sized Python projects
* How to use Git and GitHub effectively throughout development
* How to debug package imports and file path issues

---

## Role of Python, AI, and GitHub

### Python

Python was used for data processing, database creation, inventory searches, agent implementation, and the command-line interface.

### AI Components

The language model serves as the reasoning component of the system. Using OpenAI Function Calling, the model decides when a tool should be called, determines the required parameters, and transforms the returned JSON data into user-friendly responses.

### GitHub

GitHub was used for version control, backup, and documenting the development process through meaningful commits. It also serves as the platform for sharing and evaluating the completed project.

---

## Repository Link

GitHub Repository:

https://github.com/roa-aw/craigslist-agent-clean
