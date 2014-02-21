@modal_select = (app_id) ->
    $.ajax {
        "type":"get",
        "contentType":"application/json",
        "url":"/api/app/get_app_by_app_id?app_id=" + app_id,
        "success": (data) ->
            data = eval("(" + data + ")")
            data_detail = data['app_detail']
            data_detail.reverse()
            input_data = ""
            $.each data_detail, (index,detail) ->
                head = "<h1><b>" + detail['platform'] + " | " + detail['version'] + "</b></h1>"
                body = ""
                body += "<div style='float: right;'><img src='" + detail['cover'] + "' style='max-width: 100px;'/></div>"
                body += "<div><ul>"
                body += "<li><b>文件大小：</b>" + detail['apk_size'] + "</li>" if detail['apk_size']
                body += "<li><b>评分：</b>" + detail['rating_point'] + "分</li>" if detail['rating_point']
                body += "<li><b>评论数：</b>" + detail['rating_count'] + "</li>" if detail['rating_count']
                body += "<li><b>支持Android版本：</b>" + detail['android_version'] + "</li>" if detail['android_version']
                body += "<li><b>下载量：</b>" + detail['download_times'] + "</li>" if detail['download_times']
                body += "<li><b>最后更新日期：</b>" + detail['last_update'] + "</li>" if detail['last_update']
                body += "<li><b><a href='" + detail['apk_url'] + "'>Apk下载</a></b></li>" if detail['apk_url']
                body += "</ul></div>"
                body += "<p>" + detail['description'] + "</p>"
                imgs_url = detail['imgs_url'].split(" ")
                # imgs = ""
                # $.each imgs_url, (index,img_url) ->
                #     imgs += "<img src='" + img_url.replace(/https/,"http") + "' style='max-width: 230px;' />"
                imgs = "<div class='spacer'></div><div style='max-width: 800px;padding-left: 20%;padding-right: 20%;'><div id='img-slide#{index}' class='carousel slide' data-ride='carousel'><ol class='carousel-indicators'>"
                $.each imgs_url, (img_index) ->
                    if img_index is 0
                        imgs += "<li data-target='#img-slide#{index}' data-slide-to='0' class='active'></li>"
                    else
                        imgs += "<li data-target='#img-slide#{index}' data-slide-to='#{img_index}'></li>"
                imgs += "</ol><div class='carousel-inner'>"
                $.each imgs_url, (img_index, img_url) ->
                    if img_index  is 0
                        imgs += "<div class='item active' style='padding-left: 30%;padding-bottom: 20px;'><img src='#{img_url}''></div>"
                    else
                        imgs += "<div class='item' style='padding-left: 30%;padding-bottom: 20px;'><img src='#{img_url}'></div>"
                imgs += "</div><a class='left carousel-control' href='#img-slide#{index}' data-slide='prev'><span class='glyphicon glyphicon-chevron-left'></span></a><a class='right carousel-control' href='#img-slide#{index}' data-slide='next'><span class='glyphicon glyphicon-chevron-right'></span></a></div></div><div class='spacer'></div>"

                body += imgs
                if index == 0
                    input_data += "<div style='padding-bottom: 30px;'>" + head + body + "</div>"
                else
                    input_data += "<div style='border-top: 1px solid #e5e5e5; padding-bottom: 30px;'>" + head + body + "</div>"
            $('#modal_app_name').html data['app_name']
            $("#modal_app_body").html input_data
            return
    }

###
个性化          1000
交通运输        1100
体育            1200
健康与健身      1300
动态壁纸        1400
动漫            1500
医药            1600
商务            1700
图书与工具书    1800
天气            1900
娱乐            2000
媒体与视频      2100
小部件          2200
工具            2300
摄影            2400
效率            2500
教育            2600
新闻杂志        2700
旅游与本地出行  2800
生活时尚        2900
社交            3000
财务            3100
购物            3200
软件与演示      3300    
通讯            3400
音乐与音频      3500
游戏            3600
其他            3700
###

@category_dropdown = '''
    <li><a onclick="update_category(this)">个性化</a></li>
    <li><a onclick="update_category(this)">交通运输</a></li>
    <li><a onclick="update_category(this)">体育</a></li>
    <li><a onclick="update_category(this)">健康与健身</a></li>
    <li><a onclick="update_category(this)">动态壁纸</a></li>
    <li><a onclick="update_category(this)">动漫</a></li>
    <li><a onclick="update_category(this)">医药</a></li>
    <li><a onclick="update_category(this)">商务</a></li>
    <li><a onclick="update_category(this)">图书与工具书</a></li>
    <li><a onclick="update_category(this)">天气</a></li>
    <li><a onclick="update_category(this)">娱乐</a></li>
    <li><a onclick="update_category(this)">媒体与视频</a></li>
    <li><a onclick="update_category(this)">小部件</a></li>
    <li><a onclick="update_category(this)">工具</a></li>
    <li><a onclick="update_category(this)">摄影</a></li>
    <li><a onclick="update_category(this)">效率</a></li>
    <li><a onclick="update_category(this)">教育</a></li>
    <li><a onclick="update_category(this)">新闻杂志</a></li>
    <li><a onclick="update_category(this)">旅游与本地出行</a></li>
    <li><a onclick="update_category(this)">生活时尚</a></li>
    <li><a onclick="update_category(this)">社交</a></li>
    <li><a onclick="update_category(this)">财务</a></li>
    <li><a onclick="update_category(this)">购物</a></li>
    <li><a onclick="update_category(this)">软件与演示</a></li>
    <li><a onclick="update_category(this)">通讯</a></li>
    <li><a onclick="update_category(this)">音乐与音频</a></li>
    <li><a onclick="update_category(this)">游戏</a></li>
    <li><a onclick="update_category(this)">其他</a></li>
'''

@update_category = (self) ->
    console.log $(self).html()
    console.log $(self).parent().parent().attr('app_id')
    category_name = $(self).html()
    app_id = $(self).parent().parent().attr('app_id')

    $.ajax {
        "type":"get",
        "url":"/api/app/update_category/#{app_id}/#{category_name}",
        "success": (data) ->
            $(self).parent().parent().siblings("button").html("#{category_name}<span class='caret'></span>")
    }
    # console.log $(self).parentsUntil('ul .dropdown-menu').html()

# $ ->
#     $('#example').dataTable {
#         "bProcessing": true,
#         "bServerSide": true,
#         "bJQueryUI": true,
#         "sAjaxSource": "/api/app/get_app_list",
#         "fnServerData": (sSource, aoData, fnCallback) ->
#             $.ajax {
#                 "type": "get",
#                 "contentType": "application/json",
#                 "url": sSource,
#                 "dataType": "json",
#                 "data": {aoData: JSON.stringify aoData},
#                 "success": (resp) ->
#                     fnCallback resp
#                     return
#             }
#             return
#     }
#     return

# $ ->
#     $('#app_list').dataTable {
#         "bProcessing": true
#     }
#     $.ajax {
#         "type":"get",
#         "contentType":"application/json",
#         "url":"/api/app/app_list/1",
#         "success": (data) ->
#             $("#app_list").dataTable().fnAddData eval("(" + data + ")")['aaData']
#             i = 2
#             load_job = setInterval ->
#                 $.ajax {
#                     "type":"get",
#                     "contentType":"application/json",
#                     "url":"/api/app/app_list/" + i,
#                     "success": (new_data) ->
#                         $("#app_list").dataTable().fnAddData eval("(" + new_data + ")")['aaData']
#                         i += 1
#                         clearInterval load_job if i > 100
#                         return
#                 }
#                 return
#             , 1000
#     }
#     return
