from LionAPI.services import query_events

start_date = "2024-10-19"
end_date = "2024-10-23"

events = query_events(start_date,end_date)
print(events)