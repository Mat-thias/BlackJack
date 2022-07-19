import random

# The possible rank of a card
RANK_LIST = [
    "A",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "J",
    "Q",
    "K",
]

# The possible rank of a card
SUIT_LIST = [
    "HEART",
    "DIAMOND",
    "SPADE",
    "CLUB",
]

# The possible status of a player, None is for a player who is still in the game
STATUS_LIST = [
    None,
    "PASS",
    "LOST_BY_SURRENDER",
    "LOST_BY_BUST",
    "LOST_BY_LESS_DEALER",
    "WON_BY_DEALER_BUST",
    "WON_BY_GREATER_DEALER",
    "BLACK_JACK",
]


class Card:
    """Declaring a card class having a rank and suit"""

    def __init__(self, rank, suit):
        """Setting the value of a card to 0 till it is calculated or set"""
        self.rank = Card.set_rank_by_index_or_rank(rank)
        self.suit = Card.set_suit_by_index_or_suit(suit)
        self.value = 0

    def __str__(self):
        return f"{self.rank},{self.suit[0]} "

    def set_value(self):
        """
        Setting the value of a card
        Note, to set the value of an ace we need to check the value of the hand,
        it is default to 1
        """
        if self.rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            self.value = int(self.rank)
        elif self.rank in ["J", "Q", "K"]:
            self.value = 10
        else:
            self.value = 1

    @staticmethod
    def set_rank_by_index_or_rank(rank):
        """Setting the rank of a card by either passing an index or rank itself"""
        if rank in RANK_LIST:
            return rank
        elif 13 >= rank >= 1:
            return RANK_LIST[rank - 1]
        else:
            raise ValueError

    @staticmethod
    def set_suit_by_index_or_suit(suit):
        """Setting the suit of a card by either passing an index or suit itself"""
        if suit in SUIT_LIST:
            return suit
        elif 4 >= suit >= 1:
            return SUIT_LIST[suit - 1]
        else:
            raise ValueError


class Hand:

    def __init__(self, player_index=None):
        """
        card_list: the hand's current cards, list of cards
        stake: the stake on the hand
        value: the value of the hand
        player_index: the index of the player with the hand, None if it is the dealer
        is_active: True if the hand is still in the game, else False
        is_standing: True if the player is standing on the hand, else False
        is_burst: True if the hand has burst, gone above 21, else False
        status: this is initialized to None, but changes and is_active changes to False, indicating the status
                like won, lost or push
        """
        self.card_list = []
        self.stake = 100
        self.value = 0
        self.player_index = player_index
        self.is_active = True
        self.is_standing = False
        self.is_burst = False
        self.status = STATUS_LIST[0]

    def __str__(self):
        if self.player_index is not None:
            result_str = f"Player {self.player_index}: "
        else:
            result_str = f"Dealer: "
        result_str += f"Hand => "
        for card in self.card_list:
            result_str += str(card)
        result_str += f" | Value => {self.value}"
        return result_str
    
    def set_value(self):
        """
        Sets the value for a hand
        If the hand contains an ace the computation is different
        It checks if when the ace value is set to 11, the hand value doesn't exceed 21
        else, it sets all ace value to 1
        Note: If there are more than one ace, at most one can have an ace with a value of 11
        """
        ace_indices = []
        total = 0

        for index in range(len(self.card_list)):
            if self.card_list[index].rank == "A":
                ace_indices.append(index)
            else:
                self.card_list[index].set_value()
                total += self.card_list[index].value

        no_aces = len(ace_indices)

        ace_low_value = 1
        ace_high_value = 11 

        if no_aces == 0:
            self.value = total
            return 

        else:
            for i in range(no_aces):
                if i == no_aces - 1:
                    total_temp = total
                    total_temp += ace_high_value

                    if total_temp > 21:
                        self.value = total + ace_low_value
                    else:
                        self.value = total + ace_high_value
                    
                else:
                    total += ace_low_value

    def check_burst(self):
        """Checking if the hand has burst and setting it player to True"""
        if self.value > 21:
            self.is_burst = True
            self.status = STATUS_LIST[3]

    def decide(self, table):
        """
        This allows the player to decide on the hand, if the hand is active, not standing,
        and hasn't burst
        Calls the appropriate function based on the player choice
        """
        if self.status != STATUS_LIST[0] or self.is_standing \
                or not self.is_active or self.is_burst:
            return

        possible_choices = self.get_possible_choices()

        # Formulating a prompt for the user to know their available choices
        input_str = f"{self}. "
        input_str += "\nYour available choices:"

        for choice in possible_choices:
            input_str += " " + choice

        input_str += " : "

        player_input = (input(input_str))
        while player_input.upper() not in possible_choices:
            player_input = (input("Invalid input. Please make sure you choose from your available choices."))

        if player_input.upper() == 'ST':
            self.stand()   
        elif player_input.upper() == 'HT':
            self.hit(table)            
        elif player_input.upper() == 'DD':
            self.double_down(table)            
        elif player_input.upper() == 'SP':
            pass
            # self.split()            
        elif player_input.upper() == 'SU':
            self.surrender() 

    def get_possible_choices(self):
        """
        Getting the player's available choices for the hand
        Stand and hit are available when the player hand value is less than 21
        double down is available when the hand value is less than 11 and the player just has two card in his hand
        split is available when the hand has two cards, and they are both of the same rank
        It returns it as a list
        """
        possible_choices = []

        if self.value <= 21:
            possible_choices.append('ST')
            possible_choices.append('HT')

        if self.value < 11 and len(self.card_list) == 2:
            possible_choices.append('DD')

        if len(self.card_list) == 2 and self.card_list[0].rank == self.card_list[1].rank:
            possible_choices.append('SP')

        if self.value <= 21:
            possible_choices.append('SU')

        return possible_choices

    def stand(self):
        """Set the hand is_standing to True"""
        self.is_standing = True
        print(f"Player {self.player_index} is standing. Good luck!")
        print()

    def hit(self, table, double_down=None):
        """
        Draws a card for the hand
        If the player is doubling down, it stands the player
        else, it lets the player decide again
        """
        if not double_down:
            table.draw_card(self)
            self.decide(table)
        else:
            table.draw_card(self)
            self.is_standing = True

    def double_down(self, table):
        """It increases the stake of the player, draws a card and stands the hand"""
        self.stake = self.stake * 2
        self.hit(table, double_down=True)
        print(f"Player{self.player_index} doubled down. Good luck!")

    def surrender(self):
        """Sets the player status to lost by surrender"""
        self.status = STATUS_LIST[2]
        print(f"Player{self.player_index} surrendered.")


