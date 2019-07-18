# twisted-log-reader

This is very basic application written in python 2 using [twisted](https://github.com/twisted/twisted) for reading log entries from the `.jsonl` file.

## Running locally:

    git clone https://github.com/mostwk/twisted-log-reader

    cd twisted-log-reader

    virtualenv .venv

    pip install -r requirements.txt

    python server.py


## Testing:

    curl -d '{"offset": 0}' -H "Content-Type: application/json" -X POST http://localhost:8000/read_log


with `offset_diff = 5` response will be something like:

```json
    {
      "total_size": 100000,
      "next_offset": 5,
      "ok": true,
      "messages": [
        {
            "message": "Log message #0",
            "level": "ERROR"
        },
        {
            "message": "Log message #1",
            "level": "WARN"
        },
        {
            "message": "Log message #2",
            "level": "INFO"
        },
        {
            "message": "Log message #3",
            "level": "ERROR"
        },
        {
            "message": "Log message #4",
            "level": "ERROR"
        }
      ]
    }
```

