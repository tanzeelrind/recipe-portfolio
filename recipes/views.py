import os
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from google.oauth2 import id_token
from google.auth.transport import requests

from .models import Recipe


# ------------------ Recipe Views ------------------

@login_required(login_url="login_page")
def main_page(request):
    if request.method == "POST":
        data = request.POST
        recipe_name_from_form = data.get('recipe_name')
        recipe_description_from_form = data.get('description')
        recipe_image_from_form = request.FILES.get('recipe_image')

        Recipe.objects.create(
            recipe_name_from_models=recipe_name_from_form,
            recipe_description_from_models=recipe_description_from_form,
            recipe_image_from_models=recipe_image_from_form,
        )
        return redirect('/')

    recipes = Recipe.objects.all()
    if request.GET.get('search'):
        recipes = recipes.filter(recipe_name__icontains=request.GET.get('search'))

    context = {"recipes": recipes}
    return render(request, "recipe pages/index.html", context)


@login_required(login_url="login_page")
def update_recipe(request, id):
    queryset = Recipe.objects.get(id=id)

    if request.method == "POST":
        data = request.POST
        recipe_name_from_form = data.get('recipe_name')
        recipe_description_from_form = data.get('description')
        recipe_image_from_form = request.FILES.get('recipe_image')

        queryset.recipe_name_from_models = recipe_name_from_form
        queryset.recipe_description_from_models = recipe_description_from_form

        if recipe_image_from_form:
            queryset.recipe_image_from_models = recipe_image_from_form

        queryset.save()
        return redirect('/')

    context = {"recipe": queryset}
    return render(request, "recipe pages/update_recipes.html", context)


@login_required(login_url="login_page")
def delete_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/')


# ------------------ Auth Views ------------------

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid credentials")
            return redirect('login_page')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid credentials")
            return redirect('login_page')
        else:
            login(request, user)
            return redirect('/')

    return render(request, 'recipe pages/login.html')


def signup_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup_page')

        user_new = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user_new.set_password(password)
        user_new.save()

        messages.info(request, 'Account Created Successfully')
        return redirect('signup_page')

    return render(request, 'recipe pages/signup.html')


def logout_view(request):
    logout(request)
    return redirect('login_page')


# ------------------ Google Sign-In ------------------

@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after sign-in with a POST request containing ID token.
    """
    if request.method == "POST":
        print("Google auth POST hit")
        print("Request headers:", request.headers)
        print("Request body:", request.body)
        print("POST data:", request.POST)

        token = request.POST.get('credential')
        if not token:
            print("No token received")
            return HttpResponse("Server misconfigured", status=500)

        client_id = settings.GOOGLE_OAUTH_CLIENT_ID
        if not client_id:
            print("Missing GOOGLE_OAUTH_CLIENT_ID in env")
            return HttpResponse("Server misconfigured", status=500)

        try:
            user_data = id_token.verify_oauth2_token(
                token, requests.Request(), client_id
            )
        except ValueError as e:
            print("Token verification failed:", str(e))
            return HttpResponse("Invalid token", status=403)

        email = user_data.get("email")
        name = user_data.get("name", "")

        # Get or create Django user
        user, created = User.objects.get_or_create(
            username=email,
            defaults={"first_name": name}
        )

        # Log in user
        login(request, user)
        return redirect('/')

    return HttpResponse(status=405)  # method not allowed
