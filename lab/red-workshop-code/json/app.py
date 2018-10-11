from flatten_json import flatten
from flatten_json import unflatten_list
import json
import argparse
import redis

# connect to redis
r = redis.Redis(
   host='yourhost',
   password='yourpassword',
   decode_responses=True)


# parse out the JSON file from the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--json', nargs=1,
                    help="JSON file",
                    type=argparse.FileType('r'))
arguments = parser.parse_args()

# beflatten it
flat_json = flatten(json.load(arguments.json[0]))

# write it to Redis
my_hash_key = 'pyjson'
r.hmset(my_hash_key, flat_json)
print('Wrote to key: '+my_hash_key)

# fetch it from Redis
flat_json_from_redis = r.hgetall(my_hash_key)
print('Read flat version from key: '+my_hash_key)
print(flat_json_from_redis)

# take the flat verison and convert it back to a nested dic
unflattened_json = unflatten_list(flat_json_from_redis)
print('Unflattened to:')
print(unflattened_json)

