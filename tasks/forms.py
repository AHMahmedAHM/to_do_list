from django import forms 
from .models import Task, Category


class TaskForm (forms.ModelForm):
    class Meta :
        model =Task
        ### فيه حقول لم تكتب  اذن تملا تلقائي او  يدوي  
        fields = ['name', 'description', 'status', 'image', 'due_time', 'category']
        widgets ={
            'description' : forms.Textarea(attrs={'rows' : 3}),
            'status' : forms.Select(),
            'image' : forms.FileInput(attrs={'accept':'image/*'}),
            'due_time' : forms.DateInput(attrs={'type':'date'}),
            'category' : forms.Select(),
        }
    #لجعل ال category خاصة بال user فقط لانها الان تبع المشروع ككل 
    def __init__(self, *args, user=None, **kwargs): ##### اي parameter تضيفه في حاجة وارثة يكون بعد الargs كده هيكون keyword only وحتي لا يتعاض مع positional للاب
        super().__init__(*args, **kwargs) #خليها الاول احسن علشان الدالة دي لو في الاخر لو عملت parameter جديدة لازم امسحها 
        if user : 
            self.fields['category'].queryset = user.categories.all() # منطق الفلترة 


class CategoryForm(forms.ModelForm) :

    class Meta :
        model = Category
        fields = ['name']
        widgets ={
            'name' : forms.TextInput(attrs={'class' : 'input'})
        }
        
    def __init__(self, *args, user=None , **kwargs):##اي دالة وارثة بعد args
        super().__init__(*args, **kwargs)
        self.user = user ##كده انا لازم اعطيها مع الفورم

    #كده انا عاملها في الmodel UniqueConstraint  وهنا في الform
    def clean_name(self):
        name = self.cleaned_data.get('name')
        user = self.user #لازم الحقول الجديدة تكون قبل is_valid او في init
        if Category.objects.filter(user=user, name=name).exists():
            raise forms.ValidationError('هذا الاسم مستخدم من قبل')
        
        return name
