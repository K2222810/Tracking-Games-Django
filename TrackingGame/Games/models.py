from django.db import models
from django.conf import settings


class GameEntry(models.Model):
	"""Catalog entry for a game (title, release date, platform, cover URL)."""
	title = models.CharField(max_length=255)
	release_date = models.DateField(null=True, blank=True)
	platform = models.CharField(max_length=100, blank=True)
	cover_url = models.URLField(blank=True)

	def __str__(self):
		return self.title


class Game(models.Model):
	"""User-specific game record linking a user to a GameEntry."""

	STATUS_BACKLOG = 'backlog'
	STATUS_PLAYING = 'playing'
	STATUS_COMPLETED = 'completed'
	STATUS_DROPPED = 'dropped'

	STATUS_CHOICES = [
		(STATUS_BACKLOG, 'Backlog'),
		(STATUS_PLAYING, 'Playing'),
		(STATUS_COMPLETED, 'Completed'),
		(STATUS_DROPPED, 'Dropped'),
	]

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='games')
	game = models.ForeignKey(GameEntry, on_delete=models.CASCADE, related_name='user_games')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_BACKLOG)
	rank = models.IntegerField(null=True, blank=True, help_text='Optional ranking; 1 can mean favourite')
	want_to_play_date = models.DateField(null=True, blank=True)
	purchase_date = models.DateField(null=True, blank=True)

	def __str__(self):
		return f"{self.user} - {self.game} ({self.get_status_display()})"


class GameProgress(models.Model):
	"""Separate model for progress details for a Game (notes, hours, timestamp)."""
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='progress_entries')
	progress_note = models.TextField(blank=True)
	hours_played = models.PositiveIntegerField(null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-updated_at']

	def __str__(self):
		return f"Progress for {self.game} at {self.updated_at:%Y-%m-%d %H:%M}"

