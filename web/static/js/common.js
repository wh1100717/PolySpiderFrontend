// Generated by CoffeeScript 1.7.1

/*
Common.js
Author: Eric Wang
https://github.com/wh1100717
 */
$(function() {

  /*
  	dynamically activate the navi tab
   */
  var active_class;
  active_class = location.href.split("/")[3];
  if (!active_class) {
    active_class = "home";
  }
  return $("#navi_" + active_class).addClass("active");
});


/*
$ ->
	crawled_number = $('#crawled_number')
	old_n = parseInt crawled_number.html()
	count = 30
	new_n = 0
	$.changeNum = (o_n, n_n) ->
		crawled_number.html(Math.round((n_n - o_n)*count/30) + o_n) if new_n isnt 0
		if count is 30
			$.ajax(
				url: "/api/app/get_app_count",
				success: (data)->
					data = eval(data)[0]
					new_n = parseInt data['count']
					old_n = parseInt crawled_number.html()
					old_n = Math.round(0.5 * new_n) if old_n is 0
					count = 1
					return
			)
		else
			count += 1
		return
	setInterval((-> $.changeNum(old_n, new_n)), 200)
	return
 */

$(function() {
  var crawled_number, timer;
  crawled_number = $('#crawled_number');
  timer = null;
  $.changeNum = function() {
    $.ajax({
      url: "/api/app/get_app_count",
      success: function(data) {
        var count, new_n, old_n;
        data = eval(data)[0];
        new_n = parseInt(data['count']);
        old_n = crawled_number.html();
        if (old_n === "") {
          $('#crawled_number_span').fadeIn();
          old_n = Math.max(Math.round(new_n * 0.9), new_n - 300);
        } else {
          old_n = parseInt(old_n);
        }
        count = 1;
        return timer = setInterval((function() {
          crawled_number.html(old_n + count);
          count += 1;
        }), Math.round(6000 / (new_n - old_n)));
      }
    });
  };
  setInterval((function() {
    clearInterval(timer);
    $.changeNum();
  }), 6000);
});
