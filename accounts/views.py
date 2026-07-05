from django.shortcuts import render, redirect
from .forms import CustomLoginForm, CustomRegisterForm, ProfileForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.views.decorators.http import require_http_methods


def register(request):
    if request.user.is_authenticated : # بدون اقواس 
        return redirect('pages:home')

    if request.method =='POST' :
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save() #دالة save الخاصة به
            #لم اعمل login حتي يذهب الي دالتها الاول  وقد يتم انتقاله لو عملت لو كتبتها في settings
            messages.success(request, 'تم انشاء مستخدم بنجاح')
            return redirect('accounts:login')
        else :
            messages.error(request, 'فشل انشاء المستخدم لعدم صحة البيانات ')

    else :
        form = CustomRegisterForm()

    return render(request, 'registration/register.html', {'form' : form})

def custom_login(request):

    if request.user.is_authenticated :
        return redirect('pages:home')

    if request.method == 'POST':
        form = CustomLoginForm(request, request.POST) ##لانها مش ModelForm
        if form.is_valid():
            user = form.get_user() ##حصل authenticate تلقائي في الفورم

            if form.cleaned_data.get('remember_me'):  #form .يبقي الحقل نفسه انما form.cleaned_data يبقي القيمة 
                request.session.set_expiry(1209600)
            else :
                request.session.set_expiry(0)

            login(request,user)
            messages.success(request, 'تم تسجيل الدخول بنجاح')
            return redirect('pages:home')
        else :
            messages.error(request,'فشل تسجيل الدخول لعدم صحة البيانات')
    
    else :
        form = CustomLoginForm()#لا بعرض ولا يعمل اي شى
    
    return render(request, 'registration/login.html', {'form':form})

@login_required
def profile(request):

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'تم حفظ التغييرات بنجاح')
            return redirect('accounts:profile')  ###عملتها هنا علشان PRG pattern POST redirect GET  حتي يكون ىخر طلب GETعلشان لو عمل اعادة ارسال والافضل ترجعه بعد التحديث الي صفحتها ليري نتيجة التحديث غير الانشاء ممكن نوديه لصفحة ثانية
        else :
            messages.error(request, 'فشل حفظ التغييرات لعدم صحة البيانات')
    else :
        form = ProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form':form})

@login_required
@require_http_methods(['POST'])
def custom_logout(request):

    logout(request)
    return render(request, 'registration/logged_out.html')

