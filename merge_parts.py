import os
import json

def main():
    if len(sys.argv) <= 1:
        print "Usage:\n         python merge_parts.py [conversation ID]"
        print "Use if the complete JSON fails to be assembled"
        print " python merge_parts.py 1075686392"
        sys.exit()

    talk = sys.argv[1]
    
    base_directory = "Messages/"
    directory = base_directory + str(talk) + "/"
    pretty_directory = base_directory + str(talk) + "/Pretty/"

    messages = []

    for directory, subdirectories, files in os.walk(directory):
        
        for file in files:
            if 'pretty' not in os.path.join(directory, file):
                print "Loading " + file
                with open(os.path.join(directory, file)) as data_file:    
                    json_data = json.load(data_file)
                    if 'end_of_history' not in json_data['payload']:
                        messages = messages + json_data['payload']['actions']

    finalfile = open(directory + "complete.json", 'wb')
    print "Merging all files into one file..."
    finalfile.write(json.dumps(messages))
    print "Merged"
    finalfile.close()
    command = "python -mjson.tool " + directory + "complete.json > " + pretty_directory + "complete.pretty.json"
    print "Creating a pretty version of the complete JSON..."
    os.system(command)
    print "Created pretty version"


if __name__ == '__main__':
    main()
