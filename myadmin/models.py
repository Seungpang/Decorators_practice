from django.db import models

# Create your models here.

class BoardPermission(models.Model):
    board_id = models.IntegerField(verbose_name='게시판 ID') # 1을 가정
    permission_type = models.IntegerField(choices=(
                                            (1, 'create'),
                                            (2, 'read'),
                                            (3, 'update'),
                                            (4, 'delete')), verbose_name="권한 대상")
    permission_level = models.IntegerField(choices=(
                                            (1, 'user'),
                                            (2, 'admin'),
                                            (3, 'superuser')), verbose_name="권한")        


    def __str__(self):
        return self.permission_type

    class Meta:
        db_table = 'fastcampus_board_permission'
        verbose_name = '패스트캠퍼스 권한'
        verbose_name_plural = '패스트캠퍼스 권한'