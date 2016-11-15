
$(document).ready(function() {
        // JQuery code to be added in here.
        $("#about-btn").click(function(event) {
          this.html("test");
          alert ("You clicked with Jquery ");
    )
        });

        $("#likesbutton").click(function(){
            var totallikes = this.attr("totallikes");
            $("#likesheading").html("test");
            $.get("/rango/", { "wholelikes" : totallikes }, function(data) {

              $("#likesheading").html(data)

            });

       });
});
