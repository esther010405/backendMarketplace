from django.db import models    
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

# Create your models here.
class CustomUser(AbstractUser):
    """
    Custom user pour ton marketplace :
    - email unique
    - login avec email au lieu de username
    - champs de base de Django conservés (password, first_name, last_name, etc.)
    """
    # On force l'unicité de l'email
    email = models.EmailField(_("email address"),unique=True)

    # Si tu veux rendre username optionnel (facultatif visuellement)
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)

    is_seller = models.BooleanField(default=False)
    city = models.CharField(max_length=100, blank=True, null=True)

    image = models.ImageField(upload_to='user_avatars/', blank=True, null=True, help_text="Avatar de l'utilisateur")
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="Numéro de téléphone de l'utilisateur")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # On peut ajouter d'autres champs requis ici si besoin

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ['email']