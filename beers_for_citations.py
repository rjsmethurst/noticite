# coding: utf-8

""" Beers for citations. The new underground currency. """

__author__ = "Andy Casey <acasey@mso.anu.edu.au>"

# Standard library
import httplib
import json
import os
import urllib
from collections import Counter

# Module specific
import ads

# Couple of mutable variables for the reader
author_query = "^Casey, Andrew R."
records_filename = "citations.json"

my_papers = ads.search(author_query)

# How many citations did we have last time this ran?
if not os.path.exists(records_filename):
    all_citations_last_time = {"total": 0}

else:
    with open(records_filename, "r") as fp:
        all_citations_last_time = json.load(fp)

# Build a dictionary with all of our citations
bibcodes, citations = zip(*[(paper.bibcode, paper.citation_count) 
    for paper in my_papers])

all_citations = dict(zip(bibcodes, citations))
all_citations["total"] = sum(citations)

# Check if we have more citations than last time, but only if we have run 
# this script beforehand, too. Otherwise we'll get 1,000 notifications on
# the first time the script has been run
if  all_citations["total"] > all_citations_last_time["total"] \
and len(all_citations_last_time) > 1:

    # Someone has cited us since the last time we checked.
    newly_cited_papers = {}
    for bibcode, citation_count in zip(bibcodes, citations):

        new_citations = citation_count - all_citations_last_time[bibcode]

        if new_citations > 0:
            # Who were the first authors for the new papers that cited us?
            citing_papers = ads.search("citations(bibcode:{0})"
                .format(bibcode), rows=new_citations)
            newly_cited_papers[bibcode] = [paper.author[0] for paper in citing_papers]

    # Ok, so now we have a dictionary (called 'newly_cited_papers') that contains 
    # the bibcodes and names of authors who we owe beers to. But instead, we
    # would like to know how many beers we owe, and who we owe them to.
    beers_owed = Counter(sum(newly_cited_papers.values(), []))

    # Let's not buy ourself beers.
    if my_papers[0].author[0] in beers_owed:
        del beers_owed[my_papers[0].author[0]]

    for author, num_of_beers_owed in beers_owed.iteritems():

        readable_name = " ".join([name.strip() for name in author.split(",")[::-1]])
        this_many_beers = "{0} beers".format(num_of_beers_owed) \
            if num_of_beers_owed > 1 else "a beer"
        message = "You owe {0} {1} because they just cited you!"
            .format(readable_name, this_many_beers)

        print(message)

        if not "PUSHOVER_TOKEN" in os.environ \
        or not "PUSHOVER_USER" in os.environ:
            print("No pushover.net notification sent because PUSHOVER_TOKEN or"
                " PUSHOVER_USER environment variables not found.")
            continue

        conn = httplib.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
          urllib.urlencode({
            "token": os.environ["PUSHOVER_TOKEN"],
            "user": os.environ["PUSHOVER_USER"],
            "message": message
          }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()

else:
    print("No new citations!")

# Save these citations
with open(records_filename, "w") as fp:
    json.dump(all_citations, fp)
