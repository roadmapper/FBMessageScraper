import json
from pprint import pprint
from collections import defaultdict

id_mapping = {
'fbid:706676557': "Rogges",
'fbid:584246322': "Vinoth",
'fbid:100003250438654': "Aushvin",
'fbid:100003581697251': "Thannoj",
'fbid:1112575489': "Janusshan",
'fbid:1345872565': "Arrjun",
'fbid:531215673': "Ali Nawed",
'fbid:1184441679': "Ewan",
'fbid:612562487': "Keerthijan",
'fbid:100003725285733': "Harris",
'fbid:100000361213110': "Pavi",
'fbid:747570870': "Javed",
'fbid:100002441596551': "Kishan",
'fbid:667097178': "Maaz",
'fbid:776766826': "Hamza",
'fbid:1031445696': "Sabil",
'fbid:1070425055': "Saad"
}

def getKey(item):
	return item[1]

# Who sends the most messages?

msg_count = defaultdict(int)
with open('message_data.json') as msg_data:
	data = json.load(msg_data)
	msgs = data["messages"]
	print "Total Messages: " + str(len(msgs))
	for msg in msgs:
		msg_count[id_mapping[msg["author"]]] += 1

print "Message Counts: "
print sorted(msg_count.items(), key=getKey, reverse=True)



# Who swears the most adjusted for how often they message?

swear_words = set(["replace with list of swear words"])

# How often do each of us say "bro" adjusted for how often they message?
# Should have used regex in hindsight
bros = set(["bro", "broo", "brooo", "broooo", "brooooo",
 "broooooo", "brooooooo", "broooooooo", "brooooooooo", "broooooooooo"])

swear_count = defaultdict(int)
bro_count = defaultdict(int)
with open('message_data.json') as msg_data:
	data = json.load(msg_data)
	msgs = data["messages"]
	for msg in msgs:
		text = msg["body"].lower().split()
		for word in text:
			if word in swear_words:
				swear_count[id_mapping[msg["author"]]] += 1
			if word in bros:
				bro_count[id_mapping[msg["author"]]] += 1


print "Biggest, baddest sailor: "
print sorted(swear_count.items(), key=getKey, reverse=True)

adjusted_swear = {}
for key in swear_count:
	adjusted_swear[key] = 1.0 * swear_count[key] / msg_count[key]

print "Normalized swear count: "
print sorted(adjusted_swear.items(), key=getKey, reverse=True)

print "Biggest Bro: "
print sorted(bro_count.items(), key=getKey, reverse=True)

adjusted_bro = {}
for key in bro_count:
	adjusted_bro[key] = 1.0 * bro_count[key] / msg_count[key]

print "Normalized bro count: "
print sorted(adjusted_bro.items(), key=getKey, reverse=True)

# Who's name gets mentioned the most?

names = set(["ali", "javed", "nawed", "rogges", "janu",
 "janusshan", "av", "aushvin", "saad", "hamza",
 "pavi", "arrjun", "harris", "haris", "kishan",
 "kish", "sabil", "daas", "thannoj", "yeaser", "maaz", "vinoth"])

# Which school do we talk about the most?

schools = set(["waterloo", "uoft", "york", "schulich",
 "ryerson", "uwaterloo", "utoronto", "utsc", "utsg",
 "uw", "queens"])

popular = defaultdict(int)
school_count = defaultdict(int)
with open('message_data.json') as msg_data:
	data = json.load(msg_data)
 	msgs = data["messages"]
 	for msg in msgs:
 		text = msg["body"].lower().split()
 		for word in text:
 			if word in names:
 				popular[word] += 1
 			if word in schools:
 				school_count[word] += 1

print "Most popular person: "
print sorted(popular.items(), key=getKey, reverse=True)

print "Most popular school: "
print sorted(school_count.items(), key=getKey, reverse=True)


# Percentage of the time ppl message from web/messenger?
# Pie chart would be perfect for this
device = defaultdict(int)

# What was our most active day on facebook?
day_count = defaultdict(int)
with open('message_data.json') as msg_data:
	data = json.load(msg_data)
	msgs = data["messages"]
	for msg in msgs:
		device[msg["source"]] += 1
		day_count[msg["timestamp_absolute"]] += 1


print "How we send our messages: "
print sorted(device.items(), key=getKey, reverse=True)

print "Our most active days on Facebook: "
print sorted(day_count.items(), key=getKey, reverse=True)[:10]

print "Our least active days on Facebook: "
print sorted(day_count.items(), key=getKey)[1:10]
