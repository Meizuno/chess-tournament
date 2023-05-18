from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.views import APIView

from main.forms import *
from main.models import Tournament, Player
from main.serializers import TournamentSerializer, PlayerSerializer
from rest_framework.response import Response


def home_page(request):
    response = render(request, 'home.html')
    response.set_cookie('lang', 'en', samesite='Lax')
    response.set_cookie('theme', 'light', samesite='Lax')
    return response


def tournaments_page(request):
    return render(request, 'tournaments.html')


def new_tournament_page(request):
    if request.method == 'POST':
        form = TournamentNewForm(request.POST)
        if 'create' in request.POST:
            if form.is_valid():
                tournament = form.save(commit=False)
                tournament.unique_id = get_random_string(length=8)
                tournament.save()
                tournament.organizers.add(request.user)
                return redirect('/tournaments')

    else:
        form = TournamentNewForm()
    return render(request, 'new_tournament.html', {'form': form})


def tournament_detail_page(request, tournament_unique_id):
    tournament = Tournament.objects.get(unique_id=tournament_unique_id)
    organizer = tournament.organizers.filter(id=request.user.id).exists()
    if request.method == 'POST':
        if 'register' in request.POST:
            player = request.user.id
            if player is not None:
                tournament.players.add(player)
                tournament.save()
        elif 'unregister' in request.POST:
            player = request.user.id
            if player is not None:
                tournament.players.remove(player)
                tournament.save()
        elif 'edit' in request.POST:
            return redirect(f"/tournaments/{tournament_unique_id}/edit/", tournament_unique_id=tournament_unique_id)
        elif 'remove' in request.POST:
            tournament = Tournament.objects.get(unique_id=tournament_unique_id)
            tournament.delete()
            return redirect('/tournaments')
    opened = tournament.opened
    return render(request, 'tournament_detail.html', {'opened': opened, 'organizer': organizer})


def tournament_edit_page(request, tournament_unique_id):
    if request.method == 'POST':
        form = TournamentEditForm(request.POST, instance=Tournament.objects.get(unique_id=tournament_unique_id))
        if 'edit' in request.POST:
            if form.is_valid():
                form.save()
                return redirect(f'/tournaments/{tournament_unique_id}')
    else:
        form = TournamentEditForm(instance=Tournament.objects.get(unique_id=tournament_unique_id))
    return render(request, "tournament_edit.html", {'form': form})


def profile_page(request, player_unique_id):
    if request.method == 'POST':
        if 'logout' in request.POST:
            logout(request)
            return redirect('/')
        elif 'edit' in request.POST:
            return redirect(f"/profile/{player_unique_id}/edit/", player_unique_id=player_unique_id)
    return render(request, 'profile.html', {'player_unique_id': player_unique_id})


def profile_edit(request, player_unique_id):
    if request.method == 'POST':
        form = PlayerEditForm(request.POST, request.FILES, instance=Player.objects.get(unique_id=player_unique_id))
        if 'edit' in request.POST:
            if form.is_valid():
                form.save()
                return redirect(f'/profile/{player_unique_id}')
            else:
                print(form.errors.as_data())
    else:
        form = PlayerEditForm(instance=Player.objects.get(unique_id=player_unique_id))
    return render(request, 'profile_edit.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        form = PlayerLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = PlayerLoginForm()
    return render(request, 'login.html', {'form': form})


def signup_page(request):
    if request.method == 'POST':
        form = PlayerSignUpForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.unique_id = get_random_string(length=8)
            player.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = PlayerSignUpForm()
    return render(request, 'signup.html', {'form': form})


class TournamentView(APIView):
    def get(self, request):
        tournaments = Tournament.objects.all()
        serializer = TournamentSerializer(tournaments, many=True)
        user_data = {'is_authenticated': request.user.is_authenticated,
                     'username': request.user.username,
                     'id': request.user.id,
                     }
        data = {'tournaments': serializer.data, 'user': user_data}
        return Response(data)


class TournamentDetailView(APIView):
    def get(self, request, tournament_unique_id):
        try:
            tournament = Tournament.objects.get(unique_id=tournament_unique_id)
        except Tournament.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TournamentSerializer(tournament)
        return Response(serializer.data)


class PlayerDetailView(APIView):
    def get(self, request, player_unique_id):
        try:
            player = Player.objects.get(unique_id=player_unique_id)
        except Player.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PlayerSerializer(player, context={'request': request})
        return Response(serializer.data)
