import asyncpg

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .models import Record
from .forms import RecordForm

async def connect():
    return await asyncpg.connect(user='postgres', password='postgres', database='feedback', host='127.0.0.1')

def search(request):
    query = request.GET.get('name_part')
    results = []

    print(query)

    if query:
        # results = Record.objects.filter(name__icontains=query)
        results = [Record(id=1, name='Это точно запись'), Record(id=2, name='Это тоже запись'), Record(id=3, name='Ну и это запись'),]
    print(results)
    return render(request, 'myapp/search.html', {'results': results})
    
def get_record(request, pk):
    record = Record(id=1, name='name', title='title', content='content')
    data = {
        'name': record.name,
        'title': record.title,
        'content': record.content,
    }
    return JsonResponse(data)

def update_record(request, pk):
    print('a')
    post_data = request.POST  # This is also a QueryDict
    title = post_data.get('title')
    content = post_data.get('content')
    print(title, content)
    return HttpResponse(status=204)