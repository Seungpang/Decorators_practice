from django.shortcuts import render
from fcuser.models import Fcuser
from board.models import Board
from .models import Like
from fcuser.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
@login_required
def api_like(request):
    board_id = request.POST.get('board_id')
    user_id = request.session.get('user')

    with transaction.atomic():
        user = Fcuser.objects.get(pk=user_id)
        board = Board.object.get(pk=board_id)

        like = Like()
        like.writer = user
        like.board = board
        like.save()

        board.like_cnt = board.like_cnt + 1
        board.save()

    return JsonResponse({})