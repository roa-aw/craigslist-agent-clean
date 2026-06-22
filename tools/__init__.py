from tools.search import search_inventory, get_similar, get_makes, get_price_range

# ── OpenAI tool schemas ────────────────────────────────────────────────────

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_inventory",
            "description": (
                "Search the used-car inventory with optional filters. "
                "Call this whenever the user asks about available vehicles, "
                "specific makes/models, price ranges, conditions, or regions. "
                "Returns a list of matching listings."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "make":         {"type": "string",  "description": "Vehicle manufacturer, e.g. 'honda', 'ford'"},
                    "model":        {"type": "string",  "description": "Model name, e.g. 'civic', 'f-150'"},
                    "max_price":    {"type": "number",  "description": "Maximum price in USD"},
                    "min_price":    {"type": "number",  "description": "Minimum price in USD"},
                    "min_year":     {"type": "integer", "description": "Earliest model year"},
                    "max_year":     {"type": "integer", "description": "Latest model year"},
                    "condition":    {"type": "string",  "description": "One of: new, like new, excellent, good, fair, salvage"},
                    "color":        {"type": "string",  "description": "Paint color, e.g. 'blue', 'red'"},
                    "cylinders":    {"type": "string",  "description": "Engine cylinders, e.g. '4 cylinders', '8 cylinders'"},
                    "fuel":         {"type": "string",  "description": "Fuel type: gas, diesel, electric, hybrid"},
                    "transmission": {"type": "string",  "description": "automatic or manual"},
                    "drive":        {"type": "string",  "description": "Drive type: fwd, rwd, 4wd, awd"},
                    "region":       {"type": "string",  "description": "City or region name"},
                    "state":        {"type": "string",  "description": "US state abbreviation, e.g. 'ca', 'tx'"},
                    "limit":        {"type": "integer", "description": "Max results to return (default 8)"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_similar",
            "description": (
                "Find similar vehicles when the exact search returned no results. "
                "Relaxes price and year constraints by ~20% / 3 years."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "make":      {"type": "string",  "description": "Vehicle manufacturer"},
                    "max_price": {"type": "number",  "description": "Original max price"},
                    "min_year":  {"type": "integer", "description": "Original min year"},
                    "limit":     {"type": "integer", "description": "Max results"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_makes",
            "description": "Return all vehicle makes available in the inventory.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_price_range",
            "description": (
                "Get the min, max, and average price for a make/model. "
                "Use when the user asks 'how much does a used X cost?'"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "make":  {"type": "string", "description": "Manufacturer"},
                    "model": {"type": "string", "description": "Model name"},
                },
                "required": [],
            },
        },
    },
]

# Map name → callable
TOOL_MAP = {
    "search_inventory": search_inventory,
    "get_similar":      get_similar,
    "get_makes":        get_makes,
    "get_price_range":  get_price_range,
}
