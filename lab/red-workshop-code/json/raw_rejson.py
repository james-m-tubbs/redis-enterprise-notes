import redis
import argparse

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

# write JSON with REJSON
r.execute_command('JSON.SET','some_json','.',arguments.json[0].read())

# get a single (string) value from the JSON
value_of_myjson = r.execute_command('JSON.GET','some_json','myjson')
print('myjson in some_json: '+value_of_myjson)


# create an array
r.execute_command('JSON.SET','some_json','secondary.spanishNumbers','["uno"]')

# Append some values to the Array
r.execute_command('JSON.ARRAPPEND','some_json','secondary.spanishNumbers','"tres"','"cuatro"')

# insert a value to the Array
r.execute_command('JSON.ARRINSERT','some_json','secondary.spanishNumbers','1','"dos"')

# get the array back
value_of_spanishNumbers = r.execute_command('JSON.GET','some_json','secondary.spanishNumbers')
print(value_of_spanishNumbers)

# Append to the a string value
r.execute_command('JSON.STRAPPEND','some_json','myjson','"well"')

# Get the whole json object back
value_of_some_json = r.execute_command('JSON.GET','some_json','.')
print('some_json: '+value_of_some_json)
