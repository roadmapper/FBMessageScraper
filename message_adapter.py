import json
from pprint import pprint

# This adapter parses the json of the downloaded messages and
# extracts the essential fields for my analysis script.

name = "{}-{}"
file_names = []
k = 0
while k != 168000:
	# Assuming we download 2000 messages at a time
	file_names.append(name.format(k, k+2000))
	k += 2000

msg_dir = '<downloaded messages dir>/{}.json'
output = {}
output["messages"] = []
no_body = 0
for fname in file_names:
	print fname + " in progress..."
	with open(msg_dir.format(fname)) as msg_file:
		data = json.load(msg_file)
		msgs = data["payload"]["actions"]
		for msg in msgs:
			clean_msg = {}
			clean_msg["author"] = msg["author"]
			try:
				clean_msg["body"] = msg["body"]
			except KeyError:
				no_body += 1
				continue
			clean_msg["source"] = msg["source"]
			clean_msg["timestamp"] = msg["timestamp"]
			clean_msg["timestamp_datetime"] = msg["timestamp_datetime"]
			clean_msg["timestamp_absolute"] = msg["timestamp_absolute"]
			output["messages"].append(clean_msg)


with open('message_data.json', 'w') as outfile:
	json.dump(output, outfile)

print "Number of messages without a body: " + str(no_body)