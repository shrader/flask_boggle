from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('<title>Boggle</title>', html)
            # test that you're getting a template

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.get('/api/new-game')
            json = response.json
            
            # test for valid keys
            self.assertTrue(type(json['board']), list)
            self.assertTrue(type(json['gameId']), str)

            # test for games dictionary keys
            self.assertIn(json['gameId'], games)
            
            # write a test for this route
    
    def test_api_score_word(self):
        """Test scoring words"""

        with self.client as client:
            game_id = client.get("/api/new-game").get_json()['gameId']
        
            game = games[game_id]

            game.board = [["B", "C", "T", "E", "E"], 
                            ["A", "R", "S", "D", "Y"],
                            ["E", "Y", "O", "P", "M"],
                            ["J", "E", "I", "A", "T"],
                            ["F", "U", "I", "E", "L"]]
                
            json = client.post("/api/score-word",
                               json={"word": "CARTS", "gameId": game_id})
           
            # check if words are in library
            self.assertTrue(game.is_word_in_word_list("CARTS"))
            self.assertFalse(game.is_word_in_word_list("TSDYM"))

            #check if words are in board
            self.assertTrue(game.check_word_on_board("CARTS"))
            self.assertFalse(game.check_word_on_board("APPLES"))
