from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

#Manager
class CustomManager(BaseUserManager):
    
    def create_user(self, username, email, phone_number, password=None, **kwargs):
        #make password is default =None because can register with e.g. google 
        if not username :
            raise ValueError( "اسم المستخدم مطلوب بالفعل " )
        if not email :
            raise ValueError('ايميل المستخدم مطلوب بالفعل') 
        if not phone_number :
            raise ValueError( "رقم الهاتف موجود بالفعل" )

        email = self.normalize_email(email)
        user = self.model(
            username = username,
            email = email ,
            phone_number = phone_number,
            **kwargs 
        )
        user.set_password(password)#for this , it is in parameter
        user.save(using=self._db)
        return user 


    def create_superuser(self, username, email, phone_number,password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        return self.create_user(username, email, phone_number, password, **kwargs)



# User Model 
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=50)
    phone_number = models.CharField(unique=True, max_length=20)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    objects = CustomManager()


