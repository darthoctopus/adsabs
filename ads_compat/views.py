from django.shortcuts import render
from django.template import loader
import re
import ads

# Create your views here.

from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello World")

def abstract(request, bibcode):
	# return HttpResponse(f"Viewing abstract for bibcode {bibcode}")
	q = list(ads.query(
		bibcode,
		fl=[
		'bibcode',
		'title',
		'author',
		'aff',
		'doi',
		'pub',
		'pubdate',
		'citation_count',
		'abstract',
		'arxiv_class',
		'volume',
		'issue',
		'page',
		'year',
		'keywords',
		'orcid_pub'
		]
		))
	assert len(q) == 1, "Non-unique bibcode"

	bibtex = ads.ExportQuery(bibcode).execute()

	eprint = re.search(r'eprint = \{(.+)\}', bibtex)[1]

	template = loader.get_template('abstract.html')
	context = {
		'paper': q[0],
		'eprint': eprint,
		'bibtex': bibtex,
		'authors': zip(q[0].author, q[0].aff, q[0].orcid_pub)
	}
	return HttpResponse(template.render(context, request))