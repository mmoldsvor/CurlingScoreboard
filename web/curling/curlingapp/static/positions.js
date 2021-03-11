window.onload = function() {
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");

    
    var pos = JSON.parse(data);
    canvas.width = house.clientWidth;
    scale = canvas.width/1300;
    radius = pos.center.rad*scale
    canvas.height = radius*4.5;

    centerY = canvas.height-radius;
    centerX = canvas.width/2;
    console.log(scale)
    //ctx.scale(scale, scale);    
    drawHouse(centerX,centerY,radius,ctx);


    for (var key in pos.red) {
        x = centerX + parseInt(pos.red[key].x)*scale
        y = centerY + parseInt(pos.red[key].y)*scale
        drawStone(x,y, "#FF0000", ctx)
    }
    for (var key in pos.yellow) {
        x = centerX + parseInt(pos.yellow[key].x)*scale
        y = centerY + parseInt(pos.yellow[key].y)*scale
        drawStone(x,y, "#FFFF00", ctx)
    }

    //drawStone(50,50,"#FF0000",ctx);
    //drawStone(200,200,"#FFFF00",ctx);
}

function drawStone(X,Y,clr,ctx) {
    const radius = 35*scale;

    ctx.fillStyle = "#FFFFFF";
    ctx.beginPath();
    ctx.arc(X,Y,radius*1.332, 0, 2 * Math.PI, false);
    ctx.stroke();
    ctx.fill();

    ctx.fillStyle = clr;
    ctx.beginPath();
    ctx.arc(X,Y,radius, 0, 2 * Math.PI, false);
    ctx.stroke();
    ctx.fill();
}

function drawHouse(X,Y,radius,ctx){
    ctx.fillStyle = "#00FF00";
    ctx.beginPath();
    ctx.arc(X,Y,radius, 0, 2 * Math.PI, false);
    ctx.stroke();
    ctx.fill();

    ctx.fillStyle = "#FFFFFF";
    ctx.beginPath();
    ctx.arc(X,Y,radius*0.7, 0, 2 * Math.PI, false);
    ctx.stroke();
    ctx.fill();

    ctx.fillStyle = "#0000FF";
    ctx.beginPath();
    ctx.arc(X,Y,radius*0.35, 0, 2 * Math.PI, false);
    ctx.stroke();
    ctx.fill();

    ctx.fillStyle = "#FFFFFF";
    ctx.beginPath();
    ctx.arc(X,Y,radius*0.133, 0, 2 * Math.PI, false);
    ctx.stroke();
    ctx.fill();
}
