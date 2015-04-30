$( document ).ready(function() {
    var get_flair = function(subreddit_name) {
        return $.ajax("/_get_flair/" + subreddit_name);
    };

    var get_my_subreddits = function(subreddit_name) {
        return $.ajax("/_get_my_subreddits");
    };
    
    var update_rows_visibility = function() {
        if($("#hide-empty-flairs").is(":checked")) {
            $(".empty-flair").hide();
        } else {
            $(".empty-flair").show();
        }
    };

    console.log( "ready!" );
    get_my_subreddits().done(function(data){
        if (data.login_again) {
            $('#login-again-btn').show();
            return;
        }
        subreddits = data.subreddits;
        subreddits_num = subreddits.length;
        $("#flair-progressbar").removeClass("progress-bar-info");
        update_progress();
        get_all_flairs();
    }).fail(function() {
        setTimeout(get_my_subreddits, 3000);
    });

    var update_progress = function() {
        processed_subreddits = subreddits_num - subreddits.length;
        completed_percentage = processed_subreddits / subreddits_num * 100;
        $("#flair-progressbar")
            .attr('aria-valuenow', completed_percentage)
            .width(completed_percentage + "%")
            .html(processed_subreddits + " / " + subreddits_num);
        window.document.title = "myflair: " + processed_subreddits + " / " + subreddits_num;
    };

    var get_all_flairs = function() {
        get_flair(subreddits[0]).done(function(data) {
            if (data.login_again) {
                $('#login-again-btn').removeClass("hidden");
                return;
            }
            subreddit = data.subreddit;
            flair = data.flair;
            tr_class = flair ? "nonempty-flair" : "empty-flair";
            $("#myflair-table").append("<tr class=" + tr_class + "><td>" + subreddit + "</td><td>" + (flair || "[no flair]") + "</td></tr>");
            update_rows_visibility();
            subreddits.shift();
            update_progress();

            if (subreddits.length) {
                get_all_flairs();
            } else {
                $("#flair-progressbar").addClass("progress-bar-success");
                $("#flair-progressbar").removeClass("active");
            }
        }).fail(function() {
            setTimeout(get_all_flairs, 3000);
        });
    };

    $('#hide-empty-flairs').change(function() {
        update_rows_visibility();
    });
});
