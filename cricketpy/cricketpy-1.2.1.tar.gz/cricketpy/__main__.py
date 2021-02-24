from pyfiglet import Figlet
import math
import os
from criapi import Cricbuzz
def cricpy():
    c=Cricbuzz()
    f = Figlet(font='slant')
    print(f.renderText('CRICPY'))
    while 1:
        matches=c.livescore()
        scores=[]
        os.system( 'clear' )
        print('-'*100)
        for match in matches:
            score=match
            separator=' & '
            try:
                try:
                    batting=score['batting']['score']
                    board=[]
                    for bat in batting:
                        try:
                            board.append(bat['runs']+'-'+bat['wickets']+'('+bat['overs']+')')
                        except:
                            board.append(bat['runs']+'-'+bat['wickets'])
                    batting_score=separator.join(board)
                    print(score['batting']['team']+': '+batting_score)
                except:
                    print(score['batting']['team']+': ')
                try:
                    bowling=score['bowling']['score']
                    bboard=[]
                    for bowl in bowling:
                        try:
                            bboard.append(bowl['runs']+'-'+bowl['wickets']+'('+bowl['overs']+')')
                        except:
                            bboard.append(bowl['runs']+'-'+bowl['wickets'])
                    bowling_score=separator.join(bboard)
                    print(score['bowling']['team']+': '+bowling_score)
                except:
                    print(score['bowling']['team']+': ')
            except:
                matches.remove(match)
                continue
            print(match['status'])
            # print(match['venue_name'])
            print('-'*100)
            scores.append(score)
        print('match number:commentary,q:quit,r:refresh')
        choice=input()
        if choice=='q':
            os.system( 'clear' )
            exit()
        elif choice=='r':
            continue
        else :
            while 1:
                os.system( 'clear' )
                print('-'*100)
                matches=c.livescore()
                match=matches[int(choice)-1]
                score=match
                batting=score['batting']['score']
                bowling=score['bowling']['score']
                board=[]
                try:
                    for bat in batting:
                            try:
                                board.append(bat['runs']+'-'+bat['wickets']+'('+bat['overs']+')')
                            except:
                                board.append(bat['runs']+'-'+bat['wickets'])
                    batting_score=separator.join(board)
                    print(score['batting']['team']+': '+batting_score)
                except:
                    print(score['batting']['team']+': ')
                try:
                    bboard=[]
                    for bowl in bowling:
                            try:
                                bboard.append(bowl['runs']+'-'+bowl['wickets']+'('+bowl['overs']+')')
                            except:
                                bboard.append(bowl['runs']+'-'+bowl['wickets'])
                    bowling_score=separator.join(bboard)
                    print(score['bowling']['team']+': '+bowling_score)
                except:
                    print(score['bowling']['team']+': ')
                print(match['status'])
                # print(match['venue_name'])
                print('-'*100)
                commentary=c.commentary(match['id'])
                try:
                    batsmens=commentary['batsman']
                    print ("{:<20} {:<5} {:<5} {:<5} {:<5} {:<5}".format("Batsman", "R", "B", "4s","6s","SR"))
                    for batsmen in batsmens:
                        name=batsmen['name']
                        runs=batsmen['runs']
                        balls=batsmen['balls']
                        fours=batsmen['fours']
                        six=batsmen['six']
                        sr=batsmen['sr']
                        print ("{:<20} {:<5} {:<5} {:<5} {:<5} {:<5}".format(name,runs, balls, fours,six,sr))
                    print('-'*100)
                    print ("{:<20} {:<5} {:<5} {:<5} {:<5} {:<5}".format("Bowler", "O", "M", "R","W","ER"))
                    bowlers=commentary['bowler'][0]
                    bowler=bowlers['name']
                    overs=bowlers['overs']
                    maidens=bowlers['maidens']
                    runs=bowlers['runs']
                    wickets=bowlers['wickets']
                    balls=str((math.floor(float(overs))*6+math.floor((float(overs)-math.floor(float(overs)))*10))/6)
                    if balls==0:
                        er='0'
                    else:
                        er=str(round(int(runs)/float(balls),2))
                    print ("{:<20} {:<5} {:<5} {:<5} {:<5} {:<5}".format(bowler,overs,maidens,runs,wickets,er))
                    print('-'*100)
                except:
                    print("Match Completed")
                commentary=commentary['comm']
                for comment in commentary:
                    comm=comment['comm']
                    over=comment['over']
                    comm=comm.replace('<strong>','\033[91m')
                    comm=comm.replace('</strong>','\033[0m')
                    comm=comm.replace('<b>','\033[91m')
                    comm=comm.replace('</b>','\033[0m')
                    comm=comm.replace('<br/>','\n')
                    comm=comm.replace('<i>','\033[96m')
                    comm=comm.replace('</i>','\033[0m')
                    comm=comm.replace('<span class="over-summary">','')
                    comm=comm.replace('</span>','')
                    if over==None:
                        print(comm)
                    else:
                        print(over+': '+comm)
                print('-'*100)
                print('s:scorecard,b:back,r:refresh,q:quit')
                ch=input()
                if ch=='r':
                    continue
                elif ch=='b':
                    break
                elif ch=='q':
                    os.system( 'clear' )
                    exit()
                elif ch=='s':
                    scorecard=c.scorecard(match['id'])
                    inning=scorecard[0]
                    while 1:
                        os.system( 'clear' )
                        # print('-'*100)
                        # print(inning['batteam']+' '+inning['inng_num']+' '+inning['runs']+'-'+inning['wickets']+'('+inning['overs']+')')
                        # print('-'*100)
                        batsmens=inning['batcard']
                        print ("{:<20} {:<30} {:<5} {:<5} {:<2} {:<2} {:<5}".format("Batsman","Dismissal", "R", "B", "4s","6s","SR"))
                        for batsmen in batsmens:
                            name=batsmen['name']
                            runs=batsmen['runs']
                            balls=batsmen['balls']
                            fours=batsmen['fours']
                            six=batsmen['six']
                            dismissal=batsmen['dismissal']
                            sr=batsmen['sr']
                            print ("{:<20} {:<30} {:<5} {:<5} {:<2} {:<2} {:<5}".format(name,dismissal,runs, balls, fours,six,sr))
                        print('-'*100)
                        print ("{:<20} {:<5} {:<5} {:<5} {:<5} {:<5}".format("Bowler", "O", "M", "R","W","ER"))
                        bowlers=inning['bowlcard']
                        for bowl in bowlers:
                            bowler=bowl['name']
                            overs=bowl['overs']
                            maidens=bowl['maidens']
                            runs=bowl['runs']
                            wickets=bowl['wickets']
                            balls=str((math.floor(float(overs))*6+math.floor((float(overs)-math.floor(float(overs)))*10))/6)
                            if balls==0:
                                er='0'
                            else:
                                er=str(round(int(runs)/float(balls),2))
                            print ("{:<20} {:<5} {:<5} {:<5} {:<5} {:<5}".format(bowler,overs,maidens,runs,wickets,er))
                        # print('-'*100)
                        # extras=inning['extras']
                        # total=extras['total']
                        # byes=extras['byes']
                        # lbyes=extras['lbyes']
                        # wides=extras['wides']
                        # nballs=extras['nballs']
                        # penalty=extras['penalty']
                        # print ("{:<30} {:<2} {:<2} {:<2} {:<2} {:<2} {:<2}".format("Extras",total," b "+byes,"lb "+lbyes,"w "+wides,"nb "+nballs,"p "+penalty))
                        # print('-'*100)
                        print ("{:<30} {:<20} {:<10} ".format("Fall of Wickets", "Score", "Over"))
                        fall_wickets=inning['fall_wickets']
                        for fall_wicket in fall_wickets:
                            name=fall_wicket['name']
                            wicket=fall_wicket['wkt_num']
                            score=fall_wicket['score']
                            overs=fall_wicket['overs']
                            score=score+'-'+wicket
                            print ("{:<30} {:<20} {:<10} ".format(name,score,overs))
                        print('inning number:inning scorecard,b:back,r:refresh,q:quit')
                        chh=input()
                        if chh=='b':
                            break
                        elif chh=='r':
                            continue
                        elif chh=='q':
                            os.system( 'clear' )
                            exit()
                        else:
                            try:
                                inning=scorecard[int(chh)-1]
                            except:
                                print("wrong innings")
                            continue


if __name__=="__main__":
    cricpy()