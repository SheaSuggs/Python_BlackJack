import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack': 10, 'Queen':10 , 'King':10, 'Ace':11}

playing = True 

class Card():
     
    def __init__(self, suit, ranks):
         self.suit = suit
         self.rank = ranks

    def __str__(self):
        return self.rank + " of " + self.suit

class Deck():

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has: " + deck_comp
    
    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card
        
class Hand: 
    def __init__(self) -> None:
        self.cards = [] #starts with an empty list as we did in the deck class 
        self.value = 0 # start with zero value 
        self.aces = 0 # add an attribute to keep track of aces
    
    def add_card(self,card): 
        #card passed in 
        # from deck.deal() --> single Card(suit, rank)
        self.cards.append(card)
        self.value += values[card.rank]

        #track aces
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):

        while self.value > 21 and self.aces: 
            self.value -= 10
            self.aces -= 1

class chips: 
    def __init__(self, total=100):
        self.total = total 
        self.bet = 0
    
    def win_bet(self):
        self.total += self.bet 
    
    def lose_bet(self):
        self.total -= self.bet 


def take_bet(chips):
    while True:
        try: 
            chips.bet = int(input("how many chips would you like to bet?"))
        except: 
            print("sorry please provide an integer")
            print("please be sure that the value of the bet is less then what you have in total")
        else:
            if chips.bet > chips.total:
                print("sorry, you do not have enough chips! you have: {}".format(chips.total))
            else:
                break 

def hit(deck,hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing # to control an upcoming while loop
    
    while True:
        x = input('Hit or Stand? Enter h or s: ')
        if x[0].lower() == 'h':
            hit(deck, hand)

        elif x[0].lower() == 's':
            print("Player Stands Dealer's Turn")
            playing = False

        else: 
            print("Sorry, please try again. ")
            continue

        break

def show_some(player, dealer):
    #this function is to show the dealers cards at the start of the round/game

    # dealer .card[1]

    #show only one fo the dealer's cards
    print("\n Dealer's Hand: ")
    print("First card hidden! ")
    print(dealer.cards[1])
    print(dealer.value)

    #show all (2 cards) of the player's hand/cards
    print("\n player's hand: ")
    for card in player.cards: 
        print(card)
    
    print(player.value)

def show_all(player, dealer):
    #show all the dealer's cards 

    print("\n Dealer's hand: ")
    for card in dealer.cards: 
        print(card)
    #This would also work to print instead of the for loop above - print("\n Dealer's hand: , *dealer.cards,sep='\n")

    #calculate and display values (j+k)
    print(f"value of the dealer's hand is: {dealer.value}")

    #show all the players cards 
    print("\n player's hand: ")
    for card in player.cards: 
        print(card)

    # print the players card value 
    print(f"The value of the players hand is: {player.value}")

def player_busts(player,dealer,chips):
    print("Bust Player")
    print("Player Lost")
    chips.lose_bet()
def player_wins(player,dealer,chips):
    print("Player WINS")
    chips.win_bet()
def dealer_busts(player,dealer,chips):
    print("Dealer WINS!")
    chips.win_bet()
def dealer_wins(player,dealer,chips):
    print("Dealer WINS")
    chips.lose_bet()
def push(player, dealer):
    print("Dealer and player tie! Its a PUSH!!")
        

def main():
    global playing
    playing = True

    #opening 
    print("welcome to Shea's Black Jack table")
    #create and shuffle the deck and deal two cards to the dealer and the player 
    deck = Deck()
    deck.shuffle()
    #cards to the player 
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    #cards to the dealer 
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    #set up the players chips 
    player_chips = chips()


    while playing: 

        #Prompt the player for thier bet 
        take_bet(player_chips)

        #show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)
        
        #ask the user if they would like to hit or stand 
        hit_or_stand(deck,player_hand)
        #show the player his cards but keep the dealers hidden still 
        show_some(player_hand,dealer_hand)
        #If plauer's hand exceeds 21, run player_busts() and break out of loo[ 
        if player_hand.value > 21:
            print("Game Over")
            player_busts(player_hand, dealer_hand, player_chips)
            break 
        
        #if player ahsnt busted, player dealer's hand intil dealer reaches 17 
        if player_hand.value <= 21: 

            while dealer_hand.value < 17:
                hit(deck,dealer_hand)
            # show all cards 
            show_all(player_hand, dealer_hand)
            #run different winning scenarios 
            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand, player_chips)
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, player_chips)
            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand,dealer_hand,player_chips)
            else: 
                push(player_hand,dealer_hand)

        print(f"\n Player total chips are at: {player_chips.total}")
        # ask the player if they want to play again 
        playAgain = input("Would you like to play another hand? y/n: ")

        if playAgain[0].lower() == 'y':
            playing = True 
            continue 
        else:
            print("Thanks for playing see you next time")
            break


main()