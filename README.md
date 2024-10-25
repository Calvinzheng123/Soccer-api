# LionAPI

LionAPI is a FastAPI application designed to provide soccer data through a API and SQL Database. It allows users to retrieve detailed information about soccer matches, including shot data, teams, and events. Plan to update to have more features in
the future

## Features

- Fetch detailed shot data for specific matches.
```
from LionAPI import get_shots
df = get_shots("Liverpool","Chelsea","2024-10-20")
```
- Query match events with a date range
example usage
```
from LionAPI import query_events
events = query_events("2024-10-19","2024-10-23")
print(events)
```
## Installation

You can install the package using pip:

```bash
pip install LionAPI
