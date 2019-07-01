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
		'volume', 'issue', 'page', 'year', 'keyword', 'orcid_pub',
		'orcid_user'
		]
		))
	assert len(q) == 1, "Non-unique bibcode"
	paper = q[0]

	bibtex = ads.ExportQuery(bibcode).execute()
	try:
		eprint = re.search(r'eprint = \{(.+)\}', bibtex)[1]
	except:
		eprint = None

	orcid = [pub if pub != '-' else auth for pub, auth in zip(paper.orcid_pub, paper.orcid_user)]
	# orcid = [o if o != '-' else other for o, other in zip(orcid, paper.orcid_other)]

	template = loader.get_template('abstract.html')
	context = {
		'paper': paper,
		'eprint': eprint,
		'bibtex': bibtex,
		'authors': zip(paper.author, paper.aff, orcid)
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