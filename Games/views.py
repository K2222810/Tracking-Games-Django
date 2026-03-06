from datetime import date

from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Game, GameProgress, Review
from .forms import GameForm


class Home(LoginView):
    template_name = 'home.html'
    redirect_authenticated_user = True


def signup(request):
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
	
	return render(request, 'signup.html', {'form': form, 'error_message': error_message})


class GameListView(LoginRequiredMixin, ListView):
	model = Game
	context_object_name = 'games'
	template_name = 'games/game_list.html'
	paginate_by = 20

	def get_queryset(self):
		qs = Game.objects.filter(user=self.request.user).exclude(status=Game.STATUS_BACKLOG)
		direction = self.request.GET.get('dir', 'desc')
		
		if direction == 'asc':
			return qs.order_by(F('rank').asc(nulls_last=True))
		else:
			return qs.order_by(F('rank').desc(nulls_last=True))

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx['current_dir'] = self.request.GET.get('dir', 'desc')
		return ctx


class GameCreate(LoginRequiredMixin, CreateView):
	model = Game
	form_class = GameForm
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
	form_class = GameForm
	template_name = 'games/game_form.html'
	success_url = reverse_lazy('game-list')

	def form_valid(self, form):
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
	games = Game.objects.filter(user=request.user).exclude(status=Game.STATUS_BACKLOG)
	wishlist = Game.objects.filter(user=request.user, status=Game.STATUS_BACKLOG)
	return render(request, 'games/dashboard.html', {'games': games, 'wishlist': wishlist})


@login_required
def wishlist(request):
	items = Game.objects.filter(user=request.user, status=Game.STATUS_BACKLOG)
	return render(request, 'games/wishlist.html', {'games': items})


@login_required
def wishlist_toggle(request, pk):
	if request.method != 'POST':
		return redirect('wishlist')

	try:
		game = Game.objects.get(pk=pk, user=request.user, status=Game.STATUS_BACKLOG)
	except Game.DoesNotExist:
		return redirect('wishlist')

	game.status = Game.STATUS_PLAYING
	game.purchase_date = date.today()
	game.save()
	return redirect('wishlist')


@login_required
def add_progress(request, pk):
	if request.method != 'POST':
		return redirect('game-detail', pk=pk)

	try:
		game = Game.objects.get(pk=pk, user=request.user)
	except Game.DoesNotExist:
		return redirect('game-list')

	note = request.POST.get('note', '').strip()
	hours = request.POST.get('hours')
	delta = request.POST.get('delta')

	latest = game.progress_entries.first()
	prev_hours = (latest.hours_played if latest and latest.hours_played is not None else 0)

	new_hours = None
	if delta is not None and delta != '':
		try:
			d = int(delta)
			new_hours = max(0, prev_hours + d)
		except ValueError:
			new_hours = prev_hours
	elif hours:
		try:
			new_hours = max(0, int(hours))
		except ValueError:
			new_hours = prev_hours

	if new_hours is None and not note:
		return redirect('game-detail', pk=pk)

	entry = GameProgress(game=game, progress_note=note)
	if new_hours is not None:
		entry.hours_played = new_hours
	entry.save()

	if request.headers.get('x-requested-with') == 'XMLHttpRequest':
		data = {
			'id': entry.pk,
			'hours_played': entry.hours_played,
			'progress_note': entry.progress_note,
			'updated_at': timezone.localtime(entry.updated_at).strftime('%Y-%m-%d %H:%M'),
		}
		return JsonResponse({'entry': data})

	return redirect('game-detail', pk=pk)


@login_required
def edit_progress(request, pk):
	if request.method != 'POST':
		return JsonResponse({'error': 'POST required'}, status=400)
	
	entry = get_object_or_404(GameProgress, pk=pk)
	if entry.game.user != request.user:
		return JsonResponse({'error': 'forbidden'}, status=403)
	
	note = request.POST.get('note', '').strip()
	hours = request.POST.get('hours')
	if hours:
		try:
			entry.hours_played = max(0, int(hours))
		except ValueError:
			pass
	entry.progress_note = note
	entry.save()
	
	data = {
		'id': entry.pk,
		'hours_played': entry.hours_played,
		'progress_note': entry.progress_note,
		'updated_at': timezone.localtime(entry.updated_at).strftime('%Y-%m-%d %H:%M'),
	}
	return JsonResponse({'entry': data})


@login_required
def delete_progress(request, pk):
	if request.method != 'POST':
		return JsonResponse({'error': 'POST required'}, status=400)
	
	entry = get_object_or_404(GameProgress, pk=pk)
	if entry.game.user != request.user:
		return JsonResponse({'error': 'forbidden'}, status=403)
	
	game_pk = entry.game.pk
	entry.delete()
	
	if request.headers.get('x-requested-with') == 'XMLHttpRequest':
		return JsonResponse({'deleted': True, 'id': pk})
	return redirect('game-detail', pk=game_pk)


@login_required
def add_review(request, pk):
	if request.method != 'POST':
		return JsonResponse({'error': 'POST required'}, status=400)
	
	try:
		game = Game.objects.get(pk=pk)
	except Game.DoesNotExist:
		return JsonResponse({'error': 'not found'}, status=404)
	
	rating = request.POST.get('rating')
	comment = request.POST.get('comment', '').strip()
	try:
		rating = int(rating)
		if rating < 1 or rating > 5:
			raise ValueError()
	except Exception:
		rating = 5
	
	review = Review.objects.create(game=game, user=request.user, rating=rating, comment=comment)
	
	if request.headers.get('x-requested-with') == 'XMLHttpRequest':
		data = {
			'id': review.pk,
			'rating': review.rating,
			'comment': review.comment,
			'created_at': timezone.localtime(review.created_at).strftime('%B %d, %Y, %-I:%M %p')
		}
		return JsonResponse({'review': data})
	return redirect('game-detail', pk=pk)


@login_required
def delete_review(request, pk):
	if request.method != 'POST':
		return JsonResponse({'error': 'POST required'}, status=400)
	
	review = get_object_or_404(Review, pk=pk)
	if review.user != request.user:
		return JsonResponse({'error': 'forbidden'}, status=403)
	
	game_pk = review.game.pk
	review.delete()
	
	if request.headers.get('x-requested-with') == 'XMLHttpRequest':
		return JsonResponse({'deleted': True, 'id': pk})
	return redirect('game-detail', pk=game_pk)


