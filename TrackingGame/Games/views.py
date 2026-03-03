from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from .models import Game


def home(request):
	return render(request, 'games/home.html')


class GameListView(LoginRequiredMixin, ListView):
	model = Game
	context_object_name = 'games'
	template_name = 'games/game_list.html'
	paginate_by = 20

	def get_queryset(self):
		return Game.objects.filter(user=self.request.user).select_related('game')


class GameDetailView(LoginRequiredMixin, DetailView):
	model = Game
	context_object_name = 'game'
	template_name = 'games/game_detail.html'

	def get_queryset(self):
		# restrict access to the owner's games
		return Game.objects.filter(user=self.request.user).select_related('game')


