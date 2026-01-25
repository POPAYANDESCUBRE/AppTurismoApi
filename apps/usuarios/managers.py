from django.contrib.auth.models import BaseUserManager 
from django.utils.crypto import get_random_string
class PersonalizacionUsuario(BaseUserManager):
    def create_user(self, correo, password=None, **kwargs):
        if not correo:
            raise ValueError("Debe proporcionar un correo electronico")
        correo = self.normalize_email(correo)
        user= self.model(correo=correo,**kwargs)
        if password:
            user.set_password(password)
        else:
            password = get_random_string()
        user.save(using=self._db)
        return user
    
    def create_superuser(self, correo, password=None, **kwargs):
        kwargs.setdefault("is_active",True)
        kwargs.setdefault("is_staff",True)
        kwargs.setdefault("is_superuser",True)
        
        if kwargs.get('is_active') is not True:
            raise ValueError('El superusuario debe tener is_active=True.')  # Lanza un ValueError si is_staff no es True
        if kwargs.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')  # Lanza un ValueError si is_staff no es True
        if kwargs.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')  # Lanza un ValueError si is_superuser no es True
        return self.create_user(correo, password, **kwargs)
    