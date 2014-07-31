#!/usr/bin/python
import random

global status
class Card:
	def RandomCard(self):
		cards = ["2","3","4","5","6","7","8","9","J","Q","K","A"]
		return cards[random.randint(0,len(cards)-1)]
	def __init__(self):
		self.value = self.RandomCard()
	def getValue(self):
		return self.value

class Hand():
	def __init__(self):
		self.cards = []
	def getFirst(self):
		if len(self.cards) >= 1:
			return self.cards[0]
	def addCard(self):
		card = Card()
		self.cards.append(card)
	def getCards(self):
		return self.cards
	def getTotal(self):
		total = 0
		aces = 0
		for card in self.cards:
			if card.getValue() == "K" or card.getValue() == "Q" or card.getValue() == "J":
				total = total + 10
			elif card.getValue() == "A":
				aces = aces + 1
			else:
				total = total + int(card.getValue())
		if aces >= 0:
			for i in range(0,aces):
				
				if total <= 10:
					total = total + 11
				else:
					total = total + 1
		return total
				 
class Dealer:
	def __init__(self):
		self.hand = Hand()
		self.hand.addCard()
		self.hand.addCard()
	def showHand(self):
		return self.hand.getFirst()
	def showFullHand(self):
		print "Dealer has: ",
		for card in self.hand.getCards():
			print card.getValue() + " ",
		print "Total: " + str(self.hand.getTotal())
	def getHand(self):
		return self.hand
class Player:
	def __init__(self,bet):
		self.bank = 1000.0
		self.bet = bet
		self.setBet(bet)
		self.hand = Hand()
		self.hand.addCard()
		self.hand.addCard()
	def newHand(self):
		self.hand = Hand()
		self.hand.addCard()
		self.hand.addCard()
	def showHand(self):
		print "[" + str(self.getBank()) + "] " +  "Player has: ",
		for card in self.hand.getCards():
			print card.getValue() + " ",
		print "Total: " + str(self.hand.getTotal())
	def getHand(self):
		return self.hand
	def getBet(self):
		return self.bet

	def getBank(self):
		return self.bank
	def addBank(self,win):
		self.bank = self.bank + win
	def setBet(self,bet):
		self.bet = bet
		self.bank = self.bank - float(bet)
		if self.bank < 0:
			print "Not enough, betting everything..."
			self.bank = self.bank + float(bet)
			self.bet = self.bank
			self.bank = 0
			
		

class GameState:
	def __init__(self, bet, player):
		self.dealer = Dealer()
		if player:
			self.player = player
			self.player.setBet(bet)
			self.player.newHand()
		else:
			self.player = Player(bet)
		self.go = True
	def showDealer(self):
		print "Dealer has: " + self.dealer.showHand().getValue()
	def showPlayer(self):
		self.player.showHand()
	def getPlayer(self):
		return self.player
	def getDealer(self):
		return self.dealer
	def stop(self):
		self.go = False
	def cont(self):
		return self.go
	def getState(self):
		global status
		if status == False:
			return False
		choice = raw_input("Bet again? [Y/n] ")
		if choice == "y" or choice == "Y" or choice == "":
			status = True
		else:
			status = False
		return status

def printGreeting(game):
	try:
		
		print "[Default: 100] ",
		bet = raw_input("Enter bet: ")
		if bet == "":
			bet = 100.0
		while(float(bet) < 0.0):
			print "Not today partner"
			bet = raw_input("Enter bet: ")
		if not game:
			game = GameState(bet,"")
		else:
			game = GameState(bet,game.getPlayer())
		game.showDealer()
		game.showPlayer()

		return game
	except ValueError:
		print "Input Error"
		exit(0)
		

def getChoice():
	print "(h)it, (s)tand, (d)ouble, s(p)lit, s(u)rrender"
	print "----------------------------------------------"
	choice = raw_input("Enter choice: ")
	if choice == "h":
		choice = 0
	elif choice == "s":
		choice = 1
	elif choice == "d":
		choice = 2
	elif choice == "p":
		choice = 3
	elif choice == "u":
		choice = 4
	else:
		choice = -1
	return choice	

