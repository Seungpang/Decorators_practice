from django.shortcuts import render
from fcuser.models import Fcuser
from fcuser.decorators import superuser_requried
from .models import BoardPermission

# Create your views here.
@superuser_requried
def permission_list(request):
    if request.method == 'POST':
        create = request.POST.get('create')
        read = request.POST.get('read')
        update = request.POST.get('update')
        delete = request.POST.get('delete')

        c_perm, created = BoardPermission.objects.update_or_create(
            board_id=1,
            permission_type=1,
            defaults={'permission_level':int(create)}
        )        
        r_perm, created = BoardPermission.objects.update_or_create(
            board_id=1,
            permission_type=2,
            defaults={'permission_level':int(read)}
        )
        u_perm, created = BoardPermission.objects.update_or_create(
            board_id=1,
            permission_type=3,
            defaults={'permission_level':int(update)}
        )
        d_perm, created = BoardPermission.objects.update_or_create(
            board_id=1,
            permission_type=4,
            defaults={'permission_level':int(delete)}
        )

    board_perms = BoardPermission.objects.filter(board_id=1)
    perms = {}
    for perm in board_perms:
        if perm.permission_type == 1:
            perms['c_perm'] = perm.permission_level
        elif perm.permission_type ==2:
            perms['r_perm'] = perm.permission_level
        elif perm.permission_type ==3:
            perms['u_perm'] = perm.permission_level
        else:
            perms['d_perm'] = perm.permission_level                        
                      
    return render(request, 'permission_list.html', perms)

