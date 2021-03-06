import json
from django.shortcuts import render
from django.middleware import csrf
from django.http import QueryDict, HttpResponse
from curlingapp.models import Round, Scoreboard, Match, MatchForm


def live(request,match):
    context = {}
    matchid = Match.objects.get(matchName=match)
    thrw = Round.objects.filter(match=matchid).latest('timestamp')
    pos = thrw.get_pos()
    context['positions'] = pos
    ends = Scoreboard.objects.filter(match=matchid)
    
    prev = Round.objects.get(pk=thrw.pk-1)

    context['match'] = matchid.matchName
    context['prev'] = prev
    context['round'] = thrw


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

    return render(request, "curlingapp/live.html",context)

def past(request,match,end,throw):
    context = {}
    matchid = Match.objects.get(matchName=match)
    thrw = Round.objects.get(match=matchid,end=end,throw=throw)
    pos = thrw.get_pos()
    #pos = Round.objects.filter(match=matchid).latest('timestamp').get_pos()
    context['positions'] = pos
    #ends = Scoreboard.objects.filter(match=matchid)

    try:
        next = Round.objects.get(pk=thrw.pk+1)
    except:
        next = None

    prev = Round.objects.get(pk=thrw.pk-1)

    context['match'] = matchid.matchName
    context['round'] = thrw
    context['next'] = next
    context['prev'] = prev
    

    return render(request, "curlingapp/past.html",context)

def matches(request):
    context = {}
    #ends = Scoreboard.objects.filter(match=matchid)
    m = Match.objects.all()

    context['matches'] = m

    # create object of form 
    form = MatchForm(request.POST or None, request.FILES or None) 
      
    # check if form data is valid 
    if form.is_valid(): 
        # save the form data to model 
        form.save() 
    
    context['form'] = form
    return render(request, "curlingapp/matches.html",context)

def send_pos(request,camId):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        print(type(data))
        pos = data['pos']
        points = data['points']


        matchid = Match.objects.filter(camId=camId).last()
        print(matchid)

        prev = Round.objects.filter(match=matchid).latest('timestamp')
        end = prev.end
        throw = prev.throw

        if throw > 16:
            end += 1
            throw = 1
        elif throw == 16:
            winner = points["winner"]
            score = points["score"]
            s = Scoreboard(end=end,match=matchid,winner=winner,points=score)
            s.save()

        r = Round(pos=pos,end=end,throw=throw,match=matchid)
        r.save()

    elif request.method == "GET":
        csrf.get_token(request)
        return HttpResponse("")
