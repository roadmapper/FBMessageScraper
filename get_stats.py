import json
import datetime
from pprint import pprint
from collections import defaultdict

id_mapping = {
'fbid:XXXXXXXXX': "John Doe"
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
      if msg["author"] in id_mapping:
        msg_count[id_mapping[msg["author"]]] += 1

print "Message counts per group member: "
print sorted(msg_count.items(), key=getKey, reverse=True)

# Who swears the most adjusted for how often they message?
swear_words = set(["list", "of", "bad", "words"])

swear_count = defaultdict(int)
with open('message_data.json') as msg_data:
    data = json.load(msg_data)
    msgs = data["messages"]
    for msg in msgs:
        text = msg["body"].lower().split()
        for word in text:
            if word in swear_words:
                swear_count[id_mapping[msg["author"]]] += 1


print "Biggest, baddest sailor: "
print sorted(swear_count.items(), key=getKey, reverse=True)

adjusted_swear = {}
for key in swear_count:
    adjusted_swear[key] = 1.0 * swear_count[key] / msg_count[key]

print "Normalized swear count: "
print sorted(adjusted_swear.items(), key=getKey, reverse=True)


# Who's name gets mentioned the most?
names = set(["john", "doe"])

popular = defaultdict(int)
with open('message_data.json') as msg_data:
    data = json.load(msg_data)
    msgs = data["messages"]
    for msg in msgs:
        text = msg["body"].lower().split()
        for word in text:
            if word in names:
                popular[word] += 1

print "Most popular person: "
print sorted(popular.items(), key=getKey, reverse=True)

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
        date_str = datetime.datetime.fromtimestamp(msg["timestamp"]/1000.0).strftime('%Y-%m-%d')
        day_count[date_str] += 1


print "How we send our messages: "
print sorted(device.items(), key=getKey, reverse=True)

print "Our most active days on Facebook: "
print sorted(day_count.items(), key=getKey, reverse=True)[:10]

print "Our least active days on Facebook: "
print sorted(day_count.items(), key=getKey)[1:10]
