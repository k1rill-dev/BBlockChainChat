from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chat.models import Message, Profile
from django.contrib.auth import logout
from chat.forms import SignUpForm
from chat.serializers import MessageSerializer, UserSerializer
from .blockchain import get_integrity, write_blok
from django.core.mail import send_mail
from .RSA_AES import *


def index(request):
    if request.user.is_authenticated:
        return redirect('chats')
    if request.method == 'GET':
        return render(request, 'chat/index.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('{"error": "User does not exist"}')
        return redirect('chats')


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        # messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        rsa = Rsa()
        aes = Aes()
        secret_key = Profile.objects.get(user=receiver)
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        # print(dir(messages))
        # print(type(messages))
        # messages.message = '234432342234432'
        for message in messages:
            message.message = aes.dec_aes(message.message, rsa.decript(secret_key.aes_key, secret_key.secret_key))
            message.save()

        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)

        serializer = MessageSerializer(messages, many=True, context={'request': request})
        print(serializer.data)

        messages1 = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        for i in messages1:
            i.is_read = True
            i.message = aes.enc_aes(i.message, rsa.decript(secret_key.aes_key, secret_key.secret_key))
            i.save()

        print(serializer.data)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print(data)
        user_id = User.objects.get(username=data['receiver'])
        sender_id = User.objects.get(username=data['sender'])

        open_key = Profile.objects.get(user=user_id.id)
        rsa = Rsa()
        aes = Aes()
        open_key.save()
        data['message'] = aes.enc_aes(data['message'], rsa.decript(open_key.aes_key, open_key.secret_key))
        print(len(Message.objects.all()))
        if len(Message.objects.all()) == 1:
            hash_with_data = write_blok(None, data['message'], None, name_two_person=(user_id, sender_id))

        else:
            hash_with_data = write_blok(sender_id.pk, data['message'], user_id.pk, name_two_person=(user_id, sender_id))
            print(hash_with_data)

        serializer = MessageSerializer(data=hash_with_data)
        # serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def land(request):
    return render(request, 'chat/landing.html')


def out(request):
    logout(request)
    return redirect('index')


def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()

            rsa = Rsa()
            key = Profile()
            key.secret_key = rsa.get_secret_key()
            key.open_key = rsa.get_open_key()
            aes = Aes()
            aes_key = aes.print_key()
            key_aes_enc = rsa.encript(aes_key, rsa.get_open_key())
            key.aes_key = key_aes_enc
            key.user = int(user.id)
            key.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('chats')
    else:
        form = SignUpForm()
    template = 'chat/register.html'
    context = {'form': form}
    return render(request, template, context)


def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chat/chat.html',
                      {'users': User.objects.exclude(username=request.user.username)})


def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        bb = get_integrity(id_sender=sender, id_receiver=receiver)
        print(bb)
        print()
        rsa = Rsa()
        aes = Aes()
        secret_key1 = Profile.objects.get(user=receiver)
        print(secret_key1.secret_key)
        secret_key2 = Profile.objects.get(user=sender)
        print(secret_key2.secret_key)
        print()
        list1 = [(aes.dec_aes(i.message, rsa.decript(secret_key1.aes_key, secret_key1.secret_key)), 1,
                  i.timestamp.strftime("%m-%d %H.%M")) for i in
                 Message.objects.filter(sender_id=sender, receiver_id=receiver)]
        list2 = [(aes.dec_aes(i.message, rsa.decript(secret_key2.aes_key, secret_key2.secret_key)), 0,
                  i.timestamp.strftime("%m-%d %H.%M")) for i in
                 Message.objects.filter(sender_id=receiver, receiver_id=sender)]
        a = sorted(list2 + list1, key=lambda x: x[-1])
        for i in range(len(a)):
            b = (str(a[i][0]).replace("<p>", "").replace("</p>", ""), a[i][1], a[i][2])
            a[i] = b
        print(a)
        return render(request, "chat/messages.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'receiver': User.objects.get(id=receiver),
                       'messages': a,
                       'change': bb})