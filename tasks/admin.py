from django.contrib import admin
from .models import Task, Category

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'status', 'created_at', 'is_done_before_time', 'user', 'category']
    #fields الحقول التي تظهر بالداخل 
    list_select_related = ['user', 'category'] #عندما نستخدم حقل علاقة داخل list_display
    readonly_fields = ['created_at','updated_at']
    search_fields =['user__username', 'category__name'] #مقدرشي اعمل استعلام__الا في search
    date_hierarchy = 'created_at'
    list_filter = ['created_at']

    def is_done_before_time (self,obj):
        from django.utils import timezone
        #الاحدث يعني الاكبر 
        if obj.due_time and obj.due_time > timezone.now().date() and obj.status =='complete' :
            return True 
        return False 
    is_done_before_time.boolean = True # علشان يقوله ده قيمة boolean ويعمل صح وخطا
    is_done_before_time.short_description ='هل تمت قبل الوقت'

    def display_name(self, obj):
        if  obj.name and len(obj.name) > 15:
            return obj.name[:13] +'..'
        else :
            return obj.name
    display_name.short_description = 'name'




@admin.register(Category) #اقدر اعلم اكتر من واحدة داخل القوس والclass تحتهم يكون للاثنين ولكن نادر 
class CategoryAdmin(admin.ModelAdmin):
    list_display =['name','user'] #user فقط سيظهر ارقام لا لا لا سيظهر الstr  نحتاج الاستعلام في search
    list_select_related = ['user']
    search_fields = ['user__username', 'name']# مقدرشي اعلم استعلام __الا في search 
    
