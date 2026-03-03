from django.contrib import admin
from .models import GameEntry, Game, GameProgress


@admin.register(GameEntry)
class GameEntryAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'release_date', 'platform')
	search_fields = ('title', 'platform')


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'game', 'status', 'rank')
	list_filter = ('status', 'game__platform')
	search_fields = ('user__username', 'game__title')


@admin.register(GameProgress)
class GameProgressAdmin(admin.ModelAdmin):
	list_display = ('id', 'game', 'hours_played', 'updated_at')
	search_fields = ('game__game__title', 'game__user__username')

