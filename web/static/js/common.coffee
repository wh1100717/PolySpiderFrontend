###
Common.js
Author: Eric Wang
https://github.com/wh1100717
###
$ ->
	###
	dynamically activate the navi tab
	###
	active_class = location.href.split("/")[3]
	active_class = "home" if not active_class
	$("#navi_" + active_class).addClass("active")
###
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
###
$ ->
	crawled_number = $('#crawled_number')
	timer = null
	changeNum = ->
		$.ajax(
			url: "/api/app/get_app_count",
			success: (data) ->
				data = eval(data)[0]
				new_n = parseInt data['count']
				old_n = crawled_number.html()
				if old_n is ""
					$('#crawled_number_span').fadeIn()
					old_n = Math.max Math.round(new_n*0.9),(new_n-300)
				else
					old_n = parseInt old_n
				count = 1
				time_interval = new_n - old_n
				if time_interval > 0
					timer = setInterval(
						(-> 
							crawled_number.html(old_n + count)
							count += 1
							return),
						(Math.round 6000 /(time_interval)))
				return
			)
		return
	changeNum()
	setInterval((-> 
		clearInterval timer
		changeNum()
		return), 6000)
	return

