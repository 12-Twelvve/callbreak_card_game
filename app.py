import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
#######################
# user defined function
def hello():
    print('hello')
def get_priority(s, c):
    return priority['suit'][s]+priority['card'][c]
def whole_13_cards(suit):
    ke= list(priority['card'].keys())
    return [i+suit for i in ke]

priority = {
    "suit":{
        "S":1,
        "H":20,
        "C":20,
        "D":20
    },
    "card":{
        "1":1,
        "K":2,
        "Q":3,
        "J":4,
        "T":5,
        "9":6,
        "8":7,
        "7":8,
        "6":9,
        "5":10,
        "4":11,
        "3":12,
        "2":13
    }
    
}
def get_highest_card(cards):
    high_card = cards[0]
    for e in cards:
        hcard_suit = get_suit(high_card)
        hcard_no = get_card_number(high_card)
        esuit = get_suit(e)
        eno = get_card_number(e)
        if get_priority(hcard_suit, hcard_no) > get_priority(esuit, eno):
            high_card = e
    return high_card

def get_smallest_card(cards):
    small_card = cards[0]
    for e in cards:
        scard_suit = get_suit(small_card)
        scard_no = get_card_number(small_card)
        esuit = get_suit(e)
        eno = get_card_number(e)
        if get_priority(scard_suit, scard_no) < get_priority(esuit, eno):
            small_card = e
    return small_card
     
def get_first_played_cards(cards):
    return cards[0]

def get_same_suit_cards(cards, suit):
    return [c for c in cards if c[-1]==suit]

def get_suit(card):
    return card[-1]

def get_card_number(card):
    return card[:-1]

def get_higher_same_suit_cards(g, hands):
    winning_cards = []
    gsuit = get_suit(g)
    gno = get_card_number(g)
    for e in get_same_suit_cards(hands, gsuit):
        esuit = get_suit(e)
        eno = get_card_number(e)
        if get_priority(gsuit, gno) >  get_priority(esuit, eno):
            winning_cards.append(e)
    return winning_cards
 
def is_card_highest_unplayed_card(card, droped_card):
    cardNo = get_card_number(card)
    cardSuit =  get_suit(card)
    l =priority['card'][cardNo]
    cards = whole_13_cards(cardSuit)
    for c in range(l-2,-1,-1):
        if cards[c] in droped_card:
            continue
        else:
            return False
    return True
    
def is_ace(card):
    if "1" == card[:-1]:
        return True
    else:
        return False
def is_king(card):
    if "K" ==card[:-1]:
        return True 
    else:
        return False
def is_Queen(card):
    if "Q" ==card[:-1]:
        return True 
    else:
        return False
def have_JQT(cards):
    for i in cards:    
        if 'J' in i or 'Q' in i or 'T' in i:
            return True
    return False
def have_JQKA(cards):
    for i in cards:    
        if 'J' in i or 'Q' in i  or 'K' in i or '1' in i:
            return True
    return False
def have_JQ(cards):
    for i in cards:    
        if 'J' in i or 'Q' in i:
            return True
    return False
def have_Q(cards):
    for i in cards:    
        if 'Q' in i :
            return True
    return False
def have_K(cards):
    for i in cards:
        if is_king(i):
            return True
    return False
def have_A(cards):
    for i in cards:
        if is_ace(i):
            return True
    return False

# ----------------------------------------------------------
def normalBidding(hands):
    count=0
    for i in hands:
        if get_suit(i) !='S':
            if is_ace(i):
                count+=1
            elif is_king(i):
                k_cards = get_same_suit_cards(hands, get_suit(i))
                if len(k_cards) < 4 and len(k_cards)>1:
                    count +=1
                elif have_JQT(k_cards) or have_A(k_cards) and len(k_cards) <= 6:
                    count += 1
    spades_in_hand =get_same_suit_cards(hands, "S")
    spades_length = len(get_same_suit_cards(hands, "S"))
    club_length = len(get_same_suit_cards(hands, "C"))
    diamond_length = len(get_same_suit_cards(hands, "D"))
    heart_length = len(get_same_suit_cards(hands, "H"))
    if  have_A(spades_in_hand):
        count += 1
        if have_K(spades_in_hand):
            count +=1
            if have_Q(spades_in_hand):
                count +=1
    if spades_length >=1:
        # for cut off
        if club_length < 1 or diamond_length < 1 or heart_length < 1:
            count +=1
        if club_length < 2 or diamond_length < 2 or heart_length < 2 and spades_length >=2:
            count +=1
        if club_length <= 2 or diamond_length <= 2 or heart_length <= 2 and spades_length >=3:
            count +=1        
    if count <= 0:
        return 1
    if count >=8:
        return 8
    else:
        return count
