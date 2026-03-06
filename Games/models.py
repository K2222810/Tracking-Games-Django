from django.db import models
from django.conf import settings


class Game(models.Model):
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
	title = models.CharField(max_length=255, blank=True)
	platform = models.CharField(max_length=100, blank=True)
	release_date = models.DateField(null=True, blank=True)
	cover_url = models.URLField(blank=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_BACKLOG)
	rank = models.IntegerField(null=True, blank=True, help_text='Optional ranking; 1 can mean favourite')
	price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	want_to_play_date = models.DateField(null=True, blank=True)
	purchase_date = models.DateField(null=True, blank=True)

	def __str__(self):
		return f"{self.user} - {self.title} ({self.get_status_display()})"


class GameProgress(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='progress_entries')
	progress_note = models.TextField(blank=True)
	hours_played = models.PositiveIntegerField(null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-updated_at']

	def __str__(self):
		return f"Progress for {self.game} at {self.updated_at:%Y-%m-%d %H:%M}"


class Review(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	rating = models.PositiveSmallIntegerField(default=5)
	comment = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"Review {self.rating} for {self.game} by {self.user}"