def handleChoice(game, choice):
	global status
	player = game.getPlayer()
	dealer = game.getDealer()

	pTotal = player.getHand().getTotal()
	dTotal = dealer.getHand().getTotal() 
	if pTotal == 21 and dTotal != 21:
		print "Blackjack!"
		win = float(player.getBet())*2 + float(player.getBet())*1.5
		print "You won "  + str(win)
		player.addBank(win)
		game.stop()
		return game
	elif pTotal == 21 and dTotal == 21:
		print "PUSH!"
		win = float(player.getBet())*2
		print "You won " + str(win)
		player.addBank(win)
		game.stop()
		return game
	elif dTotal == 21:
		print "Dealer blackjack!"
		game.stop()
		return game


	# Hit
	if choice == 0:
		player.getHand().addCard()
		game.showDealer()
		game.showPlayer()

		if player.getHand().getTotal() > 21:
			print "BUST!"
			print "You lose " + str(player.getBet())
			game.stop()
		elif player.getHand().getTotal() == 21:
			print "WIN!"
			win = float(player.getBet())*2
			print "You win " + str(win)
			player.addBank(win)
			game.stop()
		return game	
	# Stand
	elif choice == 1:
		while dealer.getHand().getTotal() <= 21:
			dealer.showFullHand()
			if dealer.getHand().getTotal() > player.getHand().getTotal():
				print "LOSE!"
				print "You lose " + str(player.getBet())
				game.stop()
				return game
			dealer.getHand().addCard()
		dealer.showFullHand()
		print "Dealer bust!"
		win = float(player.getBet())*2
		print "You win " + str(win)
		player.addBank(win)
		game.stop()
		return game
	# Double
	elif choice == 2:
		if player.getBank() < 2*player.getBet():
			print "Not enough! "
			choice = getChoice()
			return handleChoice(game, choice)
		player.setBet(player.getBet()*2)
		player.getHand().addCard()
		dealer.getHand().addCard()

		dealer.showFullHand()
		game.showPlayer()

		if player.getHand().getTotal() > dealer.getHand().getTotal():
			if player.getHand().getTotal <= 21:
				print "WIN!"
				win = float(player.getBet())*2
				print "You win " + str(win)
				player.addBank(win)
				game.stop()
			else:
				print "LOSE!"
				print "You lose " + str(player.getBet())
				game.stop()
		elif player.getHand().getTotal() == dealer.getHand().getTotal():
			print "PUSH!"
			win = float(player.getBet())
			print "You win " + str(win)
			player.addBank(win)
			game.stop()
		else:
			if dealer.getHand().getTotal() <= 21:
				print "LOSE!"
				print "You lose " + str(player.getBet())
				game.stop()
			else:
				print "WIN!"
				win = float(player.getBet())*2
				print "You win " + str(win)
				player.addBank(win)
				game.stop()
	# Split
	elif choice == 3:

		if len(player.getHand().getCards()) != 2:
			print "Can't do that!"
			choice = getChoice()
			return handleChoice(game, choice)
		cards = player.getHand().getCards()

		if cards[0].getValue() != cards[1].getValue():
			print "Can't do that!"
			choice = getChoice()
			return handleChoice(game, choice)	
	# Surrender
	elif choice == 4:
		print "SURRENDER!"
		win = float(player.getBet())*0.5
		print "You win " + str(win)
		player.addBank(win)
		game.stop()
			
	return game

def begin(game):
	global status

	game = printGreeting(game)
	while game.cont() == True:
		choice = getChoice()
		game = handleChoice(game, choice)
	
	if game.getPlayer().getBank() == 0:
		print "Game over, go home"
		status = False
	print "[" + str(game.getPlayer().getBank()) + "] ",

	return game
if __name__=="__main__":
	try:
		status = True
		print "Welcome to Blackjack"
		print "--------------------"
		print "Putting 1000.0 in the bank"
		game = begin("")
		while game.getState():
			game = begin(game)
			continue
	except KeyboardInterrupt:
		print "Bailing!"
		exit(0)
	except EOFError:
		print "Bailing!"
		exit(0)
