from django.db.models import Q
from django.views.generic import TemplateView, ListView
from .models import Ahli
from django.http import HttpResponse
from .twint_full import main_bulk
from .hansard import main_hans
import base64
import pandas as pd
from django_tables2.tables import Table
from django.shortcuts import render
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

class HomePageView(TemplateView):
    template_name = 'home.html'

class SearchResultsView(ListView):
    model = Ahli
    template_name = 'search_results.html'
    
    def get_queryset(self): 
        query = self.request.GET.get('q')
        object_list = Ahli.objects.filter(Q(name__icontains=query) | Q(state__icontains=query))
        return object_list

def external(request):
    #receive input from template home.html
    topic = request.POST.get("topic")
    total = request.POST.get("total")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    handle = request.POST.get("handle")

    #pass parameters into external function
    main_bulk(start_date,end_date,total,topic,handle)

    #these files will be generated by the above code
    word_cloud = 'C:/Users/alter/Documents/djangodb/irdp/output.png'
    most_used = 'C:/Users/alter/Documents/djangodb/irdp/output1.png'
    top_keywords = 'C:/Users/alter/Documents/djangodb/irdp/output2.png'

    #make the image files readable by Django
    with open(word_cloud, 'rb') as binary_file:
        binary_file_data = binary_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        base64_0 = base64_encoded_data.decode('utf-8')
    with open(most_used, 'rb') as binary_file1:
        binary_file_data1 = binary_file1.read()
        base64_encoded_data1 = base64.b64encode(binary_file_data1)
        base64_1 = base64_encoded_data1.decode('utf-8')
    with open(top_keywords, 'rb') as binary_file2:
        binary_file_data2 = binary_file2.read()
        base64_encoded_data2 = base64.b64encode(binary_file_data2)
        base64_2 = base64_encoded_data2.decode('utf-8')

    #pass the images into a render along with the template
    return render(request, 'external.html',{'base64_0': base64_0,'base64_1':base64_1, 'base64_2' : base64_2})

def external_test(request):
    #receive pdf as input
    data = request.FILES["myfile"]
    path = default_storage.save('irdp\somename.pdf', ContentFile(data.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    #process it with external script
    main_hans(tmp_file,'irdp\Stopwords.txt','irdp\MP_Names.csv')
    #get the processed csv file and pass it to the template
    data = pd.read_csv('irdp\Tokenized_Hansard.csv')
    data_html = data.to_html()
    context = {'loaded_data': data_html}
    os.remove(tmp_file)
    return render(request, "test.html", context)