class Player:
    """Declaring a player class to represent a player"""

    def __init__(self, index):
        """
        index: to initialize the opposition of the player on the table
        balance: the player's available money
        hand: the player's current hand, list of cards
        """
        self.index = index
        self.balance = 100
        self.hand = Hand(index)

    def __str__(self):
        result_str = f"Player {self.index} Hand : "
        for card in self.hand.card_list:
            result_str += str(card)
        return result_str + f" | Hand value => {self.hand.value}"

    def print_info(self):
        """To print the player's information"""
        result_str = f"Player{self.index};"

        result_str += "Hand: "
        for card in self.hand.card_list:
            result_str += str(card)
        result_str += f" | value => {self.hand.value} | stake => {self.hand.stake} " \
                      f"| is_active => {self.hand.is_active} | is_standing => {self.hand.is_standing} " \
                      f"| is_burst => {self.hand.is_burst} | status => {self.hand.status}"

        print(result_str)

    def decide(self, table):
        """lets a player decide on a hand active, not standing and not blackjacked hand"""
        if self.hand.is_active and not self.hand.is_standing and self.hand.status != STATUS_LIST[7]:
            self.hand.decide(table)
            Dealer.payout(self.hand)


class Dealer(Player):
    """A dealer class which inherits from player"""

    def __init__(self):
        """
        hand: the player's current hand, list of cards
        """
        self.hand = Hand()

    def __str__(self):
        result_str = f"Dealer Hand : "
        for card in self.hand.card_list:
            result_str += str(card)
        return result_str + f" {self.hand.value}"

    def compare_player_hand(self, hand):
        """
        This compares the  hand with the dealer's hand, and set the hand status appropriately
        """
        if self.hand.value > 21:     # checking if dealer has burst then player wins by dealer burst
            hand.status = STATUS_LIST[5]

        elif self.hand.value > hand.value:
            hand.status = STATUS_LIST[4]
        elif self.hand.value < hand.value:
            hand.status = STATUS_LIST[6]
        else:
            hand.status = STATUS_LIST[1]
        
    @staticmethod
    def payout(hand):
        """
        This pays the hand's stake based on the status
        Sets hand's is active to False after paying
        """
        black_jack_rate = 1.5
        win_rate = 1
        loss_rate = -1
        pass_rate = 0

        if hand.is_active:

            if (hand.status == STATUS_LIST[7]) and hand.is_active:
                hand.stake += (hand.stake * black_jack_rate)
                print(f"{hand} won by BLACK JACK. Congratulations!\n")
            elif (hand.status == STATUS_LIST[6]) and hand.is_active:
                hand.stake += (hand.stake * win_rate)
                print(f"{hand} won by beating the dealer. Congratulations!\n")
            elif (hand.status == STATUS_LIST[5]) and hand.is_active:
                hand.stake += (hand.stake * win_rate)
                print(f"{hand} won by dealer bust. Congratulations!\n")
            elif (hand.status == STATUS_LIST[4]) and hand.is_active:
                hand.stake += (hand.stake * loss_rate)
                print(f"{hand} lost to the dealer. Try Again!\n")
            elif (hand.status == STATUS_LIST[3]) and hand.is_active:
                hand.stake += (hand.stake * loss_rate)
                print(f"{hand} lost by busting. Try Again!\n")
            elif (hand.status == STATUS_LIST[2]) and hand.is_active:
                hand.stake += (hand.stake * loss_rate)
                print(f"{hand} lost by surrendering. Try Again!\n")
            elif (hand.status == STATUS_LIST[1]) and hand.is_active:
                hand.stake += (hand.stake * pass_rate)
                print(f"{hand} passed. Try Again!\n")
            
            if hand.status != STATUS_LIST[0]:
                hand.is_active = False
       

