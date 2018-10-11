# Demo for JSON in Redis (3 ways: String, Hash and ReJSON)

# Install

Run:

```
$ pip install -r requirements.txt
```

This should install `redis-py` and `flatten_json`

For the ReJSON demo, you'll need the ReJSON module installed in Redis.

In both python files (`app.py`,`rejson.py`) you'll need add your credentials.

# Running

`app.py` contains the demo for the storing JSON as a string and flattened into a hash.

You can run it by specifying your own JSON file or using the supplied `test.json` file. This should run on just about any install of Redis.

```
$ python app.py --json ./test.json
```

`raw_rejson.py` contains the demo for storing JSON natively with the ReJSON module.

You can run it using the same format as `app.py`:

```
$ python raw_rejson.py --json ./test.json
```


`client_rejson.py` contains the demo for storing JSON natively with the ReJSON module (using the python module).

You can run it using the same format as `app.py`:

```
$ python client_rejson.py --json ./test.json
```
