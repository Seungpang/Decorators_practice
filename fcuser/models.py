from django.db import models

# Create your models here.


class Fcuser(models.Model):
    username = models.CharField(max_length=32,
                                verbose_name='사용자명')
    useremail = models.EmailField(max_length=128,
                                  verbose_name='사용자이메일')
    password = models.CharField(max_length=128,
                                verbose_name='비밀번호')
    level = models.IntegerField(choices=(
                                (1, 'user'),
                                (2, 'admin'),
                                (3, 'superuser')),verbose_name='회원등급')
    is_authenticated = models.BooleanField(verbose_name='인증여부', default=False)
    registered_dttm = models.DateTimeField(auto_now_add=True, null=True,
                                           verbose_name='등록시간')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'fastcampus_fcuser'
        verbose_name = '패스트캠퍼스 사용자'
        verbose_name_plural = '패스트캠퍼스 사용자'


class FcuserValidation(models.Model):
    fcuser = models.ForeignKey('fcuser.Fcuser', on_delete=models.CASCADE)
    hashkey = models.CharField(max_length=256, verbose_name='인증키')

    def __str__(self):
        return str(self.fcuser) + ':' + self.hashkey

    class Meta:
        db_table = 'fastcampus_fcuser_validation'
        verbose_name = '패스트캠퍼스 사용자 인증키'
        verbose_name_plural = '패스트캠퍼스 사용자 인증키'
