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

$ ->
    $('#app_list').dataTable {
        "bProcessing": true
    }
    $.ajax {
        "type":"get",
        "contentType":"application/json",
        "url":"/api/app/app_list/1",
        "success": (data) ->
            $("#app_list").dataTable().fnAddData eval("(" + data + ")")['aaData']
            i = 2
            load_job = setInterval ->
                $.ajax {
                    "type":"get",
                    "contentType":"application/json",
                    "url":"/api/app/app_list/" + i,
                    "success": (new_data) ->
                        $("#app_list").dataTable().fnAddData eval("(" + new_data + ")")['aaData']
                        i += 1
                        clearInterval load_job if i > 100
                        return
                }
                return
            , 1000
    }

    return
