from pydantic import BaseModel
from typing import Generator
import json

class Task(BaseModel):
  id: int
  title: str


def json_chunks(json_string):
    #We split by a reasonable chunk size.
    chunk_size = 5  # You can adjust this value depending on your actual use case.
    for i in range(0, len(json_string), chunk_size):
        chunk = json_string[i:i+chunk_size]
        yield chunk


def tasks_from_chunks(json_chunks: Generator[str, None, None]):
  # Initialize an empty string to hold the JSON chunks that need to be parsed.
    remaining = ""

    for chunk in json_chunks:
        # Combine the remaining chunk from the previous iteration with the current chunk.
        combined_chunk = remaining + chunk
        try:
            # Try to load the combined JSON string.
            parsed_json = json.loads(combined_chunk)
            remaining = ""  # If successful, reset the remaining string.
        except json.JSONDecodeError:
            # If the JSON is not complete, set the remaining chunk and continue to the next iteration.
            remaining = combined_chunk
            continue

        tasks = parsed_json.get('tasks', [])
        for task_json in tasks:
            # Parse the individual task and yield it.
            task = Task(**task_json)
            print("yield task", task)
            yield task
 
 
json_string = '{"tasks":[{"id":1,"title":"task1"},{"id":2,"title":"task2"},{"id":3,"title":"task3"}]}'

# Test case 1: Iterate over the tasks and print them
print("Test case 1:")
for task in tasks_from_chunks(json_chunks(json_string)):
    print(task)

# Test case 2: Collect tasks in a list and print the list
print("\nTest case 2:")
tasks_list = list(tasks_from_chunks(json_chunks(json_string)))
print(tasks_list)
