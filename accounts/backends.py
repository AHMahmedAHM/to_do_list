from django.contrib.auth.backends import ModelBackend 
from django.contrib.auth import get_user_model 
from django.db.models import Q 
import logging 

logger = logging.getLogger(__name__)

class TripleAuthBackend(ModelBackend):
    def authenticate(self, request, username, password=None, **kwargs):
        
        UserModel = get_user_model()
        try :
            user = UserModel.objects.get(Q(username=username)| Q(email=username) |Q (phone_number=username))
        except UserModel.DoesNotExist:
            ##logger.warning('%s is not found', username) حوشتها لانها المفروض للحالات ااخطيرة لانها هتتسجل في ملف
            return None 
        except UserModel.MultipleObjectsReturned : #علشان لو رجع كذا واحد مثلا اسم المستخدم هو عامله زي رقم تليفون واحد تاني
            logger.warning('multiple objects for %s username field', username)
            return None

        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user 
        return None 
