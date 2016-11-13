import json
import requests
import argparse

from ConfigParser import SafeConfigParser

# Initialize Config Variables
config = SafeConfigParser()
config.read("elk.cnf")
host = config.get("kibana", "host")
visuals_json = config.get("kibana", "visualizations")
dashboards_json = config.get("kibana", "dashboards")
searches_json = config.get("kibana", "searches")

#Import Visualizations
with open(visuals_json) as data_file:
    print "Visualizations Start"
    data = json.load(data_file)

for i in data:
    name = i['_id']
    data = json.dumps(i['_source'])
    url = host + 'visualization/' + name
    response = requests.put(url, data=data)
    print 'Visualization Status: ' + str(response)

#Import Dashboards
with open(dashboards_json) as data_file:
    print "Dashboard Start"
    data = json.load(data_file)

for i in data:
    name = i['_id']
    data = json.dumps(i['_source'])
    url = host + 'dashboard/' + name
    response = requests.put(url, data=data)
    print 'Dashboard Status: ' + str(response)

#Import Searches
with open(searches_json) as data_file:
    print "Searches Start"
    data = json.load(data_file)

for i in data:
    name = i['_id']
    data = json.dumps(i['_source'])
    url = host + 'search/' + name
    response = requests.put(url, data=data)
    print 'Search Status: ' + str(response)
