"""A module for a simple command land python implementation of blackjack."""

from random import shuffle
import input_handler

# The possible ranks of a card
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

# The possible suits of a card
SUIT_LIST = [
    "HEART",
    "DIAMOND",
    "SPADE",
    "CLUB",
]

# The possible status of a hand, None is for a hand that is still in the game
STATUS_LIST = [
    None,
    "PUSH",
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
        self.rank = rank
        self.suit = suit
        self.value = 0

    def __str__(self):
        return f"{self.rank}^{self.suit} "

    def set_value(self):
        """
        Setting the value of a card
        Note, to set the value of an ace we need to check the value of the hand,
        it is default to 11, later recalculated from the hand itself
        """
        if self.rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            self.value = int(self.rank)
        elif self.rank in ["J", "Q", "K"]:
            self.value = 10
        elif self.rank == 'A':
            self.value = 11


class Hand:
    """Declaring a hand class"""

    def __init__(self, card_list=None, player_index=None, index=None):
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
        self.card_list = [] if card_list is None else card_list
        self.stake = 0
        self.value = 0
        self.player_index = player_index
        self.index = index
        self.is_active = True
        self.is_standing = False
        self.is_burst = False
        self.status = STATUS_LIST[0]

    def __str__(self):
        result_str = f"Dealer: " if self.player_index is None else f"Player {self.player_index}: "
        result_str += f"Hand => " if self.index is None else f"Hand {self.index} => "

        for card in self.card_list:
            result_str += str(card)
        result_str += f" | Value => {self.value}"
        return result_str

    def print_info(self):
        """prints a hand object's information"""
        result_str = f"Hand {self.index}: "
        for card in self.card_list:
            result_str += str(card)
        result_str += f" | value => {self.value} | stake => {self.stake} " \
                      f"| is_active => {self.is_active} | is_standing => {self.is_standing} " \
                      f"| is_burst => {self.is_burst} | status => {self.status}"
        print(result_str)

    def set_value(self):
        """
        Sets the value for a hand
        If the hand contains aces, the computation is different
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

        if self.value == 21:
            self.stand(is_perfect_hand=True)
            return

        possible_choices = self.get_possible_choices()

        # Formulating a prompt for the user to know their available choices
        input_str = f"\n{self}. "
        input_str += "\nYour available choices:"

        for choice in possible_choices:
            input_str += " " + choice
        input_str += ": "

        error_message = "Invalid input. Please make sure you choose from your available choices. "
        player_input = input_handler.get_input_str_from_choice(
            possible_choices, input_str, error_message=error_message, case_sensitive=False)

        if player_input.upper() == 'ST':
            self.stand()
        elif player_input.upper() == 'HT':
            self.hit(table)
        elif player_input.upper() == 'DD':
            self.double_down(table)
        elif player_input.upper() == 'SP':
            self.split(table)
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

        if self.value <= 11 and len(self.card_list) == 2:
            possible_choices.append('DD')

        if len(self.card_list) == 2 and self.card_list[0].rank == self.card_list[1].rank:
            possible_choices.append('SP')

        if self.value <= 21:
            possible_choices.append('SU')

        return possible_choices

    def stand(self, is_perfect_hand=False):
        """Set the hand is_standing to True"""
        self.is_standing = True
        standing_message = f"Player {self.player_index} "
        if self.index is not None:
            standing_message += f"Hand {self.index} "
        standing_message += f"is standing on a perfect hand. Good luck!" if is_perfect_hand \
            else f"Player {self.player_index} is standing. Good luck!"
        print(standing_message)
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
            is_perfect_hand = True if self.value == 21 else False
            self.stand(is_perfect_hand=is_perfect_hand)

    def double_down(self, table):
        """It doubles the stake of the player on a hand, draws a card and stands the hand"""
        table.player_list[self.player_index].set_hand_stake(self, table, double_down=True)
        self.hit(table, double_down=True)
        print(f"Player{self.player_index} doubled down. Good luck!")

    def split(self, table):
        """
        This splits a hand into two and adds them to the players split card
        It lets the player decide on each hand along the way
        """
        if not table.player_list[self.player_index].is_split:
            table.player_list[self.player_index].is_split = True
            hand0 = Hand(card_list=[self.card_list[0]], player_index=self.player_index, index=0)
            hand1 = Hand(card_list=[self.card_list[1]], player_index=self.player_index, index=1)

        else:
            no_hands = len(table.player_list[self.player_index].split_hand)
            hand0 = Hand(card_list=[self.card_list[0]], player_index=self.player_index, index=self.index)
            hand1 = Hand(card_list=[self.card_list[1]], player_index=self.player_index, index=no_hands)

        table.player_list[self.player_index]. \
            set_split_hands_stake(hand0, hand1, table, table.player_list[self.player_index].hand.stake)

        try:
            table.player_list[self.player_index].split_hand[hand0.index] = hand0
        except IndexError:
            table.player_list[self.player_index].split_hand.append(hand0)
        try:
            table.player_list[self.player_index].split_hand[hand1.index] = hand1
        except IndexError:
            table.player_list[self.player_index].split_hand.append(hand1)

        table.player_list[self.player_index].split_hand[hand0.index].hit(table)
        table.player_list[self.player_index].split_hand[hand1.index].hit(table)

    def surrender(self):
        """Sets the player status to lost by surrender"""
        self.status = STATUS_LIST[2]
        print(f"Player{self.player_index} surrendered.")


class Player:
    """Declaring a player class to represent a player"""

    def __init__(self, index, table):
        """
        index: to initialize the opposition of the player on the table
        balance: the player's available money
        hand: the player's current hand, list of cards
        is_split: True if the player has split his hand, there by having multiple hands
        split_hand: holds the list of split hands
        is_insured: True when the player insures
        insurance: holds the stake for the insurance
        """
        self.index = index
        self.balance = 1000.00
        self.hand = Hand(player_index=index)
        self.is_split = False
        self.split_hand = []
        self.is_insured = None
        self.insurance = 0
        self.set_hand_stake(self.hand, table)

    def __str__(self):
        if self.is_split:
            no_hands = len(self.split_hand)
            result_str = f"Player {self.index} has {no_hands} hands."
            for index, hand in enumerate(self.split_hand):
                result_str += f"\nHand {index}: "
                for card in hand.card_list:
                    result_str += str(card)
                result_str += f" | Hand value => {self.hand.value}"
        else:
            result_str = f"Player {self.index}\nHand: "
            for card in self.hand.card_list:
                result_str += str(card)
            result_str += f" | Hand value => {self.hand.value}"

        return result_str

    def set_hand_stake(self, hand, table, stake=None, double_down=False):
        """stakes the hand of a player with the input stake and deducts it from the player's balance"""
        if self.is_split:
            stake = stake
        elif double_down:
            print(f"Player {self.index} has ${self.balance:.2f} is about to double down.")
            input_message = f"How much do you want to stake in $ (max is ${hand.stake:.2f})," \
                            f" you have ${self.balance} as balance: "
            stake = input_handler.get_input_float(input_message, error_massage=None,
                                                  upper_limit=min(self.hand.stake, self.balance), lower_limit=0)
        else:
            print(f"Player {self.index} has ${self.balance:.2f}.")
            input_message = "How much do you want to stake in $: "
            stake = input_handler.get_input_float(input_message, error_massage=None,
                                                  upper_limit=self.balance, lower_limit=0)

        self.debit_hand(hand, table, stake)

    def debit_hand(self, hand, table, stake):
        """Debits the stake from the player balance adds it to the table balance and the hand's stake"""
        if self.balance >= stake:
            self.balance -= stake
            table.balance += stake
            hand.stake += stake

    def debit_insurance(self, table, stake):
        """Debits the stake from the player balance adds it to the table balance and the player's insurance"""
        if self.balance >= stake:
            self.balance -= stake
            table.balance += stake
            self.insurance += stake
        else:
            print(f"{self} doesn't have enough balance.")

    def set_split_hands_stake(self, hand0, hand1, table, old_stake):
        """called when a hand is split, adds the stake of the old hand and stakes the other two new hands"""
        self.balance += old_stake
        self.set_hand_stake(hand0, table, stake=old_stake)
        self.set_hand_stake(hand1, table, stake=old_stake)

    def print_info(self):
        """To print the player's information"""
        if self.is_split:
            no_hands = len(self.split_hand)
            result_str = f"Player {self.index} has {no_hands} hands with ${self.balance:.2f}."
            for index, hand in enumerate(self.split_hand):
                result_str += f"\nHand {index}: "
                for card in hand.card_list:
                    result_str += str(card)
                result_str += f" | value => {hand.value} | stake => {hand.stake} " \
                              f"| is_active => {hand.is_active} | is_standing => {hand.is_standing} " \
                              f"| is_burst => {hand.is_burst} | status => {hand.status}"
        else:
            result_str = f"Player {self.index} has no hand with ${self.balance:.2f}.\nHand: "
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
            if not self.is_split:
                table.payout(self.hand)
            else:
                for hand in self.split_hand:
                    table.payout(hand)

    def insure(self, table):
        """allows the player to decide if he/she wants place insurance"""
        possible_choices = ['IN', 'X']
        input_str = f"\nPlayer {self.index} wants to insure. Enter 'in' or 'IN' to insure or 'x' not to: "
        insurance_input = input_handler.get_input_str_from_choice(possible_choices, input_str, case_sensitive=False)
        if insurance_input.upper() == 'IN':
            input_message = f"How much do you want to stake on insurance in $ (max is ${self.hand.stake/2:.2f})," \
                            f" you have ${self.balance} as balance: "
            stake = input_handler.get_input_float(input_message, error_massage=None,
                                                  upper_limit=min(self.hand.stake/2, self.balance), lower_limit=0)
            if stake <= self.hand.stake/2:
                self.is_insured = True
                self.debit_insurance(table, stake)
                print(f"Player {self.index} is insured.")
        else:
            print(f"Player {self.index} is not insured.")


class Dealer:
    """A dealer class which inherits from player"""

    def __init__(self):
        """
        hand: the dealer's current hand, list of cards
        """
        self.hand = Hand()

    def __str__(self):
        result_str = f"Dealer Hand: "
        for card in self.hand.card_list:
            result_str += str(card)
        return result_str + f" {self.hand.value}"

    def compare_player_hand(self, hand):
        """
        This compares the  hand with the dealer's hand, and set the hand status appropriately
        """
        if self.hand.value > 21:  # checking if dealer has burst then player wins by dealer burst
            hand.status = STATUS_LIST[5]
        elif self.hand.value > hand.value:
            hand.status = STATUS_LIST[4]
        elif self.hand.value < hand.value:
            hand.status = STATUS_LIST[6]
        else:
            hand.status = STATUS_LIST[1]


class Table:
    """Defining a table class"""

    def __init__(self, number_of_player=1):
        """
        dealer: a dealer for the table
        balance: the amount of money the table made
        player_list: a list of players for the table
        shoe: a shoe contains 6 decks of shuffled cards except the once in the drawn_cards
        drawn_cards: contains cards that have been drawn out of the shoe
        """
        self.dealer = Dealer()
        self.balance = 0
        self.player_list = [Player(index, self) for index in range(number_of_player)]
        self.shoe = Table.get_shoe()
        self.drawn_cards = []
        print()

    def __str__(self):
        return_str = f"Table has a balance of ${self.balance}.\n"
        # return_str += self.get_shoe_str()
        return_str += self.get_drawn_cards_str()
        return return_str

    @staticmethod
    def get_shoe():
        """returns a shoe, 6 decks of card shuffled """
        shoe = [
            Card(rank, suit[0]) for suit in SUIT_LIST for rank in RANK_LIST
        ]
        shoe *= 6
        shuffle(shoe)
        return shoe

    def get_shoe_str(self):
        """prints the shoe out"""
        shoe_str = "SHOE:\n "
        # for card in self.shoe:
        #     shoe_str += f"*|* | "
        shoe_str += f"*|* | " * len(self.shoe)
        shoe_str = shoe_str.strip()
        shoe_str += f" size:{len(self.shoe)}\n"
        return shoe_str

    def get_drawn_cards_str(self):
        """prints the drawn_cards out"""
        drawn_cards_str = " DRAWN-CARDS| "

        for card in self.drawn_cards:
            drawn_cards_str += f"{card} | "
        drawn_cards_str = drawn_cards_str.strip()
        drawn_cards_str += f" size:{len(self.drawn_cards)}\n"
        return drawn_cards_str

    def draw_card(self, hand):
        """
        Draws a card from the shoe and adds it to the drawn_cards as well as the hand's hand
        prints hand after every draw to help the user know what card was drawn
        """
        card = self.shoe.pop()
        hand.card_list.append(card)
        self.drawn_cards.append(card)

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

    def blackjack_or_insure_players(self):
        """
        checks if player can have blackjack
        which can happen only when the dealer's first card is not an ace
        if it is an ace, allows the players to decide if he/she wants insure
        """
        if self.dealer.hand.card_list[0].rank != RANK_LIST[0]:
            for player in self.player_list:
                if player.hand.value == 21:
                    player.hand.status = STATUS_LIST[7]
                    self.payout(player.hand)
        else:
            for player in self.player_list:
                # do you want insurance
                player.insure(self)

    def players_decide(self):
        """Lets all the active, not standing and not blackjacked player decide"""
        for player in self.player_list:
            player.decide(self)

    def are_all_active_hands_standing(self):
        """
        Checks if all active hands are standing
        returns: True if all active hand are standing
        """
        is_standing_list = []
        for player in self.player_list:
            if not player.is_split:
                if player.hand.is_active:
                    is_standing_list.append(player.hand.is_standing)
            else:
                for hand in player.split_hand:
                    if hand.is_active:
                        is_standing_list.append(hand.is_standing)

        return all(is_standing_list)

    def pay_all_active_standing_players(self):
        """Pay out all active standing hands and makes them inactive """
        if self.are_all_active_hands_standing():
            for player in self.player_list:
                if not player.is_split:
                    if player.hand.is_active:
                        self.dealer.compare_player_hand(player.hand)
                        self.payout(player.hand)
                else:
                    for hand_index in range(len(player.split_hand)):
                        if player.split_hand[hand_index].is_active:
                            self.dealer.compare_player_hand(player.split_hand[hand_index])
                            self.payout(player.split_hand[hand_index])

    def payout(self, hand):
        """
        This pays the hand's stake based on the status
        Sets hand's is active to False after paying
        """
        black_jack_rate = 1.5
        win_rate = 1
        loss_rate = -1
        push_rate = 0

        if hand.is_active:
            if (hand.status == STATUS_LIST[7]) and hand.is_active:
                hand.stake += (hand.stake * black_jack_rate)
                print(f"{hand} won by BLACK JACK. Congratulations!")
            elif (hand.status == STATUS_LIST[6]) and hand.is_active:
                hand.stake += (hand.stake * win_rate)
                print(f"{hand} won by beating the dealer. Congratulations!")
            elif (hand.status == STATUS_LIST[5]) and hand.is_active:
                hand.stake += (hand.stake * win_rate)
                print(f"{hand} won by dealer bust. Congratulations!")
            elif (hand.status == STATUS_LIST[4]) and hand.is_active:
                hand.stake += (hand.stake * loss_rate)
                print(f"{hand} lost to the dealer. Try Again!")
            elif (hand.status == STATUS_LIST[3]) and hand.is_active:
                hand.stake += (hand.stake * loss_rate)
                print(f"{hand} lost by busting. Try Again!")
            elif (hand.status == STATUS_LIST[2]) and hand.is_active:
                hand.stake += (hand.stake * loss_rate)
                print(f"{hand} lost by surrendering. Try Again!")
            elif (hand.status == STATUS_LIST[1]) and hand.is_active:
                hand.stake += (hand.stake * push_rate)
                print(f"{hand} pushed. Try Again!")

            if hand.status != STATUS_LIST[0]:
                self.credit_hand(hand)
                hand.is_active = False

    def credit_hand(self, hand):
        """credits the player's balance with the hand stake and from table balance"""
        self.player_list[hand.player_index].balance += hand.stake
        self.balance -= hand.stake
        hand.stake = 0

    def credit_insurance(self, player):
        """Credits the player's balance from the table balance with the hand stake"""
        self.player_list[player.index].balance += player.insurance
        print(player.insurance)
        self.balance -= player.insurance
        player.insurance = 0

    def print_players_info(self):
        """Prints all players info"""
        for player in self.player_list:
            player.print_info()
        print()

    def dealer_draw_card(self):
        """This draws a card for the dealer till he/she reach 17 or bursts"""
        print()
        while self.dealer.hand.value < 17:
            self.draw_card(self.dealer.hand)
        print()

    def pay_insurance(self):
        """
        This pays the player's balance based on the dealer having a blackjack or not
        """
        insurance_rate = 1 if len(self.dealer.hand.card_list) == 2 and self.dealer.hand.value == 21 else -1

        for player in self.player_list:
            if player.is_insured:
                player.insurance += (player.insurance * insurance_rate)
                self.credit_insurance(player)


def start_game():
    """This starts the game by creating a table for the game, a dealer and a list of players"""

    """
    The algorithm of the game is:
    When a game starts, a table is created with its shoe, the dealer, a list of players.
    The first serve is done, a pair of cards to the players and a single card to the dealer.
    Check for any of the player has a blackjack and pay him/her out immediately if the dealer's first card is not an ace
    or they allow them to decide on blackjack.
    Let the rest of the player decide their moves on each hand.
    A player can have more than one hand if he/she splits.
    After all players who have not burst, or surrender are standing, let the dealer draw till 17 or more.
    Pay insurance off.
    Then pay all active players; Payment could negative for loses.
    
    NOTE:
        Every player starts a balance of $1000.00
        The project is still under development.
    """

    print("Welcome to the game of Black Jack.")
    print("Please input ('ST' for STAND) ('HT' for HIT) "
          "('DD' for DOUBLING DOWN) ('SP' for SPLIT) ('SU' for SURRENDER).\n")

    # Asking for the number of players to create
    input_message, error_massage = "How many players are playing: ", "Number of players can only be between 1-6: "
    input_range = range(1, 7)
    no_players = input_handler.get_input_int(input_message, error_massage=error_massage, input_range=input_range)
    print()
    table = Table(no_players)
    table.first_serve()
    table.blackjack_or_insure_players()
    table.players_decide()
    table.dealer_draw_card()
    table.pay_insurance()
    table.pay_all_active_standing_players()
    table.print_players_info()
    print(table)
