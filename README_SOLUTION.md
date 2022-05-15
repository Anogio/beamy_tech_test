# My solution

## Level 1
I used a simple Flask app in a docker container.
The app exposes its 3000 port, and returns a 400 error if the log has an error 
that we expect (broken key/value mapping with an additional space).

In real life we would want to improve error management but 
the exercise did not specify the expected behavior.

The server writes in a folder inside the container. To check it out, you can
look at `/opt/app/parsed`

## Level 2
I used a docker-compose file to create the server + redis.

To handle the timeout, I use the API call just to enqueue the log,
and run a worker thread which reads that queue to process the lines.

I made this choice since we were setting up a Redis anyway, so it was pretty
straightforward to set up.

To check out the content of the redis, in a python shell:
```python
import redis
r = redis.Redis(host='localhost', port=6379)
r.llen("parsed_logs")
r.lpop("parsed_logs")
```

## Running the solution
### Tests
- `make test_environment` to start the required Redis
- `make test` to run the tests

### Level 1
- `make level_1_server` to run the solution
- `run_exercise` to make the calls to the server (uses you local
python - or current venv -not a docker)

### Level 2
- `make level_2_server` to run the solution (Flask server + Redis)
- `run_exercise` to make the calls to the server (uses you local
python - or current venv -not a docker)

## Next steps

- Adding better and more logging
- Adding better and more error handling
- Adding precommits (I used black one-shot to format the code here)
- Adding tests, separating more clearly endpoint tests, worker tests
and processing logic tests, by mocking out the parts that are not being tested.
- Improving the worker logic so that it can be killed gracefully, as for now the tests 
will hang rather than terminate.
- In production, we would want to have the worker on a different pod so that
a crash in the API would not cause a crash of the worker, and scaling is independent.