class Table:
    """Defining a table class"""

    def __init__(self, number_of_player=1):
        """
        dealer: a dealer for the table
        player_list: a list of players for the table
        shoe: a shoe contains 6 decks of shuffled cards except the once in the used_cards
        used_cards: contains cards that have been used out of the shoe
        """
        self.dealer = Dealer()
        self.player_list = [Player(index) for index in range(number_of_player)]
        self.shoe = Table.get_shoe()
        self.used_cards = []

    @staticmethod
    def get_shoe():
        """returns a shoe, 6 decks of card shuffled """
        shoe = [
             Card(rank, suit) for i in range(6) for suit in SUIT_LIST for rank in RANK_LIST 
             ]
        random.shuffle(shoe)
        return shoe

    def print_shoe(self):
        """prints the shoe out"""
        shoe_str = "SHOE| "

        for card in self.shoe:
            shoe_str += f"{card} | "

        shoe_str = shoe_str.strip()
        shoe_str += f" size:{len(self.shoe)}"

        print(shoe_str)

    def print_used_cards(self):
        """prints the used_cards out"""
        used_cards_str = " USED-CARDS| "

        for card in self.used_cards:
            used_cards_str += f"{card} | "

        used_cards_str = used_cards_str.strip()
        used_cards_str += f" size:{len(self.used_cards)}"

        print(used_cards_str)

    def draw_card(self, hand):
        """Draws a card from the shoe and adds it to the used_cards as well as the hand's hand"""
        card = self.shoe.pop()
        hand.card_list.append(card)
        self.used_cards.append(card)

        hand.set_value()
        hand.check_burst()
        print(hand)

    def first_serve(self):
        """Serving the players a pair of card and the dealer one card from the shoe"""
        for player in self.player_list:
            self.draw_card(player.hand)

        self.draw_card(self.dealer.hand)

        for player in self.player_list:
            self.draw_card(player.hand)
        
        print()

    def set_players_hand_value(self):
        """Setting all the players' hand value"""
        for player in self.player_list:
            player.hand.set_value()

    def check_players_black_jack(self):
        """Checking if any of the player has blackjack and paying out the player immediately"""
        if self.dealer.hand.card_list[0].rank != RANK_LIST[0]:

            for player in self.player_list:
            
                if player.hand.value == 21:
                    player.hand.status = STATUS_LIST[7]
                    Dealer.payout(player.hand)

    def players_decide(self):
        """Letting all the active, not standing and not blackjacked player decide"""
        for player in self.player_list:
            player.decide(self)

    def are_all_active_hands_standing(self):
        """
        Checks if all active hands are standing
        :returns True if all active hand are standing
        """
        is_standing_list = [
            player.hand.is_standing for player in self.player_list if player.hand.is_active
        ]
        return all(is_standing_list)

    def pay_all_active_standing_players(self):
        """Pay out all active standing hands and makes them inactive """
        if self.are_all_active_hands_standing():
            for player in self.player_list:
                if player.hand.is_active:
                    self.dealer.compare_player_hand(player.hand)
                    Dealer.payout(player.hand)

    def print_players_info(self):
        """Prints all players info"""
        for player in self.player_list:
            player.print_info()

    def dealer_draw_card(self):
        """This draws a card for the dealer till he/she reach 17 or bursts"""
        self.dealer.hand.set_value()

        while self.dealer.hand.value < 17:
            self.draw_card(self.dealer.hand)
        print()


def start_game():
    """This starts the game by creating a table for the game, a dealer and a list of players"""

    """
    The algorithm of the game is:
    When a game starts, a table is created with its shoe, the dealer, a list of players.
    The first serve is done, a pair of cards to the players and a single card to the dealer.
    Check for any of the player has a blackjack and pay him/her out immediately.
    Let the rest of the player decide their moves.
    After all players who have not burst, or surrender are standing, let the dealer draw till 17 or more.
    Then pay all active players; Payment could negative for loses.
    
    NOTE:
        This doesn't currently support split and insurance.
        The stake isn't set manually and always fixed at 100 units.
        The project is under development.
    """

    print("Welcome to the game of Black Jack.")
    print("Please note that the split feature is not available yet.")
    print("Please input ('ST' for STAND) ('HT' for HIT) "
          "('DD' for DOUBLING DOWN) ('SP' for SPLIT) ('SU' for SURRENDER).\n")

    # Asking for the number of players to create
    no_players = int(input("How many players are playing: "))

    table = Table(no_players)

    table.first_serve()
    
    table.check_players_black_jack()

    table.players_decide()

    table.dealer_draw_card()

    table.pay_all_active_standing_players()
    
    table.print_players_info()
