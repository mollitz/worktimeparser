#!/usr/bin/env python
from icalendar import Calendar, Event
import re
import datetime
import time
import math
import urllib

#This is my google calendar. its not thaat private now.. :)
path="https://www.google.com/calendar/ical/7v0jd6afcg2fohiv5gmlbgpq8o%40group.calendar.google.com/private-716809bafd66f98b017bd6ebd7eb2ea4/basic.ics"
weekly_hours = 14*60*60
first_week = 1354489200


""" Returns the worktime in seconds of the given ical event """
def parseEvent(event):
  try:
    print event
    #import ipdb; ipdb.set_trace()
    m = re.search('(\d+)', event['SUMMARY'].title())
    start = time.mktime(event['DTSTART'].dt.timetuple())
    end = time.mktime(event['DTEND'].dt.timetuple())
    t = end-start
    if m:
      t -= int(m.group(0))*60
    return end, t
  except KeyError:
    return 0, None
  

if __name__ == '__main__':
  # give a monthly overview(Month: Hours) and lastly print the hours i miss or ive overdone for my weekly_hours schedule
  content = urllib.urlopen(path).read()
  cal = Calendar.from_ical(content)
  events = cal.walk()[1:]
  s = 0
  last = 0
  for e in events:
    lasttmp, tmp = parseEvent(e)
    last = max(lasttmp, last)
    s += tmp

  print "You worked " + str(s) + " seconds."
  weeks = math.ceil((last-first_week)/(60*60*24*7))
  print "That is " + str(weeks) + " weeks."
  print "That is " + str (float(s)/(weeks*60*60)) + " hours per week in average."
  overflow_time = (s-(14*60*60*weeks))/(60*60)
  if overflow_time > 0:
    print "In total you worked " + str(overflow_time) + " hours to much."
  else:
    print "You need to work " + str(overflow_time) + " hours to get to your 14 hours/week in average."

  

  
  
