import os
from pathlib import Path
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.core.files.base import ContentFile
from .models import PurpleUsers


BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.

def login(request):
    if request.method == 'POST': #'Signin' button was clicked
        user = request.POST.get ('username')
        passw = request.POST.get ('password')
 
        auth_user = auth.authenticate(username=user, password=passw)

        if auth_user is not None:
            auth.login(request, auth_user)
            return redirect(chat)
        else:
            context = {'auth_error' : "Authentication Failed!"}
            return render(request, "login.html", context)
    else:
        #This is a GET Operation, so just return the page as it is.
        return render(request, "login.html")




def register(request):
    user_error = ""
    mail_error = ""
    pass_error = ""
    response = ""
    if request.method == "POST": #'Signup' button was clicked
        data = PurpleUsers()
        new_user = request.POST.get ('username')
        if PurpleUsers.objects.filter(username=new_user).exists():
            user_error = "Username already exists!"

            context = {'user_error': user_error}
            return render(request, 'register.html', context)
        elif new_user == "":
            user_error = "Username cannot be null!"

            context = {'user_error': user_error}
            return render(request, 'register.html', context)
        mail = request.POST.get ('email')
        if PurpleUsers.objects.filter(email__iexact=mail).exists(): #Check if email already exists in the database
            mail_error = "Email already exists!"

            context = {'mail_error': mail_error}
            return render(request, 'register.html', context)
        elif mail == "":
            mail_error = "Email cannot be null!"

            context = {'mail_error': mail_error}
            return render(request, 'register.html', context)
    
        passw = request.POST.get ('password')
        if passw == "":
            pass_error = "Password cannot be null!"

            context = {'pass_error' : pass_error}
            return render(request, 'register.html', context)

        photo = request.POST.get ('photo')
        if photo is None:
            pass_error = "No Photo!"

            context = {'pass_error' : pass_error}
            return render(request, 'register.html', context)
        PurpleUsers.objects.create_user(username=new_user, email=mail, password=passw, image=photo)
        data.save()

        response = "Registration Successfull!"

        context = {'success_message': response, 'mail_error': mail_error, 'pass_error' : pass_error}
        return render(request, 'register.html', context)
    else:
        #This is a GET Operation, so just return the page as it is.

        return render(request, "register.html")




def chat(request):
    if request.method == 'POST' and request.FILES['profile_pic']: #New dp image was uploaded
        new_image = request.FILES['profile_pic']
        
        # save the uploaded image inside the profiles folder.
        file_content = ContentFile(new_image.read())

        full_filename = os.path.join(BASE_DIR, "static\\img\\profiles", new_image.name)
        fout = open(full_filename, 'wb+')

        # Iterate through the chunks.
        for chunk in file_content.chunks():
            fout.write(chunk)
        fout.close()

        #Set the path to the uploaded image
        PurpleUsers.objects.filter(username=request.user).update(image="profiles/" + str(new_image))

        return redirect(chat)

    else:
        #This is a GET Operation, so get all messages in the database and diaplay them
        users = PurpleUsers.objects.all()
        context = {'users' : users}
        
        return render(request, "chat.html", context)


def logout(request):
    auth.logout(request)
    return redirect(login)