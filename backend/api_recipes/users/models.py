from django.db import models
from django.contrib.auth.models import AbstractUser
# # Create your models here.


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=150)
    email = models.EmailField(unique=True, max_length=254)
    # phone = models.CharField(unique=True, max_length=11)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    favorite = models.ManyToManyField()
    subscribers = models.ManyToManyField()
    shopping_cart = models.ManyToManyField()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

#
# class User(AbstractUser):
#     USER = 'user'
#     MODERATOR = 'moderator'
#     ADMIN = 'admin'
#
#     ROLE = [
#         (USER, 'user'),
#         (MODERATOR, 'moderator'),
#         (ADMIN, 'admin')
#     ]
#
#     username = models.CharField(max_length=191, unique=True)
#     email = models.EmailField(unique=True)
#     bio = models.TextField(blank=True,
#                            verbose_name='Биография',
#                            )
#
#     role = models.CharField(
#         max_length=20,
#         choices=ROLE,
#         default=USER,
#     )
#
#     def __str__(self):
#         return self.username
#
#     @property
#     def is_admin(self):
#         return self.role == self.ADMIN or self.is_superuser
#
#     @property
#     def is_moderator(self):
#         return self.role == self.MODERATOR
#
#  requiredfilds = [ укакзать поля какие ннеобходтив/]


# symetrical = False
#  related_name

#  Создали подписки
# class Follow(models.Model):
#     user = models.ForeignKey(User,
#                              on_delete=models.CASCADE,
#                              related_name='follower',
#                              verbose_name='Подписчики',
#                              )
#     author = models.ForeignKey(User,
#                                on_delete=models.CASCADE,
#                                related_name='following',
#                                verbose_name='Подписки',
#                                )
#
#     class Meta:
#         constraints = models.UniqueConstraint(
#             fields=['user', 'author'], name='unique follow')