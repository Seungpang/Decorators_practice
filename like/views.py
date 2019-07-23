from django.shortcuts import render
from fcuser.models import Fcuser
from board.models import Board
from .models import Like
from fcuser.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

@csrf_exempt
@login_required
def api_like(request):
    board_id = request.POST.get('board_id')
    user_id = request.session.get('user')

    with transaction.atomic():
        user = Fcuser.objects.get(pk=user_id)
        board = Board.objects.get(pk=board_id)

        like, created = Like.objects.get_or_create( #있으면 인자값을 주고 없으면 새로 만든다
            writer=user,
            board=board
        )

        if created: #
            board.like_cnt = board.like_cnt + 1
            board.save()
            # Board.objects.filter(pk=board_id).update(like_cnt=F('like_cnt')+1) # 효율이 더 좋음
            

        return JsonResponse({'like_cnt': board.like_cnt})

    return JsonResponse({}, status=400)

@csrf_exempt
@login_required
def api_unlike(request):
    board_id = request.POST.get('board_id')
    user_id = request.session.get('user')

    with transaction.atomic():
        user = Fcuser.objects.get(pk=user_id)
        board = Board.objects.get(pk=board_id)

        like = Like.objects.filter(writer=user, board=board)
        if like.count():
            board.like_cnt = board.like_cnt - like.count()
            board.save()
            like.delete()

        return JsonResponse({'like_cnt': board.like_cnt})

        
    return JsonResponse({}, status=400)