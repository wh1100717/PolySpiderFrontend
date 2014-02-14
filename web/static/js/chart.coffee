$ ->
    #分类数据饼状图Ajax初始化
    $.getJSON '/api/app/category_statistic', (data) ->
        $('#container-category').highcharts {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title:{text:'分类应用数据分析'},
            subtitle:{text:'PolySpider爬取应用所属分类饼状图'},
            tooltip:{pointFormat: '{series.name.percent}: <b>{point.percentage:.1f}%</b><br>{series.name.count}: <b>{point.y}</b><br>'},
            plotOptions:{
                pie:{
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        color: '#000000',
                        connectorColor: '#000000',
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                    },
                    showInLegend: true
                }
            },
            series:[
                {
                    type: 'pie',
                    name: {'percent': '百分比', 'count': '应用数'},
                    data: data
                }
            ]
        }
        return
    #平台数据饼状图Ajax初始化
    $.getJSON '/api/app/platform_statistic', (data) ->
        $('#container-platform').highcharts {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: '平台应用数据分析'
            },
            subtitle: {
                text: 'PolySpider爬取应用所属平台饼状图(忽略版本)'
            },
            tooltip: {
                pointFormat: '{series.name.percent}: <b>{point.percentage:.1f}%</b><br>{series.name.count}: <b>{point.y}</b><br>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        color: '#000000',
                        connectorColor: '#000000',
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                    },
                    showInLegend: true
                }
            },
            series: [
                {
                    type: 'pie',
                    name: {'percent': '百分比', 'count': '应用数'},
                    data: data                    
                }
            ]
        }
        return
    return