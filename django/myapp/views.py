import asyncpg

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from .models import Record
from .forms import RecordForm

async def connect():
    return await asyncpg.connect(user='postgres', password='postgres', database='feedback', host='127.0.0.1')

def search(request):
    name_part = request.GET.get('name_part', '')
    offset = int(request.GET.get('offset', 0))
    limit = 1

    records = [Record(id=1, name='Это точно запись'), Record(id=2, name='Это тоже запись'), Record(id=3, name='Ну и это запись'),]

    paginator = Paginator(records, limit)
    page_number = offset // limit + 1
    page_obj = paginator.get_page(page_number)

    page_offsets = [(i - 1) * limit for i in paginator.page_range]
    pages_data = [(x, y) for x, y in zip(page_obj.paginator.page_range, page_offsets)]

    context = {
        'records': page_obj,
        'name_part': name_part,
        'offset': offset,
        'total_count': paginator.count,
        'pages_data': pages_data,
    }

    return render(request, 'myapp/search.html', context)
    
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
    post_data = request.POST
    title = post_data.get('title')
    content = post_data.get('content')
    print(title, content)
    return HttpResponse(status=204)