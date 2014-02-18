@modal_select = (app_id) ->
    $.ajax {
        "type":"get",
        "contentType":"application/json",
        "url":"/api/app/get_app_by_app_id?app_id=" + app_id,
        "success": (data) ->
            data = eval("(" + data + ")")
            data_detail = data['app_detail']
            console.log data_detail
            input_data = ""
            $.each data_detail, (index,detail) ->
                head = "<h1><b>" + detail['platform'] + " | " + detail['version'] + "</b></h1>"
                body = ""
                body += "<div style='float: right;'><img src='" + detail['cover'] + "' /></div>"
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
                imgs = ""
                $.each imgs_url, (index,img_url) ->
                    imgs += "<img src='" + img_url + "' />"
                body += imgs
                if index == 0
                    input_data += "<div style='padding-bottom: 30px;'>" + head + body + "</div>"
                else
                    input_data += "<div style='border-top: 1px solid #e5e5e5; padding-bottom: 30px;'>" + head + body + "</div>"
            $('#modal_app_name').html data['app_name']
            $("#modal_app_body").html input_data
    }


        # <li><b>文件大小：</b><span id="modal_file_size"></span></li>
        # <li><b>评分：</b><span id="modal_rating_point"></span>分</li>
        # <li><b>评论数：</b><span id="modal_rating_count"></span></li>
        # <li><b>支持Android版本：</b><span id="modal_support_android"></span></li>
        # <li><b>下载量：</b><span id="modal_download_times"></span></li>
        # <li><b>最后更新日期：</b><span id="modal_last_update"></span></li>
        # <h1><b>详细介绍：</b></h1><span id="modal_description"></span><br>

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
