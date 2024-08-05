from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Player, GameHistory

def home(request):
    return render(request, 'game/home.html')

# def record_game_result(request):
#     if request.method == 'POST':
#         data = request.POST
#         print(f"Received game result data: {data}")
#         player1 = get_object_or_404(Player, name=data['player1'])
#         player2 = get_object_or_404(Player, name=data['player2'])
#         winner = get_object_or_404(Player, name=data['winner']) if data['winner'] else None

#         player1.games_played += 1
#         player2.games_played += 1

#         if winner:
#             if winner == player1:
#                 player1.wins += 1
#                 player2.losses += 1
#             else:
#                 player2.wins += 1
#                 player1.losses += 1
#         else:
#             player1.draws += 1
#             player2.draws += 1

#         player1.save()
#         player2.save()

#         GameHistory.objects.create(player1=player1, player2=player2, winner=winner)

#         return JsonResponse({'status': 'success'})