def hardBidding(hands):
    count=0
    C = get_same_suit_cards(hands, "C")
    D = get_same_suit_cards(hands, "D")
    H = get_same_suit_cards(hands, "H")
    S = get_same_suit_cards(hands, "S")
    for i in hands:
        if is_ace(i):
            count+=1
        elif is_king(i):
            k_cards = get_same_suit_cards(hands, get_suit(i))
            if len(k_cards) <= 3 and len(k_cards)>1:
                count +=1
            else:
                if have_A(k_cards) and len(k_cards) <=6 or have_JQT(k_cards)  and len(k_cards) <= 6:
                    count += 1
        elif is_Queen(i):
            q_cards = get_same_suit_cards(hands, get_suit(i))
            if 4>=len(C)>=3 and 4>=len(D)>=3  and 4>=len(H)>=3:
                if have_K(q_cards) and have_A(q_cards):
                    count +=1
    spades_length = len(S)
    if spades_length>6:
        if have_K(S):
            count +=1
        if have_Q(S):
            count +=1
    if len(C)<2:
        count+=1
    if len(D)<2:
        count+=1
    if len(H)<2:
        count+=1
    if spades_length > 3:
        count += spades_length-3
    if 2<spades_length<4:
        if len(C)<2 or len(H)<2 or len(D)<2:
            count +=2
    if count >=8:
        return 8
    if count <= 0:
        return 1
    else:
        return count
def softBidding(hands):
    count=0
    for i in hands:
        if is_ace(i):
            count+=1
        elif is_king(i):
            k_cards = get_same_suit_cards(hands, get_suit(i))
            if len(k_cards) < 4 and have_A(k_cards):
                count +=1
    spades_length = len(get_same_suit_cards(hands, "S"))
    if spades_length > 4:
        count += spades_length-4
    if count <= 0:
        return 1
    if count >=8:
        return 8
    else:
        return count
def bidding(hands, context, player):
    g_round = context['round']
    if g_round ==5:
        players = context['players']
        my_score = players[player]['totalPoints']
        max_score=0.0
        high_bid_score = 0.0
        score =[]
        bid =[]
        # go for 20
        mybidValue = hardBidding(hands)
        if mybidValue + my_score >=20:
            dif = 20 - int(my_score)
            if dif <=mybidValue:
                return dif
        for ke in players:
            p_score = players[ke]['totalPoints']
            p_bid = players[ke]['totalPoints']
            score.append(p_score)
            if p_score > max_score and ke != player:
                max_score= players[ke]['totalPoints']
                max_score_player = ke
            if p_bid >0:
                bid.append(p_bid)
                bid_score = p_score + p_bid
                if bid_score > high_bid_score:
                    high_bid_score = bid_score
                    high_bid_score_player = ke

        if high_bid_score_player == max_score_player:
            if my_score > high_bid_score + 3:
                return softBidding(hands)

        if my_score > high_bid_score and my_score > max_score + 4:
            return softBidding(hands)   
        if len(bid)>=3:
            if high_bid_score > my_score:
                dif = int(high_bid_score) - int(my_score)
                if dif < 4 :
                    return dif+1
                    
            else:
                return softBidding(hands)
    hb = hardBidding(hands)
    # nb = normalBidding(hands)
    # print(hb, nb)
    return hb
