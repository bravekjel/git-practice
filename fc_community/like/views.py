from django.shortcuts import render
from fcuser.models import Fcuser
from board.models import Board
from .models import Like
from django.db import transaction
from django.core import serializers
from fcuser.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import F

# Create your views here.


def api_like_list(request):
    # GET으로 board_id를 입력 받음
    board_id = request.GET.get('board_id')

    # 게시글 모델 가져오기 !
    board = Board.objects.get(pk=board_id)
    likes = Like.objects.filter(board=board)

    ret = []
    for like in likes:
        ret.append({
            'writer': like.writer.username
        })

    return JsonResponse(ret, safe=False)


@csrf_exempt
@login_required
def api_like(request):
    board_id = request.POST.get('board_id')
    user_id = request.session.get('user')

    with transaction.atomic():
        user = Fcuser.objects.get(pk=user_id)
        board = Board.objects.get(pk=board_id)

        like, created = Like.objects.get_or_create(
            writer=user,
            board=board
        )

        if created:
            board.like_cnt = board.like_cnt + 1
            board.save()
            # Board.objects.filter(pk=board_id).update(like_cnt=F('like_cnt')+1) # 전체 갱신할때 효율높이는 용도로 사용

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
