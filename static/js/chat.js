
/******** slider **********/

$(document).ready(function(){
	$('.bxslider').bxSlider();
});

/********* web soket *******/

var webSocket;
var name="Anonymous";
// var x= document.getElementById("group");
var selected;
var list ;
function getParameterByName(name) {
    var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}
$(document).ready(function(){
	webSocket= new WebSocket("ws://localhost:8888/ws?g='"+window.getParameterByName("g")+"'");
	console.log(window.getParameterByName("g"));
	webSocket.onopen =function (e) {
		console.log("Connection");

	}
	webSocket.onmessage = function(e){
		console.log(e.data);
		$("#chat-body").append("<p>"+e.data+"</p>");
	}
	webSocket.onclose = function(e){
		console.log(e);
		$("#chat-body").append("<p>"+"Connection Lost !!!!"+"</p>");
	}

	$('#send').click(function(e){
		name = $(".name").val();
		console.log(name);
		var x = document.getElementById("group").selectedIndex;
    var y = document.getElementById("group").options;
    // alert("Index: " + y[x].index + " is " + y[x].text);
		var msg = name +":"+(x-1).toString() +": "+ $("#message").val();
		console.log(msg);
		webSocket.send(msg);
		$("#message").val('');
	})

var lastModified = 0;
function doLongPolling(){
    $.ajax({
        method: 'get',
        url: 'http://localhost:8888/myapi',
        data: {lastmod: lastModified},
        success: function(res){
            lastModified = res.lastmod? res.lastmod:0;
            $("select.groupmates option").each(function(){$(this).remove()});
						$("ul.groupmates li").each(function(){$(this).remove()});

            rslt=res.body.split("\n");
            rslt.splice(rslt.length-1,1)
            $.each(rslt,function (i) {
                    $("#group").append("<option value='"+rslt[i]+"'>"+rslt[i]+"</option>")// <img class='onimg' src='"+{{ static_url("img/onlineimg.png")}}+"' alt=""><img class='img-circle_on' src='"+{{ static_url(+"img/pic.jpg"+)}}+
					if (rslt[i]!="all") {
							$("select.groupmates").append("<li value='"+rslt[i]+"'>"+rslt[i]+"</li>")
					}
            });

            console.log(res);
            doLongPolling()
        }
    })
};
doLongPolling();
})
