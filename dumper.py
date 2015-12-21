# This code is a fork of of Raghav Sood's 2014 script, hosted on https://github.com/RaghavSood/FBMessageScraper
# Changes compared to commit 4e3f268:
# * Uses configuration files instead of hardcoded values
# * Fixed a bug detecting the end_of_history mark
# * Fixed a bug downloading the latest messages

import urllib2
import urllib
import gzip
import os
import json
import sys
import time
import StringIO

__author__ = "Raghav Sood"
__copyright__ = "Copyright 2014"
__credits__ = ["Raghav Sood"]
__license__ = "CC"
__version__ = "1.0"
__maintainer__ = "Raghav Sood"
__email__ = "raghavsood@appaholics.in"
__status__ = "Production"

if len(sys.argv) <= 1:
	print "Usage:\n 	python dumper.py [config file] [conversation ID] [chunk_size (recommended: 2000)] [{optional} offset location (default: 0)]"
	print "Example conversation with Raghav Sood"
	print "	python dumper.py 1075686392 2000 0"
	sys.exit()

try:
	with open(sys.argv[1], 'r+') as infile:
		config = json.load(infile)
except:
	print "Failed to load configuration. Did you specify a proper configuration JSON?"
	sys.exit()

messages = []
talk = sys.argv[2]
offset = int(sys.argv[4]) if len(sys.argv) >= 5 else int("0")
messages_data = '{ "payload" : "empty"}'
json_end_record = "end_of_history"
limit = int(sys.argv[3])
headers = {"origin": "https://www.facebook.com", 
"accept-encoding": "gzip,deflate", 
"accept-language": "en-US,en;q=0.8", 
"cookie": config["cookie"],
"pragma": "no-cache", 
"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.122 Safari/537.36", 
"content-type": "application/x-www-form-urlencoded", 
"accept": "*/*", 
"cache-control": "no-cache", 
"referer": "https://www.facebook.com/messages/zuck"}
base_directory = "Messages/"
directory = base_directory + str(talk) + "/"
pretty_directory = base_directory + str(talk) + "/Pretty/"
fringe_message_timestamp = 0
try:
	os.makedirs(directory)
except OSError:
	pass # already exists

try:
	os.makedirs(pretty_directory)
except OSError:
	pass # already exists

while json_end_record not in json.loads(messages_data)["payload"]: # see if the JSON has a json_end_record key
	data_text = {"messages[user_ids][" + str(talk) + "][offset]": str(offset),
				 "messages[user_ids][" + str(talk) + "][timestamp]": fringe_message_timestamp,
				 "messages[user_ids][" + str(talk) + "][limit]": str(limit),
				 "client": "web_messenger",
				 "__user": config["user"],
				 "__a": config["a"],
				 "__dyn": config["dyn"],
				 "__req": config["req"],
				 "fb_dtsg": config["fb_dtsg"],
				 "ttstamp": config["ttstamp"],
				 "__rev": config["rev"]}
	data = urllib.urlencode(data_text)
	url = "https://www.facebook.com/ajax/mercury/thread_info.php"

	print "Retrieving messages " + str(offset) + "-" + str(limit+offset) + " for conversation ID " + str(talk)
	req = urllib2.Request(url, data, headers)
	response = urllib2.urlopen(req)
	compressed = StringIO.StringIO(response.read())
	decompressedFile = gzip.GzipFile(fileobj=compressed)


	outfile = open(directory + str(offset) + "-" + str(limit+offset) + ".json", 'w')
	messages_data = decompressedFile.read()
	messages_data = messages_data[9:]
	json_data = json.loads(messages_data)
	if json_data is not None and json_data['payload'] is not None:
		try:
			if not messages: # if this is the first batch, insert the whole thing
				messages = json_data['payload']['actions']
			else:
				messages = json_data['payload']['actions'][:-1] + messages # if this isn't the first batch, the final
																	# message was already there in the previous batch
			fringe_message_timestamp = json_data['payload']['actions'][0]['timestamp']
		except KeyError:
			pass #no more messages
	else:
		print "Error in retrieval. Retrying after " + str(config["error_timeout"]) + "s"
		print "Data Dump:"
		print json_data
		time.sleep(config["error_timeout"])
		continue
	outfile.write(messages_data)
	outfile.close()
	command = "python -mjson.tool " + directory + str(offset) + "-" + str(limit+offset) + ".json > " + pretty_directory + str(offset) + "-" + str(limit+offset) + ".pretty.json"
	os.system(command)
	offset = offset + limit
	time.sleep(config["general_timeout"])

finalfile = open(directory + "complete.json", 'wb')
finalfile.write(json.dumps(messages))
finalfile.close()
command = "python -mjson.tool " + directory + "complete.json > " + pretty_directory + "complete.pretty.json"
os.system(command)
