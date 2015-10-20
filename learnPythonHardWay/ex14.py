#!/usr/bin/env python
# coding=utf-8
from sys import argv
script, user_name,user_id = argv
prompt = '>'
print "Hi %s, I'm the %s script.my_id %s "%(user_name, script, user_id)
print "I'd like to ask you a few questions."
print "Do you like me %s?"%user_name
likes = raw_input(prompt)

print "Where do you live %s?"%user_name
lives = raw_input(prompt)

print "What kind of computer do you have?"
computer = raw_input(prompt)

print """
Alright, so you said %r about liking me.
You live in %r. Not sure where that is.
And you have a %r computer. Nice.
"""%(likes, lives, computer)