# ----------------------------------------------------------
def othersDeal(hands, played, history, history_for_cutof):
        first_card = get_first_played_cards(played)
        first_suit = get_suit(first_card)
        list_of_same_cards = get_same_suit_cards(hands, first_suit)
        if not list_of_same_cards:
            spades_in_hand = get_same_suit_cards(hands, "S")
            spades_in_played_cards = get_same_suit_cards(played, "S")
            list_of_same_history_cards = get_same_suit_cards(history, first_suit)
            if not spades_in_played_cards:
                if not spades_in_hand:
                    return get_smallest_card(hands)
                else:
                    if len(played)>=3:
                        return get_smallest_card(spades_in_hand)
                    histroy_spades = get_same_suit_cards(history,"S")
                    if len(spades_in_hand + histroy_spades)>=13:
                        return get_smallest_card(spades_in_hand)
                    if len(list_of_same_history_cards)>=8:
                        highest_spade = get_highest_card(spades_in_hand)
                        if is_card_highest_unplayed_card(highest_spade ,histroy_spades):
                            return highest_spade
                    return get_smallest_card(spades_in_hand)
            else:
                hspades_in_played_card = get_highest_card(spades_in_played_cards)
                list_of_higher_spades_card= get_higher_same_suit_cards(hspades_in_played_card, spades_in_hand)
                if not list_of_higher_spades_card:
                    card_to_return = get_smallest_card(hands)
                else:
                    if len(played)>=3:
                        return get_smallest_card(list_of_higher_spades_card)
                    if len(list_of_same_history_cards)>=10:
                        highest_spade = get_highest_card(spades_in_hand)
                        histroy_spades = get_same_suit_cards(history,"S")
                        if is_card_highest_unplayed_card(highest_spade ,histroy_spades):
                            return highest_spade
                    return get_smallest_card(list_of_higher_spades_card)
        else:
            highest_played_card = get_highest_card(played)
            if get_suit(highest_played_card) == 'S' and "S"!=first_suit:
                card_to_return = get_smallest_card(list_of_same_cards)
            else:

                list_of_same_played_cards = get_same_suit_cards(played, first_suit)
                list_of_history_spades = get_same_suit_cards(history, 'S')
                highest_suit_played_card = get_highest_card(list_of_same_played_cards)
                higher_cards = get_higher_same_suit_cards(highest_suit_played_card, hands)
                if not higher_cards:
                    card_to_return = get_smallest_card(list_of_same_cards)
                else:
                    if len(played)>=3:
                        return get_smallest_card(higher_cards)
                    if first_suit in find_cutOf_suit(history_for_cutof):
                        if len(list_of_history_spades)<8:
                            return get_smallest_card(higher_cards)
                            
                    highest_card = get_highest_card(higher_cards)
                    droped_cards = get_same_suit_cards(history, first_suit)
                    
                    if is_card_highest_unplayed_card(highest_card, droped_cards):
                        card_to_return = highest_card
                    else:
                        # ------
                        card_to_return = get_smallest_card(higher_cards)
        return card_to_return
def dealing_Spades(S, hist):
    drop_s = get_same_suit_cards(hist, 'S')
    h1 = get_highest_card(S)
    if is_card_highest_unplayed_card(h1, drop_s):
        if len(S)>1:
            h2 =get_highest_card([i for i in S + [h1] if i not in S or i not in [h1]])
            if is_Queen(h1)  or is_king(h1):
                return h1
            if is_card_highest_unplayed_card(h2, drop_s + [h1]):
                return h1
        if len(drop_s)>=8:
            return h1
    return None
     
def find_cutOf_suit(history):
    cut_off_suits=[]
    cut_off_suits_uniq = []
    for round in history:
        first_card_suit = get_suit(round[0])
        # second_card_suit = get_suit(round[1])
        # third_card_suit = get_suit(round[2])
        # forth_card_suit = get_suit(round[3]) 
        highest_card_suit =get_suit(get_highest_card(round))
        if first_card_suit != highest_card_suit and highest_card_suit=='S':
                cut_off_suits.append(first_card_suit)
    for x in cut_off_suits:
        if x not in cut_off_suits_uniq:
            cut_off_suits_uniq.append(x)   
    return cut_off_suits_uniq

def in_danger(cards, history):
    h = get_highest_card(cards)
    if is_king(h) and not is_card_highest_unplayed_card(h, history) and len(cards)>1:
        return True
    else :
        return False

def in_dhoosing(cards, history):
    h = get_highest_card(cards)
    if is_Queen(h) and not is_card_highest_unplayed_card(h, history) and len(cards)>1:
        return True
    else:
        return False

