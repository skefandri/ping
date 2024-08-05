# # game/consumers.py

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from time import time

# class PongConsumer(AsyncWebsocketConsumer):
#     game_state = {
#         'paddle1Y': 0,
#         'paddle2Y': 0,
#         'ballX': 0,
#         'ballY': 0,
#         'ballSpeedX': 2,
#         'ballSpeedY': 2,
#         'score1': 0,
#         'score2': 0,
#         'gameOver': False,
#         'winnerMessage': ''
#     }

#     async def connect(self):
#         self.room_group_name = 'pong'
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()
#         print("WebSocket connection accepted")

#         # Initialize game state
#         self.game_state['paddle1Y'] = (400 - 75) / 2
#         self.game_state['paddle2Y'] = (400 - 75) / 2
#         self.game_state['ballX'] = 800 / 2
#         self.game_state['ballY'] = 400 / 2

#         # Start the game loop
#         self.loop_task = self.loop.create_task(self.game_loop())

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#         self.loop_task.cancel()
#         print(f"WebSocket connection closed with code: {close_code}")

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         print(f"Received data: {data}")

#         # Update paddle positions based on player input
#         if 'player1Up' in data:
#             self.game_state['paddle1Y'] -= 8 if data['player1Up'] else 0
#         if 'player1Down' in data:
#             self.game_state['paddle1Y'] += 8 if data['player1Down'] else 0
#         if 'player2Up' in data:
#             self.game_state['paddle2Y'] -= 8 if data['player2Up'] else 0
#         if 'player2Down' in data:
#             self.game_state['paddle2Y'] += 8 if data['player2Down'] else 0

#     async def game_update(self, event):
#         message = event['message']
#         print(f"Sending data to WebSocket: {message}")

#         # Send updated game state to WebSocket
#         await self.send(text_data=json.dumps(message))

#     async def game_loop(self):
#         while True:
#             self.update_ball_position()

#             # Broadcast updated game state to all clients
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'game_update',
#                     'message': self.game_state
#                 }
#             )
#             await asyncio.sleep(0.016)  # Run the loop at ~60 FPS

#     def update_ball_position(self):
#         # Update ball position
#         self.game_state['ballX'] += self.game_state['ballSpeedX']
#         self.game_state['ballY'] += self.game_state['ballSpeedY']

#         # Ball collision with top and bottom walls
#         if self.game_state['ballY'] + 10 > 400 or self.game_state['ballY'] - 10 < 0:
#             self.game_state['ballSpeedY'] = -self.game_state['ballSpeedY']

#         # Ball collision with paddles
#         if self.game_state['ballX'] - 10 < 10:
#             if self.game_state['paddle1Y'] < self.game_state['ballY'] < self.game_state['paddle1Y'] + 75:
#                 self.game_state['ballSpeedX'] = -self.game_state['ballSpeedX']
#                 deltaY = self.game_state['ballY'] - (self.game_state['paddle1Y'] + 75 / 2)
#                 self.game_state['ballSpeedY'] = deltaY * 0.02
#             else:
#                 self.game_state['score2'] += 1
#                 self.reset_ball()

#         elif self.game_state['ballX'] + 10 > 800 - 10:
#             if self.game_state['paddle2Y'] < self.game_state['ballY'] < self.game_state['paddle2Y'] + 75:
#                 self.game_state['ballSpeedX'] = -self.game_state['ballSpeedX']
#                 deltaY = self.game_state['ballY'] - (self.game_state['paddle2Y'] + 75 / 2)
#                 self.game_state['ballSpeedY'] = deltaY * 0.02
#             else:
#                 self.game_state['score1'] += 1
#                 self.reset_ball()

#         # Check for game over
#         if self.game_state['score1'] >= 3:
#             self.game_state['gameOver'] = True
#             self.game_state['winnerMessage'] = 'Player 1 Wins!'
#         elif self.game_state['score2'] >= 3:
#             self.game_state['gameOver'] = True
#             self.game_state['winnerMessage'] = 'Player 2 Wins!'

#     def reset_ball(self):
#         self.game_state['ballX'] = 800 / 2
#         self.game_state['ballY'] = 400 / 2
#         self.game_state['ballSpeedX'] = -self.game_state['ballSpeedX']
#         self.game_state['ballSpeedY'] = 2
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("WebSocket connection accepted")

        self.game_state = {
            'paddle1Y': (400 - 75) / 2,
            'paddle2Y': (400 - 75) / 2,
            'ballX': 800 / 2,
            'ballY': 400 / 2,
            'ballSpeedX': 4,
            'ballSpeedY': 2,
            'score1': 0,
            'score2': 0,
            'gameOver': False,
            'winnerMessage': ''
        }

    async def disconnect(self, close_code):
        print(f"WebSocket connection closed with code: {close_code}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"Received data: {data}")

        # Update paddle positions based on player input
        if 'player1Up' in data and data['player1Up']:
            self.game_state['paddle1Y'] = max(self.game_state['paddle1Y'] - 8, 0)
        if 'player1Down' in data and data['player1Down']:
            self.game_state['paddle1Y'] = min(self.game_state['paddle1Y'] + 8, 400 - 75)
        if 'player2Up' in data and data['player2Up']:
            self.game_state['paddle2Y'] = max(self.game_state['paddle2Y'] - 8, 0)
        if 'player2Down' in data and data['player2Down']:
            self.game_state['paddle2Y'] = min(self.game_state['paddle2Y'] + 8, 400 - 75)

        # Update ball position
        self.game_state['ballX'] += self.game_state['ballSpeedX']
        self.game_state['ballY'] += self.game_state['ballSpeedY']

        # Ball collision with top and bottom walls
        if self.game_state['ballY'] + 10 > 400 or self.game_state['ballY'] - 10 < 0:
            self.game_state['ballSpeedY'] = -self.game_state['ballSpeedY']

        # Ball collision with paddles
        if self.game_state['ballX'] - 10 < 10:
            if self.game_state['paddle1Y'] < self.game_state['ballY'] < self.game_state['paddle1Y'] + 75:
                self.game_state['ballSpeedX'] = -self.game_state['ballSpeedX']
                deltaY = self.game_state['ballY'] - (self.game_state['paddle1Y'] + 75 / 2)
                self.game_state['ballSpeedY'] = deltaY * 0.2
            else:
                self.game_state['score2'] += 1
                self.reset_ball()

        elif self.game_state['ballX'] + 10 > 800 - 10:
            if self.game_state['paddle2Y'] < self.game_state['ballY'] < self.game_state['paddle2Y'] + 75:
                self.game_state['ballSpeedX'] = -self.game_state['ballSpeedX']
                deltaY = self.game_state['ballY'] - (self.game_state['paddle2Y'] + 75 / 2)
                self.game_state['ballSpeedY'] = deltaY * 0.2
            else:
                self.game_state['score1'] += 1
                self.reset_ball()

        # Check for game over
        if self.game_state['score1'] >= 3:
            self.game_state['gameOver'] = True
            self.game_state['winnerMessage'] = 'Player 1 Wins!'
        elif self.game_state['score2'] >= 3:
            self.game_state['gameOver'] = True
            self.game_state['winnerMessage'] = 'Player 2 Wins!'

        # Send updated game state to the WebSocket
        await self.send(text_data=json.dumps(self.game_state))

    def reset_ball(self):
        self.game_state['ballX'] = 800 / 2
        self.game_state['ballY'] = 400 / 2
        self.game_state['ballSpeedX'] = -self.game_state['ballSpeedX']
        self.game_state['ballSpeedY'] = 2
