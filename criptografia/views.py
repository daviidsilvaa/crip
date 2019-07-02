from django.shortcuts import render
from django.conf.urls import url
from django.http import HttpResponse
from django.template import engines
from django.template.loader import render_to_string

from cripweb import settings
# import para sistema de arquivos
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.conf import settings
from criptografia.models import Document
from criptografia.forms import DocumentForm
from wsgiref.util import FileWrapper

#import para encrypt/decrypt
import os
import base64
import platform


# Create your views here.
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


def encrypt(request):

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            import glob
            
            symmetric_encrypt(form.getName(),request.POST['password'])

            list_of_files = glob.glob(settings.STATIC_ROOT +'/media/*') 
            filename =  max(list_of_files, key=os.path.getctime)

            if platform.system() == "Windows":
                filename = filename[filename.rfind("\\")+1:]
            else:
                filename = filename[filename.rfind("/")+1:]
            
            
            html = render_to_string('download.html', {'filename': filename})
            return HttpResponse(html)
    else:
        form = DocumentForm()
    return render(request, 'upload.html', { 'form': form })

def decrypt(request):

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            import glob
            
            symmetric_decrypt(form.getName(),request.POST['password'])

            list_of_files = glob.glob(settings.STATIC_ROOT +'/media/*') 
            filename =  max(list_of_files, key=os.path.getctime)

            if platform.system() == "Windows":
                filename = filename[filename.rfind("\\")+1:]
            else:
                filename = filename[filename.rfind("/")+1:]
            
            html = render_to_string('download.html', {'filename': filename})
            return HttpResponse(html)
    else:
        form = DocumentForm()
    return render(request, 'upload.html', { 'form': form })

def download(request):
    import glob
    
    list_of_files = glob.glob(settings.STATIC_ROOT +'/media/*') 
    filepath =  max(list_of_files, key=os.path.getctime)
    
    if platform.system() == "Windows":
        filename = filepath[filepath.rfind("\\")+1:]
    else:
        filename = filepath[filepath.rfind("/")+1:]

    filewrapper = FileWrapper(open(filepath, 'rb'))
    response = HttpResponse(filewrapper, content_type='text/csv')
    response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    return response



#criptografia simetrica (AES)

# retorna apenas o nome do arquivo, sem seu caminho
def correct_filename(filename):
    if platform.system() == "Windows":
        return filename[filename.rfind("\\")+1:]
    else:
        return filename[filename.rfind("/")+1:]

def symmetric_encrypt(filepath, key):

    filename, file_extension = os.path.splitext(filepath)
    filename = correct_filename(filename)
  
    if os.system("openssl enc -aes-256-cbc -salt -in static/media/" + filepath +" -out static/media/" + filepath +".enc -k "+ key) != 0:
        print("Encryption failed!")
        return 
    return True
    
def symmetric_decrypt(filepath, key): 

    filename, file_extension = os.path.splitext(filepath)
    filename = correct_filename(filename)
    print(filepath)
    print(filename)
    if os.system("openssl enc -aes-256-cbc -d -in static/media/" + filepath + " -out static/media/" + filepath +".txt -k "+ key) != 0:
        print("Decryption failed!")
        return (False, "")
        
    return (True, filename+"dec"+file_extension)

#criptografia assimetrica (RSA)

def assymetric_encrypt(filepath, keyfile):
    #key publica
    filename, file_extension = os.path.splitext(filepath)
    filename = correct_filename(filename)

    if os.system("openssl rsautl -encrypt -inkey "+ keyfile +" -pubin -in "+ filepath +" -out "+ filename +"enc.enc") != 0:
        print("Encryption failed!")
        return (False, "")
        
    return (True, filename+"enc.encrypted")

def assymetric_decrypt(filepath, keyfile):
    #key privada
    filename, file_extension = os.path.splitext(filepath)
    filename = correct_filename(filename)

    if os.system("openssl rsautl -decrypt -inkey "+ keyfile +" -in "+ filepath+" -out "+ filename +"dec.txt") != 0:
        print("Decryption failed!")
        return (False, "")
        
    return(True, filename+"dec.txt")
