from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate


UserModel = get_user_model()   ##مينفعشي نعملها في init  لان  Meta  بتحدث قبل انشاء الobject  انما وقت انشاء الملف 

#UserCreationForm >>ModelForm منطق كلمتي المرور والتحق منهم والتشفير ويمكن الاستغناء ب user.set_password()
class CustomRegisterForm(UserCreationForm):
    
    class Meta :
        model = UserModel
        fields =['first_name', 'last_name', 'username', 'email', 'phone_number']
        widgets ={
            'email' : forms.EmailInput(attrs={'class':'form-control'}),
            'phone_number' : forms.TextInput(attrs={'type':'tel', 'class':'form-control'}),
        }
    ## مش محتاج اعمل تحقق لل username  لانه موجود انما الايميل لانه مش اجباري  والهاتف لانه مش موجود خالص 
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email : #هل هذه الخطوة لها قيمة  ؟؟ ج:نعم لها قيمة لان الكبيعي ان الايميل غير اجباري 
            raise forms.ValidationError('حقل مطلوب بالفعل')
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError('هذا الايميل مستخدم من قبل ')
        
        return email 

    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError('هذا الحقل مطلوب  ')
        if len(phone_number) < 11 or not phone_number.startswith('01'):
            raise forms.ValidationError('رقم الهاتف غير صحيح')
        if UserModel.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('رقم الهاتف هذا مستخدم من قبل')

        return phone_number
    
    #مطلوب ال save لو محتاجه تضيف حقول 




class CustomLoginForm(AuthenticationForm): #Form >>no class Meta بيقارن كلمة المرور بعد تشفيرها يمكن الاستغناء ب set_password
    remember_me = forms.BooleanField( initial=False , required=False) ###اي حقل BooleanField + checkboxinput(الافتراضي) لازم تعمل required=False
    
    ## مش مطلوب تحقق من كتابة ال username  لانه اجباري في الموديل وال form هنا 
    
    def clean(self):
        cleaned_data = super().clean()  
        #بما اني استدعيت super  في هذا الفورم الجاهز  فالمنطق لل authenticate , self.user_cache موجود داخل clean()
        return cleaned_data
        
    ## مينفعشي اعمل دالة save  لانه مش مربوط ب Model هو اساسا Form   




class ProfileForm(forms.ModelForm): #بيستخدمه عند التعديل 
    
    class Meta :
        model = UserModel
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number']
    
    ####دالة عمومية 
    def clean_unique_field(self,field_name):
        value = self.cleaned_data.get(field_name) ##كده كده هكتبه هناك نص 
        if not value :
            raise forms.ValidationError('هذا الحقل مطلوب') #كده كده هيكتبها جمب الحقل 
        #self.instance هي المستخدن
        if UserModel.objects.filter(**{field_name:value}).exclude(pk=self.instance.pk).exists():  ### فلارة ديناميكية افضل لماذا من العادية  field_name = value ??
            raise forms.ValidationError(' مستخدم من قبل ')
        return value

    ## لازم اعمل كل حاجة هنا 
    def clean_username (self):
        return self.clean_unique_field('username')  # اكتبها هنا كما احب ان اكتبها هناك 
    
    def clean_email(self):
        return  self.clean_unique_field('email') # هل لازم  اعمل return هنا وانا عامل هناك ولماذا 
    
    def clean_phone_number(self):
        return self.clean_unique_field('phone_number')

        
    #لو فيه حاجة جديدة مش كاتبها في manager اظبطها هنا 

