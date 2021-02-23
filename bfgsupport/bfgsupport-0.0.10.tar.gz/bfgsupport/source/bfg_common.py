"""Common routines for Bfg and Kivy screens."""
# import random
import os
import shutil

from bridgeobjects import Auction, SEATS, CALLS
from .dealer import Dealer

STAGE_NO_FORCE_OVERCALL = [
        _('Response to 2NT'),
        _('Response to 2C'),
    ]

OVERCALL_CHOICES = [
        'No overcalls',
        'Allow overcalls',
        'Force overcalls',
    ]


# def get_stage_and_board(stages, seat_index=None, dealer=None, allow_overcalls=True):
#     """Return a board relevant to set stages."""
#     stage = random.choice(stages)
#     hand_dealer = Dealer(seat_index, allow_overcalls)

#     # Solo hands
#     if stage == _('Opening ones'):
#         board = hand_dealer.deal_opening_one_board(seat_index)
#     elif stage == _('Limit bids'):
#         board = hand_dealer.deal_limit_bids_responder_board(seat_index)
#     elif stage == _('Response in new suit'):
#         board = hand_dealer.deal_respond_in_new_suit_board(seat_index)
#     elif stage == _('Balanced rebids'):
#         board = hand_dealer.deal_balanced_rebid_board(seat_index)
#     elif stage == _('Single suited rebids'):
#         board = hand_dealer.deal_single_suited_rebid_board(seat_index)
#     elif stage == _('Two suited rebids'):
#         board = hand_dealer.deal_two_suited_rebid_board(seat_index)
#     elif stage == _('Support for responder'):
#         board = hand_dealer.deal_support_for_responder_board(seat_index)
#     elif stage == _('Raise responders NT'):
#         board = hand_dealer.deal_raise_responder_nt_board(seat_index)
#     elif stage == _('Response to weak two'):
#         board = hand_dealer.deal_response_to_weak_two_board(seat_index)
#     elif stage == _('Response to 2NT'):
#         board = hand_dealer.deal_response_to_two_nt_board(seat_index)
#     elif stage == _('Response to 2C'):
#         board = hand_dealer.deal_response_to_two_clubs_board(seat_index)

#     # Duo hands
#     elif stage == '20+ points hand':
#         board = hand_dealer.twenty_plus_hand()
#     elif stage == '23+ points hand':
#         board = hand_dealer.twenty_three_plus_hand()
#     elif stage == 'Weak NT':
#         board = hand_dealer.weak_nt_hand()
#     elif stage == 'Strong NT':
#         board = hand_dealer.strong_nt_hand()
#     elif stage == '5 card majors':
#         board = hand_dealer.five_card_major_opening()
#     elif stage == 'Benji 2C opening hand':
#         board = hand_dealer.benji_two_club_hand()
#     elif stage == 'Slam potential':
#         board = hand_dealer.slam_potential_hand()
#     elif stage == 'Jacoby 2NT':
#         board = hand_dealer.jacoby_2nt_board()
#     elif stage == 'Negative doubles':
#         board = hand_dealer.negative_double_hand(dealer)
#     elif stage == 'Splinters':
#         board = hand_dealer.splinter_board(dealer)
#     elif stage == 'Unassuming Cue bids':
#         board = hand_dealer.unassuming_cue_bid_board(dealer)
#     elif stage == 'Take-out doubles':
#         board = hand_dealer.take_out_double_board(dealer)
#     elif stage == 'xxx':
#         board = hand_dealer.deal_random_board()
#     else:
#         dealer = Dealer()
#         board = hand_dealer.deal_random_board()
#     return stage, board


def get_random_board(max_bids, dealer='N'):
    """Generate a 'biddable' random board."""
    allowed = False
    board = None
    while not allowed:
        board = Dealer(dealer).deal_random_board()
        auction = get_auction(board)
        dealer_index = SEATS.index(board.dealer)
        # This ensures that the number of bids fits on the screen.
        if len(auction.calls) + dealer_index <= max_bids:
            allowed = True
    return board


def get_auction(board, test=False):
    """Generate the auction."""
    if test:
        player_index = 0
    else:
        player_index = board.dealer_index
    auction_calls = []
    board.bid_history = []
    while not three_final_passes(auction_calls):
        player = board.players[player_index]
        # print('get_auction', player_index, board.players[player_index].hand)
        bid = player.make_bid()
        auction_calls.append(bid)
        player_index += 1
        player_index %= 4
    auction = Auction()
    auction.calls = auction_calls
    return auction


def three_final_passes(calls):
    """Return True if there have been three consecutive passes."""
    three_passes = False
    if len(calls) >= 4:
        if calls[-1].is_pass and calls[-2].is_pass and calls[-3].is_pass:
            three_passes = True
    return three_passes


def get_hand_for_seat(board, seat):
    """Return the correct hand for user's seat for the board."""
    seat_index = SEATS.index(seat)
    dealer_index = SEATS.index(board.dealer)
    distance_from_dealer = (seat_index - dealer_index) % 4
    hand = board.hands[distance_from_dealer]
    return hand


