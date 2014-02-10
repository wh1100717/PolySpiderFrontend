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

$ ->
	###
	crawled number process
	###
	new_n = 100
	crawled_number = $('#crawled_number')
	old_n = parseInt crawled_number.html()
	count = 1
	$.changeNum = (o_n, n_n) -> 
		crawled_number.html((n_n - o_n)*count/5 + o_n)
		if count isnt 5
			count += 1
		else
			new_n = new_n + 100
			old_n = parseInt crawled_number.html()
			count = 1
		return
	setInterval((-> $.changeNum(old_n, new_n)), 100)
	return


