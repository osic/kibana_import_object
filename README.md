# Kibana Objects Import

Imports Kibana visualizations, searches, and dashboards to be used by others or migrated.

1. Clone this repo in your ES environment
2. Export relevant dashboard, visualizations, searches vi Kibana UI
3. Save them in the json folder with respective name (see elk.cnf for name)
4. run python import_objects.py

You should then see that it imports all of the ojects specified.  This was written to be a part of a bigger script.  But can still be used and customized as needed.