def choose_cards(cdh, history):
    functions = (in_danger, in_dhoosing)
    count =0
    for func in functions:
        for i in cdh:
            hist = get_same_suit_cards(history, get_suit(i[0]))
            if func(i, hist):return i ,count
        count +=1
    s_history = get_same_suit_cards(history, "S")
    if len(s_history) >= 13:
        for i in cdh:
            i_highest_card = get_highest_card(i)
            i_history_card = get_same_suit_cards(history, get_suit(i[0]))
            if is_card_highest_unplayed_card(i_highest_card,i_history_card):
                return i, count
        return max(cdh, key=len), count

    return min(cdh, key=len), count

   
def myDeal(hands, history, history_for_cutof):
    S = get_same_suit_cards(hands, "S")
    if S:
        card = dealing_Spades(S, history)
        if card:
            return card  
    C = get_same_suit_cards(hands, "C")
    D = get_same_suit_cards(hands, "D")
    H = get_same_suit_cards(hands, "H")
    cdh =[i for i in (C, D, H) if len(i)!=0]
    dealway=2
   
    if not cdh:
        # dealspades in regular manner
        s =[hands]
        choosed_suit_cards, dealway =choose_cards(s, history)
    else: 
         # play for danger card if not danger play with dhoosing card
        choosed_suit_cards, dealway = choose_cards(cdh, history) 
    spades_in_history = get_same_suit_cards(history, 'S')
    if len(S)<=2 and dealway==2 and not have_JQKA(S):
        if len(C)>=3  and len(D) >=3 and len(H)>=3:
            return S[0]
    if len(spades_in_history)>=13:
        c_in_history = get_same_suit_cards(history, 'C')
        d_in_history = get_same_suit_cards(history, 'D')
        h_in_history = get_same_suit_cards(history, 'H')
        if C:
            if is_card_highest_unplayed_card(C[0], c_in_history):
                return C[0]
        if D:
            if is_card_highest_unplayed_card(D[0], d_in_history):
                return D[0]
        if H:
            if is_card_highest_unplayed_card(H[0], h_in_history):
                return H[0]
    highest_card = get_highest_card(choosed_suit_cards)
    highest_card_suit = get_suit(highest_card)

    droped_cards = get_same_suit_cards(history, highest_card_suit)
    if is_card_highest_unplayed_card(highest_card, droped_cards):
        return highest_card
    else:
        if dealway ==0 or dealway==1:
            # for king and queen
            if len(choosed_suit_cards)<3:
                return choosed_suit_cards[len(choosed_suit_cards)//2]
            else:
                return choosed_suit_cards[2]
        return get_smallest_card(choosed_suit_cards)

# ----------------------------------------------------------
# def playing(hands, played, history): 
    

#######################
@app.route("/hi", methods=["GET"])
def hi():
    """
    This function is required to check for the status of the server.
    When docker containers are spun, this endpoint is called continuously
    to check if the docker container is ready or not.  
    Alternatively, if you need to do some pre-processing,
    do it first and then add this endpoint.
    """
    return jsonify({"value": "hello"})


@app.route("/bid", methods=["POST"])
def bid():
    body = request.get_json()
    # print(json.dumps(body, indent=2))

    ####################################
    #     Input your code here.        #
    cards= body['cards']
    context = body['context']
    playerId = body['playerId']

    bidValue =bidding(cards, context, playerId) 
    ####################################

    # return should have a single field value which should be an int reprsenting the bid value
    return jsonify({"value": bidValue})


@app.route("/play", methods=["POST"])
def play():


    body = request.get_json()
    print(json.dumps(body, indent=2))
 
    ####################################
    #     Input your code here.        #
    hands= body['cards']
    played = body['played']
    dirtyhistory= body['history']
    # for cutoff
    history_for_cutof= [h[1] for h in dirtyhistory]
    history = [card for h in dirtyhistory for card in h[1]]

    if played:
        mycard= othersDeal(hands, played, history, history_for_cutof)
    else:
        mycard= myDeal(hands, history, history_for_cutof)
    ####################################


    return jsonify({"value": mycard })


# Docker image should always listen in port 7000
app.run(host="0.0.0.0", port=7000)