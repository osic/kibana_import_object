# Kibana Objects Import

Imports Kibana visualizations, searches, and dashboards to be used by others or migrated.

1. Clone this repo in your ES environment
2. Make sure relevant dashboard, visualizations, searches are exported and location is noted
3. Customize elk.cnf folder for location of exports (file name and location) if you choose to pull from here
4. run - python import_objects.py - No parameters means it will just pull from the config file
 
You can also specify parameters in the command.

    python import_objects.py -s json/search.json -d json/dashboard.json -v json/visual.json

You should then see that it imports all of the ojects specified.  This was written to be a part of a bigger script.  But can still be used and customized as needed.

**More to add.  Still WIP**
