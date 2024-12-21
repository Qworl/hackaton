import asyncio
import asyncpg

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from .models import Record, Feedback, Subcategory
from .forms import RecordForm

async def connect():
    return await asyncpg.connect(user='postgres', password='postgres', database='feedback', host='')

async def get_all_records(search_string):
    conn = await connect()
    record = await conn.fetch('''
        SELECT
            id,
            title,
            text,
            grade,
            feedback_type,
            is_finance,
            subcategory_type
        FROM feedback
        WHERE lower(text collate "en_US") ~ $1 or lower(title collate "en_US") ~ $1;
    ''', search_string)
    await conn.close()
    return record

def search(request):
    name_part = request.GET.get('name_part', '')
    offset = int(request.GET.get('offset', 0))
    limit = 1

    records = asyncio.run(get_all_records(name_part.lower()))

    paginator = Paginator(records, limit)
    page_number = offset // limit + 1
    page_obj = paginator.get_page(page_number)
    print(page_obj.object_list)

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


async def get_record_impl(pk):
    conn = await connect()
    record = await conn.fetchrow('''
        SELECT
            title,
            text,
            grade,
            feedback_type,
            is_finance,
            subcategory_type
        FROM feedback WHERE id = $1;
    ''', pk)
    await conn.close()
    return record


def get_record(request, pk):
    record = asyncio.run(get_record_impl(pk))
    data = {
        'title': record['title'],
        'text': record['text'],
        'grade': record['grade'],
        'feedback_type': Feedback(record['feedback_type']).name if record['feedback_type'] is not None else 'No type',
        'is_finance': record['is_finance'] or False,
        'subcategory_type': Subcategory(record['subcategory_type']).name if record['subcategory_type'] is not None else 'No type',
    }
    return JsonResponse(data)


async def update_record_impl(pk, feedback_type, is_finance, subcategory_type):
    print(pk, feedback_type, is_finance, subcategory_type)
    conn = await connect()
    await conn.execute('''
        UPDATE feedback SET
            feedback_type = $1,
            is_finance = $2,
            subcategory_type = $3,
            is_quailified = true
        WHERE id = $4;
    ''', feedback_type, is_finance, subcategory_type, pk)
    await conn.close()


def update_record(request, pk):
    post_data = request.POST
    feedback_type = Feedback[post_data.get('feedback_type')].value
    is_finance = True if post_data.get('is_finance', 'false').lower() == 'true' else False
    subcategory_type = Subcategory[post_data.get('subcategory_type')].value
    asyncio.run(update_record_impl(pk, feedback_type, is_finance, subcategory_type))
    return HttpResponse(status=204)
