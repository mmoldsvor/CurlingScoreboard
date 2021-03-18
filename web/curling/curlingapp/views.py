import json
from django.shortcuts import render
from django.middleware import csrf
from django.http import QueryDict, HttpResponse
from curlingapp.models import Round, Scoreboard, Match


def match(request,match):
    context = {}
    matchid = Match.objects.get(match=match)
    print(matchid)
    pos = Round.objects.filter(match=matchid).latest('timestamp').get_pos()
    context['positions'] = pos
    ends = Scoreboard.objects.filter(match=matchid)
    
    yellow = [0]*10
    red = [0]*10

    for e in ends:
        end, team, score = e.get_score()
        if team == "yellow":
            yellow[end-1] = score
        elif team == "red":
            red[end-1] = score
    
    context['totalRed'] = sum(red)
    context['totalYellow'] = sum(yellow)

    context['red'] = red
    context['yellow'] = yellow

    return render(request, "curlingapp/index.html",context)

def send_pos(request,camId):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        print(type(data))
        pos = data['pos']

        points = data['points']

        matchid = Match.objects.filter(camId=camId).last()
        print(matchid)

        if points != None:
            winner = points["winner"]
            score = points["score"]
            s = Scoreboard(end=1,match=matchid,winner=winner,points=score)
            s.save()

        r = Round(pos=pos,end=1,throw=4,match=matchid)
        r.save()




        #print("pos",pos)
        #print("points",points)

    elif request.method == "GET":
        csrf.get_token(request)
        return HttpResponse("")
