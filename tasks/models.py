from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone


UserModel = get_user_model()

def image_path(instance, filename):
    ext = filename.split('.')[-1]
    now = timezone.now() #علشان  TZ
    # Y capital 
    path = f'tasks/{now:%Y/%m/%d}/{instance.user_id}.{ext}' #لا تكرر /قبل y واختار حقل معمول من البداية كحقل العلاقة _id علشان ناخد الرقم مش الراجع__str__
    return path



class Task(models.Model):
    
    #قاعدة البيانات الاول وبعد كده اللي هيظهر 
    STATUS_CHOICES=(
        ('complete','تمت'),
        ('doing','قيد التنفيذ'),
        ('later','فيما بعد'),
    )


    name = models.CharField(max_length=50)
    description = models.TextField(blank=True) #كيف نعلم blank  غير null علشان Char,Text Field لو مكتبشي حاجة ترجع '' مش null
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    image = models.ImageField(blank=True, upload_to=image_path) #مش هعمل null علشان لو معملشي صورة اعمر صورة افتراضية علش شكل الحرف ، لا تعمل ()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_time = models.DateField(null=True, blank=True)
    slug = models.SlugField(blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True,blank=True,  related_name='tasks')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='tasks')

    class Meta :
        constraints =[
            models.UniqueConstraint(fields=['slug', 'user'], name='unique_slug_per_user' ),
        ]
        ordering = ['-updated_at']

    def get_absolute_url(self):
        return reverse('tasks:task_details', kwargs={'slug':self.slug})

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        #ممكن اعمل وخلاص self.slug=slugify(self.name)
        if not self.slug:
            self.slug = slugify(self.name)
        elif self.pk : #  يعني تعديل ليس انشاء
            old_name = self.__class__.objects.filter(pk=self.pk).first().name
            if old_name != self.name : #self.name الجديد
                self.slug = slugify(self.name) ##تحديث الslugبالاسم الجديد سؤاء غيره ام لا 

        super().save(*args,**kwargs) # لازم نحطها علشان منطقهم بس حطها فيةالاخر بعد التعديل قبل ما هي تحفظ 



class Category(models.Model):
    name = models.CharField(max_length=20)
    # لان هذه الاقسام خاصة بكل مستخدم 
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='categories')
    
    class Meta :
        constraints=[
            ## علشان نعمل واحد مش لكل النشروع انما واحد لكل مستخدم 
            models.UniqueConstraint(fields=('name', 'user'), name='unique_category_per_user'),
        ]

    def __str__(self):
        return self.name
    