def display_bids(parent):
    """Assign the bids for an auction."""
    seat = SEATS.index(parent.user.seat)
    dealer = SEATS.index(parent.board.dealer)

    # if this is the first round of bidding, the bidder starts with dealer
    # otherwise the player on the left of the 'seat' has to bid
    if not parent.first_bid:
        bid_name = parent.auction.calls[parent.call_index].name
        parent.bid_list[parent.call_index + dealer] = parent.get_bid_image(bid_name)

        # move on to next bidder
        parent.call_index += 1

    while ((parent.call_index + dealer) % 4 != seat and
           parent.call_index < len(parent.auction.calls)):
        bid_name = parent.auction.calls[parent.call_index].name
        parent.bid_list[parent.call_index + dealer] = parent.get_bid_image(bid_name)
        parent.call_index += 1
    parent.first_bid = False


def three_passes_made(parent):
    """Return True if there have been three consecutive passes."""
    if parent.first_bid:
        three_passes_found = False
    elif parent.call_index <= 3:
        three_passes_found = False
    else:
        three_passes_found = True
        for call in parent.board.auction.calls[parent.call_index - 3:parent.call_index]:
            if not call.is_pass:
                three_passes_found = False
                break
    return three_passes_found


def is_insufficient_bid(parent, bid_value):
    """Return True if the bid_value is insufficient."""
    last_bid = -1
    if parent.call_index == 0:
        return False
    else:
        for bid in parent.board.bid_history[parent.call_index - 1::-1]:
            if bid != 'P' and bid != 'D':
                last_bid = CALLS.index(bid)
                break
        this_bid = CALLS.index(bid_value)
        if this_bid > last_bid:
            return False
        else:
            return True


def _tag(colour, end_tag=False):
    """Return a html tag of the colour."""
    if end_tag:
        text = '</{}>'
    else:
        text = '<{}>'
    return text.format(colour)


def convert_text_to_html(text):
    """Convert proprietary text to html."""
    html = text
    for colour in ['red', 'blue', 'green', 'yellow']:
        if _tag(colour) in text:
            new_text = '<span style="color:{}">'.format(colour)
            html = html.replace(_tag(colour), new_text)
        if _tag(colour, True) in text:
            html = html.replace(_tag(colour, True), '</span>')
    return html


def hands_bid_increment(self):
    """Increment hand count."""
    self.config.all_hands_count += 1
    self.config.term_hands_count += 1
    self.config.session_hands_count += 1


def correct_bid_increment(self):
    """Increment correct bid count."""
    self.config.all_hands_correct += 1
    self.config.term_hands_correct += 1
    self.config.session_hands_correct += 1


def abbreviate_bid(bid_name):
    """Return the abbreviation of non-value bids."""
    if bid_name == 'PASS':
        return 'P'
    elif bid_name == 'DOUBLE':
        return 'D'
    else:
        return bid_name


def build_and_deploy_translations_file():
    """Create the .pot file, build an .mo and deploy the .mo to locale(s)."""
    print('build_and_deploy_translations_file', os.getcwd())

    def _add_items_to_pot(pot_list, comment_list):
        """Append message items to pot_list."""
        index = -1
        for index, line in enumerate(comment_list):
            if 'msgid' in line:
                break
        assert index >= 0, 'index not assigned'
        pot_list.extend(comment_list[index - 2:])
        return pot_list

    # Merge bfg_text.pot, bid_comments.txt and bid_strategy.txt into bfg.pot and
    source_directory = 'comment_editor/data/'
    destination_directory = '../bfg_components/bfg_components/locale/'
    message_suffix = 'dist/locale/en_GB/LC_MESSAGES/'
    messages_directory = destination_directory + 'en_GB/LC_MESSAGES/'
    target_directories = ['bfg_python', 'deal_display', 'comment_viewer', 'bfg_kivy']

    with open(source_directory + 'bfg_text.pot', 'r') as f_bfg_pot:
        bfg_pot_text = f_bfg_pot.read()
        bfg_pot_list = bfg_pot_text.split('\n')
    print(len(bfg_pot_list))

    with open(source_directory + 'bid_comments.txt', 'r') as f_bid_comments:
        bid_comments_text = f_bid_comments.read()
        bid_comments_list = bid_comments_text.split('\n')
    print(len(bid_comments_list))

    with open(source_directory + 'bid_strategy.txt', 'r') as f_bid_strategy:
        bid_strategy_text = f_bid_strategy.read()
        bid_strategy_list = bid_strategy_text.split('\n')
    print(len(bid_strategy_list))

    bfg_pot_list = _add_items_to_pot(bfg_pot_list, bid_comments_list)
    bfg_pot_list = _add_items_to_pot(bfg_pot_list, bid_strategy_list)

    # save bfg.pot in ../bfg_components/bfg_components/locale
    with open(destination_directory + 'bfg.pot', 'w') as f_bfg_pot:
        bfg_pot_text = '\n'.join(bfg_pot_list)
        f_bfg_pot.write(bfg_pot_text)

    # copy bfg.pot to ../bfg_components/bfg_components/locale/en_GB/LC_MESSAGES
    shutil.copyfile(destination_directory + 'bfg.pot', messages_directory + 'bfg.po')

    # cd to ../bfg_components/bfg_components/locale/en_GB/LC_MESSAGES
    # build the bfg.mo
    current_dir = os.getcwd()
    os.chdir(messages_directory)
    os.system('ls -l')
    os.chdir(current_dir)

    # copy the .mo to bfg_python, comment_editor and comment_viewer.
    for target in target_directories:
        target_dir = '../' + target + os.sep + target + os.sep + message_suffix
        shutil.copyfile(messages_directory + 'bfg.mo', target_dir + 'bfg.mo')
