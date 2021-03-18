import json
from django.shortcuts import render
from django.middleware import csrf
from django.http import QueryDict, HttpResponse
from curlingapp.models import Round, Scoreboard


def match(request,match):
    print("index")
    context = {}
    pos = Round.objects.latest('timestamp').get_pos()
    print("pos",pos)
    context['positions'] = pos
    ends = Scoreboard.objects.filter(match=match)
    
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

def send_pos(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        print(type(data))
        pos = data['pos']



        points = data['points']

        if points != None:
            winner = points["winner"]
            score = points["score"]
            s = Scoreboard(end=1,match="TestMatch",winner=winner,points=score)
            s.save()


        r = Round(pos=pos,end=1,throw=4,match="Test Match")
        r.save()
        #print("pos",pos)
        #print("points",points)

    elif request.method == "GET":
        csrf.get_token(request)
        return HttpResponse("")
