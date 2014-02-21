$ ->
	seriesOptions = []
	$.getJSON '/api/status/status_history', (data) ->
		xiaomi_crawled_data = []
		xiaomi_new_data = []
		xiaomi_update_data = []
		baidu_crawled_data = []
		baidu_new_data = []
		baidu_update_data = []
		hiapk_crawled_data = []
		hiapk_new_data = []
		hiapk_update_data = []
		appchina_crawled_data = []
		appchina_new_data = []
		appchina_update_data = []
		googleplay_crawled_data = []
		googleplay_new_data = []
		googleplay_update_data = []
		muzhiwan_crawled_data = []
		muzhiwan_new_data = []
		muzhiwan_update_data = []
		$.each data, (date, item) ->
			date = date.split('-')
			date = Date.UTC(parseInt(date[0]), parseInt(date[1])-1, parseInt(date[2]))
			item = eval('(' + item + ')')
			$.each item, (platform, platform_data) ->
				switch platform
					when 'xiaomi'
						xiaomi_crawled_data.push [date, parseInt platform_data.crawled] if platform_data.crawled
						xiaomi_new_data.push [date, parseInt platform_data.new] if platform_data.new
						xiaomi_update_data.push [date, parseInt platform_data.update] if platform_data.update
					when 'baiduapp'
						baidu_crawled_data.push [date, parseInt platform_data.crawled] if platform_data.crawled
						baidu_new_data.push [date, parseInt platform_data.new] if platform_data.new
						baidu_update_data.push [date, parseInt platform_data.update] if platform_data.update
					when 'hiapk'
						hiapk_crawled_data.push [date, parseInt platform_data.crawled] if platform_data.crawled
						hiapk_new_data.push [date, parseInt platform_data.new] if platform_data.new
						hiapk_update_data.push [date, parseInt platform_data.update] if platform_data.update
					when 'appchina'
						appchina_crawled_data.push [date, parseInt platform_data.crawled] if platform_data.crawled
						appchina_new_data.push [date, parseInt platform_data.new] if platform_data.new
						appchina_update_data.push [date, parseInt platform_data.update] if platform_data.update
					when 'googleplay'
						googleplay_crawled_data.push [date, parseInt platform_data.crawled] if platform_data.crawled
						googleplay_new_data.push [date, parseInt platform_data.new] if platform_data.new
						googleplay_update_data.push [date, parseInt platform_data.update] if platform_data.update
					when 'muzhiwan'
						muzhiwan_crawled_data.push [date, parseInt platform_data.crawled] if platform_data.crawled
						muzhiwan_new_data.push [date, parseInt platform_data.new] if platform_data.new
						muzhiwan_update_data.push [date, parseInt platform_data.update] if platform_data.update
				return
			return
		seriesOptions[0] = {name: 'xiaomi_crawled_data', data: xiaomi_crawled_data.sort (x,y) -> x[0]-y[0]}
		seriesOptions[1] = {name: 'xiaomi_new_data', data: xiaomi_new_data.sort (x,y) -> x[0]-y[0]}
		seriesOptions[2] = {name: 'xiaomi_update_data', data: xiaomi_update_data.sort (x,y) -> x[0]-y[0]}
		seriesOptions[3] = {name: 'baidu_crawled_data', data: baidu_crawled_data.sort (x,y) -> x[0]-y[0]}
		seriesOptions[4] = {name: 'baidu_new_data', data: baidu_new_data.sort (x,y) -> x[0]-y[0]}
		seriesOptions[5] = {name: 'baidu_update_data', data: baidu_update_data.sort (x,y) -> x[0]-y[0]}
		seriesOptions[6] = {name: 'hiapk_crawled_data', data: hiapk_crawled_data.sort (x,y) -> x[0]-y[0]}
		seriesOptions[7] = {name: 'hiapk_new_data', data: hiapk_new_data.sort (x,y) -> x[0]-y[0]}
		seriesOptions[8] = {name: 'hiapk_update_data', data: hiapk_update_data.sort (x,y) -> x[0]-y[0]}
		seriesOptions[9] = {name: 'appchina_crawled_data', data: appchina_crawled_data.sort (x,y) -> x[0]-y[0]}
		seriesOptions[10] = {name: 'appchina_new_data', data: appchina_new_data.sort (x,y) -> x[0]-y[0]}
		seriesOptions[11] = {name: 'appchina_update_data', data: appchina_update_data.sort (x,y) -> x[0]-y[0]}
		seriesOptions[12] = {name: 'googleplay_crawled_data', data: googleplay_crawled_data.sort (x,y) -> x[0]-y[0]}
		seriesOptions[13] = {name: 'googleplay_new_data', data: googleplay_new_data.sort (x,y) -> x[0]-y[0]}
		seriesOptions[14] = {name: 'googleplay_update_data', data: googleplay_update_data.sort (x,y) -> x[0]-y[0]}
		seriesOptions[15] = {name: 'muzhiwan_crawled_data', data: muzhiwan_crawled_data.sort (x,y) -> x[0]-y[0]}
		seriesOptions[16] = {name: 'muzhiwan_new_data', data: muzhiwan_new_data.sort (x,y) -> x[0]-y[0]}
		seriesOptions[17] = {name: 'muzhiwan_update_data', data: muzhiwan_update_data.sort (x,y) -> x[0]-y[0]}
		$('#container-status-list').highcharts 'StockChart',{
			chart: {},
			rangeSelector: {selected:1},
			title: {text:'爬虫数据分析'},
			legend: {enabled:true},
			tooltip:{
				pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>',
				valueDecimals: 2
			}
			series: seriesOptions
		}
		status_list_chart = $('#container-status-list').highcharts()
		status_list_chart.series[1].hide()
		status_list_chart.series[2].hide()
		status_list_chart.series[4].hide()
		status_list_chart.series[5].hide()
		status_list_chart.series[7].hide()
		status_list_chart.series[8].hide()
		status_list_chart.series[10].hide()
		status_list_chart.series[11].hide()
		status_list_chart.series[13].hide()
		status_list_chart.series[14].hide()
		status_list_chart.series[16].hide()
		status_list_chart.series[17].hide()
		return
	return

