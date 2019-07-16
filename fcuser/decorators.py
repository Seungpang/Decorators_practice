from django.shortcuts import redirect
from fcuser.models import Fcuser
from myadmin.models import BoardPermission
from django.http import JsonResponse
def permission_required(function):
    @login_required
    def wrap(request, *args, **kwargs):
        perms = BoardPermission.objects.filter(board_id=1)
        
        user_id = request.session.get('user')
        user = Fcuser.objects.get(pk=user_id)

        #READ
        if request.method == 'GET':
            perm = BoardPermission.objects.get(board_id=1, permission_type=2)
            if user.level < perm.permission_level:
                return JsonResponse({'error': '권한에러'}, status=403)

        #CREATE
        elif request.method == 'POST':
            perm = BoardPermission.objects.get(board_id=1, permission_type=1)
            if user.level < perm.permission_level:
                return JsonResponse({'error': '권한에러'}, status=403)
        #UPDATE
        elif request.method == 'PUT':
            perm = BoardPermission.objects.get(board_id=1, permission_type=3)
            if user.level < perm.permission_level:
                return JsonResponse({'error': '권한에러'}, status=403)
        #DELETE
        else:
            perm = BoardPermission.objects.get(board_id=1, permission_type=4)
            if user.level < perm.permission_level:
                return JsonResponse({'error': '권한에러'}, status=403)
        
        

        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap




def login_required(function):
    def wrap(request, *args, **kwargs):
        if not request.session.get('user'):
            return redirect('/fcuser/login/')

        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def admin_requried(function):
    @login_required
    def wrap(request, *args, **kwargs):
        user_id = request.session.get('user')
        user = Fcuser.objects.get(pk=user_id)
        if user.level < 2: #2: admin
            return redirect('/')

        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def superuser_requried(function):
    @login_required
    def wrap(request, *args, **kwargs):
        user_id = request.session.get('user')
        user = Fcuser.objects.get(pk=user_id)
        if user.level < 3: #3: superuser
            return redirect('/')

        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap    