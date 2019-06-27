from django import forms
from criptografia.models import Document
from django.conf import settings
import glob
import os
import platform 


class DocumentForm(forms.ModelForm):
    def getName(self):
        list_of_files = glob.glob(settings.MEDIA_ROOT +'/*') # * means all if need specific format then *.csv
        filename =  max(list_of_files, key=os.path.getctime)
    
        if platform.system() == "Windows":
            return filename[filename.rfind("\\")+1:]
        else:
            return filename[filename.rfind("/")+1:]


            
    class Meta:
        model = Document
        fields = ('docfile', )

        