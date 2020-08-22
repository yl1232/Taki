from card import Card
from card_type import CardType
from player import Player
import constants
import random


class Game:
    def __init__(self):
        self.card_on_table = None
        self.players = None
        self.deck = None
        self.player_turn = 0
        self.number_of_players = None

    def initialize_deck(self):
        self.deck = [Card(num, color, card_type=CardType.Regular_Card) for color in constants.COLORS
                     for num in range(constants.CARD_MIN_NUMERIC_VALUE, constants.CARD_MAX_NUMERIC_VALUE)]
        self.deck += [Card(color=random.choice(constants.COLORS), card_type=CardType.Stop_Card)
                      for i in range(constants.AMOUNT_OF_STOP_CARDS)]
        self.deck += [Card(card_type=CardType.Change_Color_Card) for i in range(constants.AMOUNT_OF_CHANGE_COLOR_CARDS)]
        random.shuffle(self.deck)

    def update_number_of_players_from_user_input(self):
        while self.number_of_players not in range(constants.PLAYERS_LOWER_LIMIT, constants.PLAYERS_UPPER_LIMIT + 1):
            self.number_of_players = int(input(f'Enter number of players (between {constants.PLAYERS_LOWER_LIMIT} '
                                               f'to {constants.PLAYERS_UPPER_LIMIT}): '))

    def initialize_players_data(self):
        self.players = []
        self.update_number_of_players_from_user_input()
        for i in range(self.number_of_players):
            name = input(f"Insert player {i} name: ")
            age = int(input(f"Insert player {i} age: "))
            cards = [self.deck.pop() for j in range(constants.INITIAL_AMOUNT_OF_CARDS_PER_PLAYER)]
            player = Player(name, age, cards)
            self.players.append(player)
        self.players.sort(key=lambda x: x.age)

    def put_down_initial_card_on_table(self):
        self.card_on_table = self.deck.pop()
        while self.card_on_table.card_type == CardType.Change_Color_Card:
            self.deck.append(self.card_on_table)
            random.shuffle(self.deck)
            self.card_on_table = self.deck.pop()

    @staticmethod
    def find_most_common_color(cards):
        cards_colors = [card.color for card in cards if card.color]
        if not cards_colors:
            return None
        most_common_color = max(set(cards_colors), key=cards_colors.count)
        return most_common_color

    def print_game_status(self):
        print("Game status:")
        print(f"There are {len(self.deck)} cards in the deck")
        print(f"Card on table is {self.card_on_table}")
        for player in self.players:
            cards_text = [str(card) for card in player.cards]
            print(f"{player.name} has {len(player.cards)} cards: {cards_text}")
        print("")

    def put_down_card_on_table(self, player, card):
        self.card_on_table = card
        player.cards.remove(card)
        print(f"{player.name} discarded {self.card_on_table} (player left with {len(player.cards)} cards) \n")

    def try_playing_numeric_card_with_matching_number_or_color(self, player):
        for card in player.cards:
            if (card.color == self.card_on_table.color or card.num == self.card_on_table.num) and \
                    card.card_type == CardType.Regular_Card:
                self.put_down_card_on_table(player, card)
                return True
        return False

    def try_playing_stop_card(self, player):
        for card in player.cards:
            if card.card_type == CardType.Stop_Card and card.color == self.card_on_table.color:
                self.put_down_card_on_table(player, card)
                self.block_the_next_player()
                return True
        return False

    def try_playing_change_color_card(self, player):
        for card in player.cards:
            if card.card_type == CardType.Change_Color_Card:
                most_common_color = Game.find_most_common_color(player.cards)
                if most_common_color:
                    card.color = most_common_color
                else:
                    card.color = random.choice(constants.COLORS)  # BUG - card.color is a string
                self.put_down_card_on_table(player, card)
                return True
        return False

    def pull_card_from_deck(self, player):
        pulled_card = self.deck.pop()
        print(f"{player.name} pulled {pulled_card} from the deck ({len(self.deck)} cards left in the deck) \n")
        player.cards.append(pulled_card)

    def block_the_next_player(self):
        self.advance_to_next_player_turn()
        self.notify_player_was_blocked()

    def block_initial_player(self):
        self.notify_player_was_blocked()
        self.advance_to_next_player_turn()

    def notify_player_was_blocked(self):
        blocked_player = self.players[self.player_turn]
        print(f"{blocked_player.name}'s turn was blocked by a stop card\n")

    def advance_to_next_player_turn(self):
        self.player_turn += 1
        if self.player_turn >= self.number_of_players:
            self.player_turn = 0

    def declare_winner(self):
        winner = self.players[0]
        for player in self.players:
            if len(player.cards) < len(winner.cards):
                winner = player
        if not winner.cards:
            print(f"{winner.name} won with 0 cards")
        else:
            print(f"Game is over, the deck is empty. {winner.name} won with {len(winner.cards)} cards")

    def play_game(self):
        self.initialize_deck()
        self.initialize_players_data()
        self.put_down_initial_card_on_table()
        print(f"\n *** Game has started *** \n")
        self.print_game_status()
        if self.card_on_table.card_type == CardType.Stop_Card:
            self.block_initial_player()
        while self.deck:
            player_played_card = False
            player = self.players[self.player_turn]
            if self.try_playing_numeric_card_with_matching_number_or_color(player):
                player_played_card = True
            elif self.try_playing_stop_card(player):
                player_played_card = True
            elif self.try_playing_change_color_card(player):
                player_played_card = True
            if not player.cards:
                break
            if not player_played_card:
                self.pull_card_from_deck(player)
            self.print_game_status()
            self.advance_to_next_player_turn()

        self.declare_winner()

