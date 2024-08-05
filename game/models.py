from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100, unique=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)

class GameHistory(models.Model):
    player1 = models.CharField(max_length=100)
    player2 = models.CharField(max_length=100)
    winner = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
