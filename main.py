
from django.conf.urls import url
from django.http import HttpResponse
from django.template import engines
from django.template.loader import render_to_string

# import para sistema de arquivos
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
from models import Document
from forms import FileForm

DEBUG = True
SECRET_KEY = '4l0ngs3cr3tstr1ngw3lln0ts0l0ngw41tn0w1tsl0ng3n0ugh'
ROOT_URLCONF = __name__
TEMPLATES = [
	{	'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [ '/home/david/git/crip/template/' ],
	},
]

def home(request):
	title = 'Crip Files Homepage'
	author = 'David e Gabriel'
	html = render_to_string('home.html', {'title': title, 'author': author})
	return HttpResponse(html)

def about(request):
	title = 'about'
	author = 'David e Gabriel'
	html = render_to_string('about.html', {'title': title, 'author': author})
	return HttpResponse(html)

	def list(request):
		# manuseia upload de arquivo
		if request.method == 'POST':
			form = DocumentForm(request.POST, request.FILES)
			if form.is_valid():
				newdoc = Document(docfile = request.FILES['docfile'])
				newdoc.save()

				return HttpResponseRedirect(reverse('list'))
		else:
			form = DocumentForm()

		documents = Document.objects.all()

		return render(request, 'list.html', {'documents': documents, 'form': form})

urlpatterns = [
    url(r'^$', home, name='homepage'),
    url(r'^about/$', about, name='aboutpage'),
	url(r'^list/$', list, name='list'),
]
