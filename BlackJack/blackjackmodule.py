import random
global CARD_NUMBER_LIST, CARD_SHAPE_LIST, STATUS_LIST

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
        Note, to set the value of an ace we need to check the value of the hand
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
        elif rank <= 13 and rank >= 1:
            return RANK_LIST[rank - 1]
        else:
            raise ValueError

    @staticmethod
    def set_suit_by_index_or_suit(suit):
        """Setting the suit of a card by either passing an index or suit itself"""
        if suit in SUIT_LIST:
            return suit
        elif suit <= 4 and suit >= 1:
            return SUIT_LIST[suit - 1]
        else:
            raise ValueError


class Player:
    """Declaring a player class to represent a player"""

    def __init__(self, index):
        """
        index: to initialize the opposition of the player on the table
        stake: the player stake on the hand
        hand: the player's current hand, list of cards
        hand_value: the value of the hand of the player
        is_active: True if the player is still in the game, else False
        is_standing: True if the player is standing on his/her current hand, else False
        is_burst: True if the player has burst, gone above 21, else False
        status: this is initialized to None, but changes and is_active changes to False
        """
        self.index = index
        self.stake = 100
        self.hand = []
        self.hand_value = 0
        self.is_active = True
        self.is_standing = False
        self.is_burst = False
        self. status = STATUS_LIST[0]


    def __str__(self):
        result_str = f"Player {self.index} Hand : "
        for card in self.hand:
            result_str += str(card)
        return result_str + f" | Hand value => {self.hand_value}"


    def check_burst(self):
        """Checking if the player has burst and setting is player to True"""
        if self.hand_value > 21:
            self.is_burst = True
            self.status = STATUS_LIST[3]


    def set_hand_value(self):
        """
        Sets the hand value for a player
        If the hand contains an ace the computation is different.
        It checks if when the ace value is set to 11, the hand value doesn't exceed 21
        else, it sets all ace value to 1
        Note: If there are more than one ace, at most one can have an ace with a value of 11
        """
        ace_indices = []
        total = 0

        for index in range(len(self.hand)):
            if self.hand[index].rank == "A":
               ace_indices.append(index)
            else:
                self.hand[index].set_value()
                total += self.hand[index].value

        no_aces = len(ace_indices)

        ace_low_value = 1
        ace_high_value = 11 

        if no_aces == 0:
            self.hand_value = total
            return 

        else:
            for i in range(no_aces):
                if i == no_aces - 1:
                    total_temp = total
                    total_temp += ace_high_value

                    if total_temp > 21:
                        self.hand_value = total + ace_low_value
                    else:
                        self.hand_value = total + ace_high_value
                    
                else:
                    total += ace_low_value
                   


    def decide(self, table):
        """
        This allows the player to decide if the player is active, not standing, and hasn't burst
        Calls the appropriate function based on the player choice
        """
        if self.status != STATUS_LIST[0] or self.is_standing == True or self.is_active == False or self.is_burst == True:
            # print(f"{self} can not choose.")
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

        if (player_input.upper() == 'ST'):
            self.stand()   
        elif (player_input.upper() == 'HT'):
            self.hit(table)            
        elif (player_input.upper() == 'DD'):
            self.double_down(table)            
        elif (player_input.upper() == 'SP'):
            pass
            # self.split()            
        elif (player_input.upper() == 'SU'):
            self.surrender()  

    def get_possible_choices(self):
        """
        Getting the player's available choices
        Stand and hit are available when the player hand value is less than 21
        double down is available when the hand value is less than 11 and the player just has two card in his hand
        split is available when the hand has two cards, and they are both of the same rank
        It returns it as a list
        """
        possible_choices = []

        if self.hand_value <= 21:
            possible_choices.append('ST')
            possible_choices.append('HT')

        if self.hand_value < 11 and len(self.hand) == 2:
            possible_choices.append('DD')

        if len(self.hand) == 2 and self.hand[0].rank == self.hand[1].rank:
            possible_choices.append('SP')

        if self.hand_value <= 21:
            possible_choices.append('SU')

        return possible_choices


    def stand(self):
        """Set the player is_standing to True"""
        self.is_standing = True
        print(f"Player {self.index} is standing. Good luck!")
        print()
        

    def hit(self, table, double_down=None):
        """
        Draws a card for the player
        If the player is doubling down, th stands the player
        else, it let the player decide again
        """
        if not double_down:
            table.draw_card(self)
            self.decide(table)
        else:
            table.draw_card(self)
            self.is_standing = True


    def double_down(self, table):
        """It increases the stake of the player, draws a card and stands the player"""
        self.stake = self.stake * 2
        self.hit(table, double_down=True)
        print(f"Player{self.index} doubled down. Good luck!")


    def surrender(self):
        """Sets the player status to lost by surrender"""
        self.status = STATUS_LIST[2]
        print(f"Player{self.index} surrendered.")

    def print_status(self):
        """To print the player's status"""
        print(f"Player{self.index} status is {self.status}")


