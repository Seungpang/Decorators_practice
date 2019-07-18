from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, JsonResponse
from fcuser.models import Fcuser
from tag.models import Tag
from .models import Board
from .forms import BoardForm
from django.views.decorators.csrf import csrf_exempt
from fcuser.decorators import login_required, admin_requried
# Create your views here.

def api_board_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        return JsonResponse({}, status=404)

    if request.method == 'GET':
        return JsonResponse({
            'title': board.title,
            'contents': board.contents,
            'writer': board.writer.username,
            'registered_dttm': board.registered_dttm
        })
    else:
        return JsonResponse({}, status=400)

@csrf_exempt
def api_board_write(request):
    if not request.session.get('user'):
        return JsonResponse({
            'error': '로그인을 해야합니다'
        }, status=401)

    if request.method == 'POST':
        if 'title' not in request.POST or not request.POST['title']:  #POST는 딕셔너리
            return JsonResponse({
                'error': '제목을 입력해야 합니다'
            }, status=400)
        elif 'contents' not in request.POST or not request.POST['contents']:
            return JsonResponse({
                'error': '내용을 입력해야 합니다'
            }, status=400)

        user_id = request.session.get('user')
        fcuser = Fcuser.objects.get(pk=user_id)

        board = Board()
        board.title = request.POST.get('title')
        board.contents = request.POST.get('contents')
        board.writer = fcuser
        board.save()

        return JsonResponse({}, status=201)
    
    return JsonResponse({}, status=400)


def board_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다')

    return render(request, 'board_detail.html', {'board': board})


def board_write(request):
    if not request.session.get('user'):
        return redirect('/fcuser/login/')

    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('user')
            fcuser = Fcuser.objects.get(pk=user_id)

            tags = form.cleaned_data['tags'].split(',')

            board = Board()
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            board.writer = fcuser
            board.save()

            for tag in tags:
                if not tag:
                    continue

                _tag, _ = Tag.objects.get_or_create(name=tag)
                board.tags.add(_tag)

            return redirect('/board/list/')
    else:
        form = BoardForm()

    return render(request, 'board_write.html', {'form': form})



def board_list(request):
    all_boards = Board.objects.all().order_by('-id')
    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_boards, 3)

    boards = paginator.get_page(page)
    return render(request, 'board_list.html', {'boards': boards})

