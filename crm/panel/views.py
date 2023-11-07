from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password

from accounts.models import User
from .models import User as User_tg
from .models import Messages


def main(req, page=None):
    """Главноя страница со всеми меню"""
    if req.user.is_authenticated:
        if page == 'users':
            users_list = User_tg.objects.all()
            users = [el for el in users_list]

            return render(req, 'work/main.html', {'page': page, 'users': users_list})

        else:
            users = User.objects.all()
            return render(req, 'work/main.html', {'page': page, 'users': users})

    else:
        return redirect('login')


def staf(req, id=None):
    """Страница редактирования данных персонала"""
    messages = []
    if req.user.is_authenticated:
        user = User.objects.get(id=id)
        if user:
            if req.method == 'POST':
                data = req.POST.dict()

                if 'delete' in data:
                    user.delete()
                    return redirect('main', 'manage')

                user.name = data['name']
                user.phone = data['phone']
                user.save()
                messages.append('Изменения сохранены!')

            return render(req, 'work/staf.html', {'user': user, 'messages': messages})


def user_page(req, id=None):
    """Страница пользователя"""
    messages = []
    if req.user.is_authenticated:
        user = User_tg.objects.get(id=id)

        if req.method == 'POST':
            data = req.POST.dict()
            if 'ban' in data:
                user.tg_id = f'{user.tg_id}_ban' if '_ban' not in user.tg_id else str(user.tg_id).replace('_ban', '')
                user.phone = f'{user.phone}_ban' if '_ban' not in user.phone else str(user.phone).replace('_ban', '')

            user.save()

            if 'delete' in data:
                user.delete()
                return redirect('main', 'users')
            if 'money' in data:
                user.money = int(data['money'])
                user.save()

            if 'msg' in data:
                msg = Messages()
                msg.address = f'{user.tg_id}_admin_send'
                msg.text = data['msg']
                msg.save()

        if user:
            ban = '_ban' in user.tg_id
            msg = [el for el in Messages.objects.all()]
            u_messages = []

            for el in msg:
                if str(user.tg_id) in str(el.address):
                    u_messages.append({'text': el.text, 'user': True if 'admin' not in el.address else False})
            u_messages.reverse()
            return render(req, 'work/user.html', {'user': user, 'ban': ban, 'msg': u_messages, 'messages': messages})


def create_staf(req):
    """Создание персонала"""
    messages = []
    if req.method == 'POST':
        user = User()
        data = req.POST.dict()
        user.name = data['name']
        user.phone = data['phone']
        user.password = make_password(data['psswd'])
        user.save()
        return redirect('staf', user.id)

    return render(req, 'work/createstaf.html', {'messages': messages})
