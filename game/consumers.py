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
            'ballSpeedX': 3,
            'ballSpeedY': 2,
            'score1': 0,
            'score2': 0,
            'gameOver': False,
            'winnerMessage': ''
        }

    async def disconnect(self, close_code):
        await self.close()
        print(f"WebSocket connection closed with code: {close_code}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        # print(f"Received data: {data}")

        if data.get('resetGame'):
            self.reset_game()
        else:
            if data.get('player1Up'):
                self.game_state['paddle1Y'] = max(self.game_state['paddle1Y'] - 8, 0)
            if data.get('player1Down'):
                self.game_state['paddle1Y'] = min(self.game_state['paddle1Y'] + 8, 400 - 75)
            if data.get('player2Up'):
                self.game_state['paddle2Y'] = max(self.game_state['paddle2Y'] - 8, 0)
            if data.get('player2Down'):
                self.game_state['paddle2Y'] = min(self.game_state['paddle2Y'] + 8, 400 - 75)

            self.update_ball_position()

            if self.game_state['score1'] >= 3:
                self.game_state['gameOver'] = True
                self.game_state['winnerMessage'] = 'Player 1 Wins!'
            elif self.game_state['score2'] >= 3:
                self.game_state['gameOver'] = True
                self.game_state['winnerMessage'] = 'Player 2 Wins!'

        # Send updated game state to the WebSocket
        await self.send(text_data=json.dumps(self.game_state))

    def update_ball_position(self):
        if not self.game_state['gameOver']:
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
                    self.game_state['ballSpeedY'] = deltaY * 0.02
                else:
                    self.game_state['score2'] += 1
                    self.reset_ball()

            elif self.game_state['ballX'] + 10 > 800 - 10:
                if self.game_state['paddle2Y'] < self.game_state['ballY'] < self.game_state['paddle2Y'] + 75:
                    self.game_state['ballSpeedX'] = -self.game_state['ballSpeedX']
                    deltaY = self.game_state['ballY'] - (self.game_state['paddle2Y'] + 75 / 2)
                    self.game_state['ballSpeedY'] = deltaY * 0.02
                else:
                    self.game_state['score1'] += 1
                    self.reset_ball()

    def reset_ball(self):
        self.game_state['ballX'] = 800 / 2
        self.game_state['ballY'] = 400 / 2
        self.game_state['ballSpeedX'] = -self.game_state['ballSpeedX']
        self.game_state['ballSpeedY'] = 1

    def reset_game(self):
        self.game_state = {
            'paddle1Y': (400 - 75) / 2,
            'paddle2Y': (400 - 75) / 2,
            'ballX': 800 / 2,
            'ballY': 400 / 2,
            'ballSpeedX': 3,
            'ballSpeedY': 2,
            'score1': 0,
            'score2': 0,
            'gameOver': False,
            'winnerMessage': ''
        }
