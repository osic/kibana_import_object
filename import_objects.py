import json
import requests
import argparse

from ConfigParser import SafeConfigParser


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self):
        desc = "Accepts search, dashboard, and visualization json from Kibana.  Pushes to ES."
        usage_string = "[-s/--search] ([-d/--dashboard] | [-v/--visual]) [-o/--output-file]  [-h/--host]"

        super (ArgumentParser, self).__init__(
            usage=usage_string, description=desc)

        self.add_argument(
            "-s", "--search", metavar="<json file with searches>",
            required=False, default=None)
            
        self.add_argument(
            "-d", "--dashboard", metavar="<json file with dashboards>",
            required=False, default=None)
            
        self.add_argument(
            "-v", "--visual", metavar="<json file with visualizations>",
            required=False, default=None)
            
        self.add_argument(
            "-h", "--host", metavar="<host url where ES lives>",
            required=False, default=None)

        self.add_argument(
            "-o", "--output-file", metavar="<path to output file>",
            required=False, default=None)


def entry_point():

    cl_args = ArgumentParser().parse_args()

    # Initialize Config Variables
    config = SafeConfigParser()
    config.read("elk.cnf")
    host = cl_args.host or config.get("kibana", "host")
    visuals_json = cl_args.visual or config.get("kibana", "visualizations")
    dashboards_json = cl_args.dashboard or config.get("kibana", "dashboards")
    searches_json = cl_args.search or config.get("kibana", "searches")

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


if __name__ == "__main__":
    entry_point()