from django.shortcuts import render, get_object_or_404, redirect
from .models import Record
from .forms import RecordForm

def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        # results = Record.objects.filter(name__icontains=query)
        results = [Record(id=1, name='Это точно запись'), Record(id=1, name='Это тоже запись'), Record(id=1, name='Ну и это запись'),]
    return render(request, 'myapp/search.html', {'results': results})

def edit_record(request, record_id):
    record = get_object_or_404(Record, id=record_id)
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('search')
    else:
        form = RecordForm(instance=record)
    return render(request, 'myapp/edit_record.html', {'form': form})