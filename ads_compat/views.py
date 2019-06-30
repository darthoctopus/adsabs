from django.shortcuts import render, redirect
from django.template import loader
import re
import ads

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect

def index(request):
	template = loader.get_template('index.html')
	return HttpResponse(template.render({}, request))

def abstract(request, bibcode):
	# return HttpResponse(f"Viewing abstract for bibcode {bibcode}")
	q = list(ads.query(
		bibcode,
		fl=[
		'bibcode', 'title', 'author', 'aff', 'doi', 'pub',
		'pubdate', 'citation_count', 'abstract', 'arxiv_class',
		'volume', 'issue', 'page', 'year', 'keyword', 'orcid_pub'
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

def qsearch(request, qstring=None):
	if qstring is None:
		try:
			qstring = request.GET['qsearch']
		except:
			return HttpResponseRedirect('/')

	if 'qsort' in request.GET:
		sort = request.GET['qsort']
	else:
		sort = 'classic_factor'

	results = list(ads.query(qstring, fl=[
			'bibcode', 'title', 'author', 'pubdate', 'doi', 'classic_factor'
		], sort=sort))

	if sort == 'classic_factor':
		norm = max(r.classic_factor for r in results)
		for r in results:
			r.classic_factor /= norm / 50
			r.classic_factor += 50

	template = loader.get_template('qsearch.html')
	context = {
	'qstring': qstring,
	'results': results,
	'total': len(results)
	}
	return HttpResponse(template.render(context, request))