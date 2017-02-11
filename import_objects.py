import json
import requests
import argparse
import subprocess

from ConfigParser import SafeConfigParser


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self):
        desc = "Accepts search, dashboard, and visualization json from Kibana.  Pushes to ES."
        usage_string = "[-s/--search] ([-d/--dashboard] | [-v/--visual]) [-o/--output-file]  [-u/--url] [-i/--index]"

        super (ArgumentParser, self).__init__(
            usage=usage_string, description=desc)

        self.add_argument(
            "-s", "--search", metavar="<json file with searches>",
            required=False, default=None)

        self.add_argument(
            "-d", "--dashboard", metavar="<json file with dashboards>",
            required=False, default=None)

        self.add_argument(
            "-r", "--remove",
            required=False, default=None)

        self.add_argument(
            "-v", "--visual", metavar="<json file with visualizations>",
            required=False, default=None)

        self.add_argument(
            "-u", "--url", metavar="<host url where ES lives>",
            required=False, default=None)

        self.add_argument(
            "-o", "--output-file", metavar="<path to output file>",
            required=False, default=None)

        self.add_argument(
            "-i", "--index", metavar="<add new index to ES>",
            required=False, default=None)

        self.add_argument(
            "-l", "--ilist",
            required=False, default=None, action='store_true')

        self.add_argument(
            "-m", "--mapping", metavar="<add mapping for index>",
            required=False, default=None)

        self.add_argument(
            "-p", "--pattern", metavar="<add mapping for index>",
            required=False, default=None)


def entry_point():

    cl_args = ArgumentParser().parse_args()

    # Initialize Config Variables
    config = SafeConfigParser()
    config.read("elk.cnf")
    host = cl_args.url or config.get("kibana", "host")
    host2 = cl_args.url or config.get("kibana", "host2")
    visuals_json = cl_args.visual or config.get("kibana", "visualizations")
    dashboards_json = cl_args.dashboard or config.get("kibana", "dashboards")
    searches_json = cl_args.search or config.get("kibana", "searches")

    #Import Visualizations
    if visuals_json:
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
    if dashboards_json:
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
    if searches_json:
        with open(searches_json) as data_file:
            print "Searches Start"
            data = json.load(data_file)

        for i in data:
            name = i['_id']
            data = json.dumps(i['_source'])
            url = host + 'search/' + name
            response = requests.put(url, data=data)
            print 'Search Status: ' + str(response)

    #Show list of indexes
    if cl_args.ilist:
        url = host2 + '_cat/indices?v'
        response = requests.get(url)
        print response.text

    #Add new index and index pattern
    if cl_args.index and cl_args.mapping:
        print "Working on Index"
        subprocess.call(["curl -X PUT http://localhost:9200/" + cl_args.index + " -T " + cl_args.mapping], shell=True)
        if cl_args.pattern:
            subprocess.call(["curl -X PUT http://localhost:9200/" + cl_args.index + "/index-pattern/" + cl_args.index + " -T " + cl_args.pattern], shell=True)
        print "/nIndex Created"
    elif cl_args.index:
        print "Please provide index name and index mapping to create index"

    #Delete index
    if cl_args.remove:
        print "Deleting Index"
        url = host2 + cl_args.remove + '?pretty'
        response = requests.delete(url)
        print response.text

if __name__ == "__main__":
    entry_point()
