""" Bid for Game
    BiddingBoard class
"""

from datetime import datetime

from .player import Player
from bridgeobjects import Hand, Board, RANKS, SEATS, parse_pbn


class BiddingBoard(Board):
    """Define BfG BiddingBoard class."""
    SEAT_SEATS = [_('N'), _('E'), _('W'), _('S'), _('Random')]
    SLAM_POINTS = 32

    def __init__(self, *args, **kwargs):
        super(BiddingBoard, self).__init__(*args, **kwargs)
        self.description = ''
        self.bid_history = []
        self.active_bid_history = []
        self._stage = None
        self.players = {}
        for index in range(4):
            self.players[index] = Player(self, None, index)
        self.check_bids = []
        self._dealer = None

    def __repr__(self):
        """Return a string representation of the deal."""
        cards = [card.name for card in self.hands[0].cards]
        return 'BiddingBoard: {}'.format(':'.join(cards))

    def __str__(self):
        cards = [card.name for card in self.hands[0].cards]
        """Return a string representation of the deal."""
        return "BiddingBoard: North's hand {}".format(':'.join(cards))

    @property
    def stage(self):
        """Assign stage property."""
        return self._stage

    @stage.setter
    def stage(self, value):
        """Return stage property."""
        self._stage = value

    def deal_from_pbn(self, pbn_string):
        """Create a deal from pbn_string."""
        pass

    def set_description(self, description):
        """Set the BiddingBoard description."""
        self.description = description

    @staticmethod
    def _default_hands():
        hands = []
        dummy_hand = ['AS', 'KS', 'QS', 'JS', 'TS', '9S', '8S',
                      '7S', '6S', '5S', '4S', '3S', '2S']
        hands.append(Hand(dummy_hand))
        dummy_hand = [hand.replace('S', 'H') for hand in dummy_hand]
        hands.append(Hand(dummy_hand))
        dummy_hand = [hand.replace('H', 'D') for hand in dummy_hand]
        hands.append(Hand(dummy_hand))
        dummy_hand = [hand.replace('D', 'C') for hand in dummy_hand]
        hands.append(Hand(dummy_hand))
        return hands

    def parse_pbn_deal(self, deal, delimiter=":"):
        """Return a list of hands from a pbn deal string."""
        # example deal
        #   ['[Board "Board 1"]', '[Dealer "N"]',
        #    '[Deal "N:JT84.A987.8.T982 AKQ.KQ54.KQ2.A76 7652.JT3.T9.KQJ5 93.62.AJ76543.43"]']
        # hands = [None, None, None, None]
        # # Assign hands to board in correct position
        # self._dealer = deal[0]
        # hand_index = self._get_pbn_dealer_index(deal)
        # raw_hands = deal[2:].split(delimiter)
        # for card_list in raw_hands:
        #     hand = Hand(card_list)
        #     hands[hand_index] = hand
        #     hand_index = (hand_index + 1) % 4
        event = parse_pbn(deal)[0]
        board = event.boards[0]
        self.description = board.description
        self.dealer = board.dealer
        self.hands = board.hands
        for index in range(4):
            self.players[index].hand = self.hands[index]
        return board.hands

    def _get_pbn_dealer_index(self, deal):
        """
            Return the first hand index to ensure that the first hand
            assigned to the board's hands list is that of the board dealer.
        """
        # first_hand is the position index of the first hand given in the deal
        first_hand = SEATS.index(deal[0])

        # dealer_index is the position index of the dealer
        dealer_index = SEATS.index(self.dealer)

        # rotate the hand index to ensure that the
        # first hand created is the dealer's
        hand_index = (first_hand - dealer_index) % 4
        return hand_index

    def create_pbn_list(self):
        """Return a board as a list of strings in pbn format."""
        deal_list = ['[Event "bfg generated deal"]',
                     '[Date "{}"]'.format(datetime.now().strftime('%Y.%m.%d')),
                     '[Board "{}"]'.format(self.description),
                     '[Dealer "{}"]'.format(self.dealer),
                     '[Deal "{}:{}"]'.format(self.dealer, self._get_deal_pbn(' ')),
                     '']
        return deal_list

    def _get_deal_pbn(self, delimiter=' '):
        """Return a board's hands as a string in pbn format."""
        hands_list = []
        for _, hand in self.hands.items():
            hand_list = []
            for _ in range(4):
                hand_list.append(['']*13)
            for card in hand.cards:
                suit = 3 - card.suit.rank
                rank = 13 - RANKS.index(card.rank)
                hand_list[suit][rank] = card.name[0]
            for index in range(4):
                hand_list[index] = ''.join(hand_list[index])
            hands_list.append('.'.join(hand_list))
        return delimiter.join(hands_list)

    @staticmethod
    def rotate_board_hands(board, increment=1):
        """Return the hands rotated through increment clockwise."""
        rotated_hands = {}
        hands = board.hands
        for index in range(4):
            rotated_index = (index + increment) % 4
            if index in hands:
                rotated_hands[rotated_index] = hands[index]
                board.players[rotated_index].hand = hands[index]
            if SEATS[index] in hands:
                rotated_hands[SEATS[rotated_index] ] = hands[SEATS[index]]
        board.hands = rotated_hands
        return board
