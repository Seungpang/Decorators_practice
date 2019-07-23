from django.db import models

# Create your models here.
class Like(models.Model):
    writer = models.ForeignKey('fcuser.Fcuser', on_delete=models.CASCADE,
                                verbose_name='작성자') 
    board = models.ForeignKey('board.Board',on_delete=models.CASCADE,
                                verbose_name='게시글')
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록일자')


    def __str__(self):
        return str(self.writer)

    class Meta:
        db_table = 'fastcampus_like'
        verbose_name = '좋아요'
        verbose_name_plural = '좋아요'