$ ->
	initData = ->
		data = []
		time = (new Date()).getTime()
		data.push {x: time + i*1000, y: 0} for i in [-19..0]
		return data
	Highcharts.setOptions({global:{useUTC:false}})
	$('#container-status-realtime').highcharts {
		chart:{
			type: 'spline',
			animation: Highcharts.svg,
			marginRight: 10,
			events:{
				load: ->
					series = @series
					setInterval ()-> 
						x = (new Date()).getTime()
						$.getJSON '/api/status/status_today', (data) ->
							$.each data,(platform,platform_data) ->
								switch platform
									when "xiaomi"
										series[0].addPoint [x, parseInt platform_data.crawled], true, true
										series[1].addPoint [x, parseInt platform_data.new], true, true
										series[2].addPoint [x, parseInt platform_data.update], true, true
									when "baiduapp"
										series[3].addPoint [x, parseInt platform_data.crawled], true, true
										series[4].addPoint [x, parseInt platform_data.new], true, true
										series[5].addPoint [x, parseInt platform_data.update], true, true
									when "hiapk"
										series[6].addPoint [x, parseInt platform_data.crawled], true, true
										series[7].addPoint [x, parseInt platform_data.new], true, true
										series[8].addPoint [x, parseInt platform_data.update], true, true
									when "appchina"
										series[9].addPoint [x, parseInt platform_data.crawled], true, true
										series[10].addPoint [x, parseInt platform_data.new], true, true
										series[11].addPoint [x, parseInt platform_data.update], true, true
									when "googleplay"
										series[12].addPoint [x, parseInt platform_data.crawled], true, true
										series[13].addPoint [x, parseInt platform_data.new], true, true
										series[14].addPoint [x, parseInt platform_data.update], true, true
									when "muzhiwan"
										series[15].addPoint [x, parseInt platform_data.crawled], true, true
										series[16].addPoint [x, parseInt platform_data.new], true, true
										series[17].addPoint [x, parseInt platform_data.update], true, true
								return
							return
						return
					,5000
					return
			},
		}
		title: {text: '实时数据分析'},
		xAxis: {type: 'datetime', tickPixelInterval: 150},
		yAxis: {
			title: {
				text: 'Value'
			},
			plotLines: [{
				color: '#808080'
			}]
		},
		tooltip: {
			formatter: -> '<b>' + this.series.name + '</b><br/>' + Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' + Highcharts.numberFormat(this.y, 0);
		},
		legend: {enabled: true},
		exporting: {enabled: false},
		series: [
			{name: 'xiaomi_crawled_data', data: initData()},
			{name: 'xiaomi_new_data', data: initData()},
			{name: 'xiaomi_update_data', data: initData()},
			{name: 'baidu_crawled_data', data: initData()},
			{name: 'baidu_new_data', data: initData()},
			{name: 'baidu_update_data', data: initData()},
			{name: 'hiapk_crawled_data', data: initData()},
			{name: 'hiapk_new_data', data: initData()},
			{name: 'hiapk_update_data', data: initData()},
			{name: 'appchina_crawled_data', data: initData()},
			{name: 'appchina_new_data', data: initData()},
			{name: 'appchina_update_data', data: initData()},
			{name: 'googleplay_crawled_data', data: initData()},
			{name: 'googleplay_new_data', data: initData()},
			{name: 'googleplay_update_data', data: initData()}
			{name: 'muzhiwan_crawled_data', data: initData()},
			{name: 'muzhiwan_new_data', data: initData()},
			{name: 'muzhiwan_update_data', data: initData()}
		]
	}
	status_chart = $('#container-status-realtime').highcharts();
	status_chart.series[1].hide()
	status_chart.series[2].hide()
	status_chart.series[4].hide()
	status_chart.series[5].hide()
	status_chart.series[7].hide()
	status_chart.series[8].hide()
	status_chart.series[10].hide()
	status_chart.series[11].hide()
	status_chart.series[13].hide()
	status_chart.series[14].hide()
	status_chart.series[16].hide()
	status_chart.series[17].hide()
	return
