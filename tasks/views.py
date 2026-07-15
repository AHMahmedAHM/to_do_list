from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm, CategoryForm
from .models import Task 
from django.contrib.auth.decorators import login_required
from django.contrib import messages 

##هل لو عاوز اي حد يقدر يستخدمها احوش الديكور واعمل ال user im model null,blank 
@login_required 
def tasks_list(request):
    tasks = Task.objects.filter(user=request.user)
    context ={
        'tasks' : tasks,
        'tasks_complete' : tasks.filter(status='complete'),
        'tasks_doing' : tasks.filter(status='doing'),
        'tasks_later' : tasks.filter(status='later'),
    }

    return render(request, 'tasks/tasks_list.html', context)


@login_required###محتاجها في كل دالة لاني بفلتر علي اساس المستخدن 
def task_details(request, slug):
    
    task = get_object_or_404(Task, user=request.user, slug=slug)
    # اي get يبقي فيه except or get_object_or_404
    
    context ={
        'task' : task
    }

    return render(request, 'tasks/task_details.html', context)


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, user=request.user) ##لاتنس محتاج الuser لفلترة الاقسام 
        if form.is_valid(): #يستدعي الclean
            task = form.save(commit=False)
            #شوف الحقول اللي لسه لم تضاف يدويا او تلقائيا 
            task.user = request.user
            task.save()
            return redirect('tasks:tasks_list') #PRG pattern 
    else :
        form =TaskForm(user=request.user) #اعطيها البارميتر بتاعتعلشان الفلترة سواء العرض او الارسال 
    
    context ={
        'form' : form,
    }

    return render(request, 'tasks/add_task.html', context)


@login_required
def add_category(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST, user=request.user)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user #حقل في الموديل وليس في الفورم وغير تلقائي
            category.save()
            return redirect('tasks:add_task') #PRG pattern
    else :
        form = CategoryForm(user=request.user)
    
    context={
        'form' : form
    }

    return render(request, 'tasks/add_category.html', context)


@login_required
def change_status(request, slug):
    task = get_object_or_404(Task, slug=slug, user=request.user)
    if task.status != 'later': #علشان لو لسه لم ابدا تنفيذ لا تتحدث حتي لا تنزل تحت 
        if task.status == "complete" :
            task.status ='doing'
            messages.warning(request, 'تم الغاء اكتمال المهمة والمهمة اصبحت بالاسفل')
    

        elif task.status =="doing" :
            task.status ='complete'
    
        task.save() #فكرة الupdate كلها هنا 
    return redirect('tasks:tasks_list')


