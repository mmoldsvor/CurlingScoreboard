import json
from django.shortcuts import render
from django.middleware import csrf
from django.http import QueryDict, HttpResponse
from curlingapp.models import Round, Scoreboard

#pos = '{"center": {"x": "960.5", "y": "591.5", "rad": "485.1"}, "red": [{"x": "-56.0", "y": "-200.0", "rad": "37.1628", "color": "red"}], "yellow": [{"x": "55.0", "y": "-92.0", "rad": "38.0952", "color": "yellow"}, {"x": "-261.0", "y": "-369.0", "rad": "38.3616", "color": "yellow"}]}'

# Create your views here.
def index(request):
    print("index")
    context = {}
    pos = Round.objects.latest('timestamp').get_pos()
    print("pos",pos)
    context['positions'] = pos
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
