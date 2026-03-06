from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from datetime import date

from .models import Game
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)


class Home(LoginView):
    template_name = 'home.html'
    redirect_authenticated_user = True


def signup(request):
	# Redirect authenticated users away from signup
	if request.user.is_authenticated:
		return redirect('game-list')

	error_message = ''
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('game-list')
		else:
			error_message = 'Invalid sign up - try again'
	else:
		form = UserCreationForm()
	context = {'form': form, 'error_message': error_message}
	return render(request, 'signup.html', context)


@login_required
def add_game(request):
	return redirect('game-list')


class GameListView(LoginRequiredMixin, ListView):
	model = Game
	context_object_name = 'games'
	template_name = 'games/game_list.html'
	paginate_by = 20

	def get_queryset(self):
		# Show only non-backlog games in the main game list
		qs = Game.objects.filter(user=self.request.user).exclude(status=Game.STATUS_BACKLOG)
		# Sorting: support ?sort=rank|date and ?dir=asc|desc
		sort = self.request.GET.get('sort')
		direction = self.request.GET.get('dir', 'desc')
		if sort == 'rank':
			order_field = 'rank' if direction == 'asc' else '-rank'
		elif sort == 'date':
			# sort by purchase_date
			order_field = 'purchase_date' if direction == 'asc' else '-purchase_date'
		else:
			# default: rank descending then purchase_date descending
			order_field = '-rank'
		return qs.order_by(order_field)

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx['current_sort'] = self.request.GET.get('sort', '')
		ctx['current_dir'] = self.request.GET.get('dir', 'desc')
		return ctx


class GameCreate(LoginRequiredMixin, CreateView):
	model = Game
	fields = ['title', 'platform', 'status', 'rank', 'want_to_play_date', 'purchase_date', 'release_date', 'cover_url']
	template_name = 'games/game_form.html'
	success_url = reverse_lazy('game-list')

	def form_valid(self, form):
		form.instance.user = self.request.user
		# If the user clicked "Add to Wishlist", force backlog status and redirect to wishlist
		if 'add_to_wishlist' in self.request.POST:
			form.instance.status = Game.STATUS_BACKLOG
			self.object = form.save()
			return redirect('wishlist')
		return super().form_valid(form)


class GameDetailView(LoginRequiredMixin, DetailView):
	model = Game
	context_object_name = 'game'
	template_name = 'games/game_detail.html'

	def get_queryset(self):
		# restrict access to the owner's games
		return Game.objects.filter(user=self.request.user)


class GameUpdate(LoginRequiredMixin, UpdateView):
	model = Game
	fields = ['title', 'platform', 'status', 'rank', 'release_date', 'price', 'purchase_date', 'cover_url', 'want_to_play_date']
	template_name = 'games/game_form.html'
	success_url = reverse_lazy('game-list')

	def form_valid(self, form):
		# If the user clicked the 'mark_purchased' button, set purchase_date and update status
		if 'mark_purchased' in self.request.POST:
			form.instance.purchase_date = date.today()
			form.instance.status = Game.STATUS_PLAYING
		return super().form_valid(form)


class GameDelete(LoginRequiredMixin, DeleteView):
	model = Game
	template_name = 'games/game_confirm_delete.html'
	success_url = reverse_lazy('game-list')


@login_required
def dashboard(request):
	"""Show dashboard with game cards and a wish list (Backlog)."""
	user = request.user
	games = Game.objects.filter(user=user).exclude(status=Game.STATUS_BACKLOG)
	wishlist = Game.objects.filter(user=user, status=Game.STATUS_BACKLOG)
	return render(request, 'games/dashboard.html', {'games': games, 'wishlist': wishlist})


@login_required
def wishlist(request):
    """Show only backlog/wishlist games for the user."""
    user = request.user
    items = Game.objects.filter(user=user, status=Game.STATUS_BACKLOG)
    return render(request, 'games/wishlist.html', {'games': items})


@login_required
def wishlist_toggle(request, pk):
	"""Handle toggling a wishlist item to purchased (it will disappear from wishlist).

	This does not delete the Game; it updates its status so it no longer
	appears on the wishlist page.
	"""
	if request.method != 'POST':
		return redirect('wishlist')
	try:
		game = Game.objects.get(pk=pk, user=request.user, status=Game.STATUS_BACKLOG)
	except Game.DoesNotExist:
		return redirect('wishlist')

	# mark it as purchased/playing so it no longer appears in the wishlist
	from datetime import date
	game.status = Game.STATUS_PLAYING
	game.purchase_date = date.today()
	game.save()
	return redirect('wishlist')


