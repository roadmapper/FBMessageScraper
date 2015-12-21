This is  a fork of the following repository: [https://github.com/RaghavSood/FBMessageScraper](https://github.com/RaghavSood/FBMessageScraper).

Here's a changelog, as compared to that repository's commit 4e3f268:
* This version now uses configuration files instead of hardcoded values
* Fixed a bug detecting the end_of_history mark
* Fixed a bug downloading the latest messages (these were probably caused by Facebook adjusting the format of their response JSONs)
* Added a file text_printer.py to print the contents of the JSON dump.

To use text_printer.py, do: `python text_printer.py {configuration_file}, {id}`. (Only do this after performing the steps in the original instructions.)

Here follow the original instructions:

Facebook Message Scraper
========================

A simple python script to download the entire conversation from Facebook, not limited like the one in the data dump provided by Facebook

Outputs the conversation in a JSON format, as well as the JSON for each individual chunk.

Initial Setup
=============

Run for both `dumper.py` and `group_dumper.py`

1. In Chrome, open [facebook.com/messages](https://www.facebook.com/messages/) and open any conversation with a fair number of messages
2. Open the network tab of the Chrome Developer tools
3. Scroll up in the conversation until the page attempts to load previous messages
4. Look for the POST request to [thread\_info.php](https://www.facebook.com/ajax/mercury/thread_info.php)
5. You need to copy certain parameters from this request into the python script to complete the setup:
  1. Set the `cookie` value to the value you see in Chrome under `Request Headers`
  2. Set the `__user` value to the value you see in Chrome under `Form Data` 
  3. Set the `__a` value to the value you see in Chrome under `Form Data`
  4. Set the `__dyn` value to the value you see in Chrome under `Form Data`
  5. Set the `__req` value to the value you see in Chrome under `Form Data`
  6. Set the `fb_dtsg` value to the value you see in Chrome under `Form Data`
  7. Set the `ttstamp` value to the value you see in Chrome under `Form Data`
  8. Set the `__rev` value to the value you see in Chrome under `Form Data`

You're now all set to start downloading messages.

Downloading Messages
====================

1. Get the conversation ID for those messages by opening [http://graph.facebook.com/{username-of-chat-partner}](http://graph.facebook.com/{username_of_chat_partner}). *Edit. This method no longer works. Click on their profile picture, and check the URL. The last sequence of numbers (10 digits) is their Facebook ID.*
2. Copy the `id` value from there
3. For group conversations, the ID can be retrieved from the messages tab, as part of the URL. You must use `group_dumper.py` instead.
4. Run the command `python dumper.py {id} 2000`, and put the value you retrieved for ID earlier. *Edit: Also specify a configuration file: the command will be: `python dumper.py {configuration file} {id} 2000`*

Messages are saved by default to `Messages/{id}/`

Known Issues
============

The script sometimes has trouble with very large conversations (>100k messages). Facebook seems to rate limit this, and returns empty responses. In such cases, the script will retry after 30s until it gets a valid response.

It may take the script several tries to get a valid response. DO NOT PANIC.

Interrupting the execution before completion only leaves the JSON chunks, not the stitched file.
