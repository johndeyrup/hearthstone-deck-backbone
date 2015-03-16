'''
Created on Sep 6, 2014
A hearthstone deck simulator
@author: John
'''
from random import shuffle
from random import randint
import json
from tkinter import *
import urllib.request

#Card class, which contains a dictionary of its stats
class Card(object):      
    #Initiate card  
    def __init__(self, a_card):
        self.card_dic = a_card
    #Return stats of card
    def get_card(self):
        return self.card_dic
    
#Deck class, which contains cards
class Deck(object):
    #Initiate deck class
    def __init__(self, deck_size, deck_list):
        self.size = deck_size
        self.dec_list = deck_list
        self.shuf_list = []
    #Shuffle deck
    def shuffle_list(self):
        shuffle(self.dec_list)
        self.shuf_list = [i.get_card() for i in self.dec_list]
    #Returns the first 4 cards    
    def start_hand(self):
        return self.shuf_list[:4]
    
#Hand class, contains cards which are visible to the player    
class Hand(object):
    #Initiate hand class
    def __init__(self, player_handsize, player_card):
        self.hand_dic = {
                         "handsize" : player_handsize,
                         "cards" : player_card
                         }        
    #Return cards in hand    
    def get_hand(self):
        return self.hand_dic["cards"]

#Player class, a player has class, life total, available crystals
class Player(object):
    #Initiate player class
    def __init__(self, player_class, player_life, hand, is_turn, crystal):
        self.player_dic = {
                    "class" : player_class,
                    "hand" : hand,
                    "life" : player_life,
                    "turn" : is_turn,
                    "crystal" : crystal,
                    "remaining_crystal" : crystal
                    }
    #Prints the cards in players hand
    def print_player(self):
        for card in self.player_dic["hand"].get_hand():
            print (card["name"]) 
        print (self.player_dic)

#Board class has a state of creatures and players
class Board(object):
    #Initiate board class
    def __init__(self):
        self.player1_cards = []
        self.player2_cards = []

#Get library of cards
def get_card_library(filename):
    json_data = open(filename)
    data = json.load(json_data)
    card_lib = data["cards"]
    json_data.close()
    return card_lib 

#Gets attributes of cards, you must put the cards exact name as key for the json dictionary
def get_card_atr(lib, card_name):
    for card in lib:
        if card['name'] == card_name:
            return card
            break

#Determine whether player 1 or player 2 goes first    
def det_turn():
    p1_turn = True
    p2_turn = False
    ran_x = randint(0,1)
    if(ran_x == 1):
        p1_turn = False
        p2_turn = True
    return p1_turn, p2_turn
            
#Initialize Cards
card_library = get_card_library('all_cards.json')   
argent_squire = Card(get_card_atr(card_library, "Argent Squire"))         
swamp_ooze = Card(get_card_atr(card_library, "Acidic Swamp Ooze"))
amani_ber = Card(get_card_atr(card_library, "Amani Berserker"))

#Initialize Deck, it is made up of card objects
p1_dlist = [argent_squire, swamp_ooze, amani_ber, swamp_ooze]
p1_deck = Deck(40, p1_dlist)
p1_deck.shuffle_list()
  
#Initialize turns
is_p1_turn, is_p2_turn = det_turn()
      
#Add cards to players' hand
player1_hand = Hand(10, p1_deck.start_hand())
player1 = Player("Hunter", 20, player1_hand, is_p1_turn, 1)
 
#Initialize Board
board = Board()

#Places player 1's cards on   
def main():
    root = Tk()
    w = 800
    h = 600
    offsetw = (root.winfo_screenwidth()-w)/2
    offseth = (root.winfo_screenheight()-h)/2
   
    root.geometry("%dx%d+%d+%d"%(w,h,offsetw,offseth))
     
    root.attributes("-fullscreen",1)
    frm = Frame(root)
    frm.place()
    image_list = []
    for card in player1_hand.get_hand():
        image_list.append(PhotoImage(file=(urllib.request.urlretrieve(card["image_url"], "FP1_022.png")[0])))
        offsetx = 350
    for i in image_list:
        Label(root, image=i).place(x=offsetx, y=0)
        offsetx += 200
    player_lbl = Label(root, text='Player 1 Hand', font='20')
    player_lbl.pack()
    root.mainloop()
        
if __name__ == "__main__":
    main()