class Dealer(Player):
    """A dealer class which inherits from player"""

    def __init__(self):
        """
        hand: the player's current hand, list of cards
        hand_value: the value of the hand of the player
        """
        self.hand = []
        self.hand_value = 0


    def __str__(self):
        result_str = f"Dealer Hand : "
        for card in self.hand:
            result_str += str(card)
        return result_str + f" {self.hand_value}"


    def compare_player_hand(self, player):
        """
        This compares the dealer's hand with the player's hand, and set the player's status appropriately
        """
        if self.hand_value > 21:     # checking if dealer has burst then player wins by dealer burst
            player.status = STATUS_LIST[5]

        elif (self.hand_value > player.hand_value):
            # print("dealer.hand_value > player.hand_value")
            player.status = STATUS_LIST[4]
        elif (self.hand_value < player.hand_value):
            # print("dealer.hand_value < player.hand_value")
            player.status = STATUS_LIST[6]
        else:
            # print("dealer.hand_value == player.hand_value")
            player.status = STATUS_LIST[1]
        

    # def set_player_status(self, player):
    #     player.set_hand_value()
    #     self.set_hand_value()
    #
    #     if (player.hand_value > 21):
    #             player.outcome = OUTCOME[1]
    #     if (self.hand_value > player.hand_value):
    #         player.outcome = STATUS_LIST[1]
    #     elif (self.hand_value < player.hand_value):
    #         player.outcome = STATUS_LIST[0]
    #     else:
    #         player.outcome = OUTCOME[2]


    def payout(self, player):
        """
        This pays the player's stake based on the status
        Sets player's is active to False after paying
        """
        black_jack_rate = 1.5
        win_rate = 1
        loss_rate = -1
        pass_rate = 0

        if player.is_active:

            if (player.status == STATUS_LIST[7]) and player.is_active :
                player.stake += (player.stake * black_jack_rate)
                print(f"{player} won by BLACK JACK. Congratulations!\n")
            elif (player.status == STATUS_LIST[6]) and player.is_active :
                player.stake += (player.stake * win_rate)
                print(f"{player} won by beating the dealer. Congratulations!\n")
            elif (player.status == STATUS_LIST[5]) and player.is_active :
                player.stake += (player.stake * win_rate)
                print(f"{player} won by dealer bust. Congratulations!\n")
            elif (player.status == STATUS_LIST[4]) and player.is_active :
                player.stake += (player.stake * loss_rate)
                print(f"{player} lost to the dealer. Try Again!\n")
            elif (player.status == STATUS_LIST[3]) and player.is_active :
                player.stake += (player.stake * loss_rate)
                print(f"{player} lost by busting. Try Again!\n")
            elif (player.status == STATUS_LIST[2]) and player.is_active :
                player.stake += (player.stake * loss_rate)
                print(f"{player} lost by surrendering. Try Again!\n")
            elif (player.status == STATUS_LIST[1]) and player.is_active :
                player.stake += (player.stake * pass_rate)
                print(f"{player} passed. Try Again!\n")
            
            if (player.status != STATUS_LIST[0]):
                player.is_active = False
       

class Table:
    """Defining a table method"""

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


    def draw_card(self, player):
        """Draws a card from the shoe and adds it to the used_cards as well as the player's hand"""
        card = self.shoe.pop()
        player.hand.append(card)
        self.used_cards.append(card)

        player.set_hand_value()
        player.check_burst()
        print(player)


    def first_serve(self):
        """Serving the players a pair of card and the dealer one card from the shoe"""
        for player in self.player_list:
            self.draw_card(player)

        self.draw_card(self.dealer)

        for player in self.player_list:
            self.draw_card(player)
        
        print()
            

    def set_players_hand_value(self):
        """Setting all the players hand value"""
        for player in self.player_list:
                player.set_hand_value()


    def check_players_black_jack(self):
        """Checking if any of the player has blackjack and paying out the player immediately"""
        if self.dealer.hand[0].rank != RANK_LIST[0]:

            for player in self.player_list:
            
                if player.hand_value == 21:
                    player.status = STATUS_LIST[7]
                    self.dealer.payout(player)


    def print_players_status(self):
        for player in self.player_list:
            print(f"Player{player.index} status is {player.status}")


    def players_decide(self):
        """Letting all the active, not standing and not blackjacked player decide"""
        for player in self.player_list:
            if player.is_active and not(player.is_standing) and player.status != STATUS_LIST[7]:
                player.decide(self)
                self.dealer.payout(player)


    def are_all_active_players_standing(self):
        """
        Checks if all active players are standing
        :returns True if all active players are standing
        """
        is_standing_list = [
            player.is_standing for player in self.player_list if player.is_active==True
        ]
        return all(is_standing_list)


    def pay_all_active_standing_players(self):
        """Pay out all active standing players and makes them inactive """
        if self.are_all_active_players_standing():
            for player in self.player_list:
                if player.is_active:
                    self.dealer.compare_player_hand(player)
                    self.dealer.payout(player)


    def print_players_info(self):
        """Prints all players info"""
        for player in self.player_list:
            print(f"Player {player.index}| stake : {player.stake} | is_active : {player.is_active} | is_standing : {player.is_standing} | status : {player.status} | is_burst : {player.is_burst}")


    def dealer_draw_card(self):
        """This draws a card for the dealer till he/she reach 17 or bursts"""
        self.dealer.set_hand_value()

        while self.dealer.hand_value < 17 :
            self.draw_card(self.dealer)
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
    print("Please input ('ST' for STAND) ('HT' for HIT) ('DD' for DOUBLING DOWN) ('SP' for SPLIT) ('SU' for SURRENDER).\n")

    # Asking for the number of players to create
    no_players = int(input("How many players are playing: "))

    table = Table(no_players)

    table.first_serve()
    
    table.check_players_black_jack()

    table.players_decide()

    table.dealer_draw_card()

    table.pay_all_active_standing_players()
    
    table.print_players_info()