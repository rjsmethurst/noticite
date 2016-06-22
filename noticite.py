#############
### Flask app for citation notification
#############

from __future__ import print_function, division, unicode_literals
import numpy as np

from flask import Flask, jsonify, render_template, request, send_file, make_response, json

import httplib
import json
import os
import urllib
from collections import Counter

# Module specific
import ads


app = Flask(__name__)

__author__ = ["Andy Casey <acasey@mso.anu.edu.au>", "Becky Smethurst <rjsmethurst@gmail.com>"]


@app.route('/')
def homepage():
	doi = "2015MNRAS.450..435S"
	paper, papers, scraped_text, no_citations = get_citations(doi)
	return render_template('index.html', paper =paper, text = scraped_text, citations=papers, num=no_citations)

def get_citations(bibcode):
	papers = list(ads.SearchQuery(q=bibcode))
	paper = papers[0]
	no_citations = paper.citation_count
	cite_list =[]
	cite_arxivid = []
	for cite in paper.citation:
		paper_cite = list(ads.SearchQuery(q=cite))
		print paper_cite[0].indentifier
		cite_list.append(paper_cite[0].first_author.split(',')[0]+' et al. '+paper_cite[0].year)
		for entry in paper_cite[0].identifier:
			if re.match("^[0-9]{4}\.+[0-9]{5}", entry):
				cite_arxivid.append(entry)
			else:
				pass
		for entry in cite_arxivid:
			text.append(get_article(entry, first_author=paper[0].first_author, clobber=False))
		else:
			text.append()
	return paper.first_author.split(',')[0]+' et al. '+paper.year, cite_list, text, no_citations 


def get_article(arxiv_id, first_author, clobber=False):
    # Try to load cached file.
	fn = "{0}.tar.gz".format(arxiv_id)
	local = os.path.join(DATA_DIR, fn)

	# Download the remote file.
	if clobber or not os.path.exists(local):
	    url = "http://arxiv.org/e-print/{0}v2".format(arxiv_id)
	    r = requests.get(url)
	    code = r.status_code
	    if code != requests.codes.ok:
	    	url = "http://arxiv.org/e-print/{0}v1".format(arxiv_id)
	    	r = requests.get(url)
	    	code = r.status_code
	    	if code != requests.codes.ok:
	        	print("Download of {0} failed with code: {1}".format(url, code))
	        	return None
	    with open(local, "wb") as f:
	        f.write(r.content)

	tex = []
	if tarfile.is_tarfile(local):
	    with tarfile.open(local) as f:
	        for member in f:
	            if os.path.splitext(member.name)[1] == ".tex":
	                tex.append(f.extractfile(member).read())
	else:
	    with gzip.open(local) as f:
	        tex.append(f.read())

	# Parse the tex files in the archive.
	bib = []
	if tarfile.is_tarfile(local):
	    with tarfile.open(local) as f:
	        for member in f:
	            if os.path.splitext(member.name)[1] == ".bbl":
	                bib.append(f.extractfile(member).read())
	            elif os.path.splitext(member.name)[1] == ".bib":
	                bib.append(f.extractfile(member).read())
	else:
	    with gzip.open(local) as f:
	        bib.append(f.read())

	if len(bib) != 0:
		idx = bib[0].find(first_author)
		bibtext = bib[0][idx:idx+1000].split(']')[1]
		bibref = re.findall("{.*?}", bibtext)[0]
		idxbib = tex[0].find(bibref[1:-1])
		splicetex = tex[0][idxbib-1000:idxbib+1000]
	else:
		idx = tex[0].find(first_author)
		bibtext = tex[0][idx:idx+1000].split(']')[1]
		bibref = re.findall("{.*?}", bibtext)[0]
		idxbib = tex[0].find(bibref[1:-1])
		splicetex = tex[0][idxbib-1000:idxbib+1000]

	return splicetex


print("Found {0} tex file(s)".format(len(tex)))

    return [s for p in map(parse_tex, tex) for s in p if len(s)]

@app.route('/showSignUp')
def showsignup():
	return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signup():
	_name = request.form['inputName']
	_email = request.form['inputEmail']
	_password = request.form['inputDOI']
	if _name and _email and _password:
	    return json.dumps({'html':'<span>All fields good !!</span>'})
	else:
	    return json.dumps({'html':'<span>Enter the required fields</span>'})
	
	
if __name__ == '__main__':
	app.debug = True
	app.run()
