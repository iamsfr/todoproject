from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import *
from .forms import TodoForm

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView

class TasklistView(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'task'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'details.html'
    context_object_name = 'task'

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name', 'priority', 'date')

    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')




# Create your views here.
def home(request):
    task1 = Task.objects.all()
    if request.method =='POST':
        task = request.POST.get('task','')
        priority = request.POST.get('priority','')
        date    = request.POST.get('date','')
        tasks = Task(name=task, priority=priority,date=date)
        tasks.save()

    return render(request, 'home.html',{'task':task1})

def delete(request,id):
    task = Task.objects.get(id=id)
    if request.method =='POST':
        task.delete()
        return redirect('/')
    return render(request, 'delete.html')

def update(request,id):
    task = Task.objects.get(id=id)
    form = TodoForm(request.POST or None,instance=task)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'edit.html',{'form':form,'task':task})
    
