import json
import os
import sys

def printJason(infile):
	sum = 0
	with open(infile) as json_file:
		json_data = json.load(json_file)
		messages = json_data
		for message in messages:
			if 'body' in message:
				print message["timestamp_relative"], id_to_names[message["author"]], message["body"]
				sum += 1
			elif 'log_message_body' in message:
				print message["timestamp_relative"], id_to_names[message["author"]], message["log_message_body"]
				sum += 1
		print sum, "messages printed."

def getConfig(infile):
	try:
		with open(infile, 'r+') as infile:
			return json.load(infile)
	except:
		print "Error loading configuration file %s" % infile
		sys.exit()


if __name__ == "__main__":
	if (len(sys.argv) != 3):
		print "Error. You need to specify your conversation partner's Facebook user id, and a configuration file."
		sys.exit()

	id_to_names = getConfig(sys.argv[1])["ids_dictionary"]
	printJason(os.path.join("Messages", sys.argv[2], "complete.json"))