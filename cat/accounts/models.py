from django.db import models


class Accounts(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name="Ad")
    surname = models.CharField(
        max_length=255, blank=False, null=False, verbose_name="Soyad"
    )
    email = models.EmailField(
        max_length=255, blank=False, null=False, verbose_name="Email"
    )
    password = models.CharField(
        max_length=255, blank=False, null=False, verbose_name="Şifre"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Oluşturulma Tarihi"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kullanıcı"
        verbose_name_plural = "Kullanıcılar"
        db_table = "Accounts"
