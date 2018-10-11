import argparse
import json
from rejson import Client, Path


rj = Client(
    host='localhost', 
    password='yourpassword',
    decode_responses=True)



# parse out the JSON file from the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--json', nargs=1,
                    help="JSON file",
                    type=argparse.FileType('r'))
arguments = parser.parse_args()

# write JSON with REJSON
rj.jsonset('some_json',Path.rootPath(),json.loads(arguments.json[0].read()))

# get a single (string) value from the JSON
value_of_myjson = rj.jsonget('some_json', Path('myjson'))
print('myjson in some_json: {}'.format(value_of_myjson))


# create an array
rj.jsonset('some_json',Path('secondary.spanishNumbers'),["uno"])

# Append some values to the Array
rj.jsonarrappend('some_json',Path('secondary.spanishNumbers'),"tres","cuatro")

# insert a value to the Array
rj.jsonarrinsert('some_json',Path('secondary.spanishNumbers'),'1','dos')


# get the array back
value_of_spanishNumbers = rj.jsonget('some_json',Path('secondary.spanishNumbers'))
print(value_of_spanishNumbers)

# Append to the a string value
rj.jsonstrappend('some_json','well',Path('myjson'))

# Get the whole json object back
value_of_some_json = rj.jsonget('some_json',Path.rootPath())
print('some_json: '+json.dumps(value_of_some_json, indent=1))
