$(function () {
    $('#save-banner-btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $('#banner-dialog');
        var nameInput = $("input[name='name']");
        var imageInput = $("input[name='image_url']");
        var linkInput = $("input[name='link_url']");
        var priorityInput = $("input[name='priority']");

        var name = nameInput.val();
        var image_url = imageInput.val();
        var link_url = linkInput.val();
        var priority = priorityInput.val();
        var submitType = self.attr("data-type");
        var bannerId = self.attr('data-id')

        var url = ''
        if (submitType == 'update'){
            url = '/cms/ubanner/';
        }else{
            url = '/cms/addbanner/';
        }

        if(!name || !image_url || !link_url || !priority){
            zlalert.alertInfo('请输入完整的轮播图数据！');
            return;
        };

        zlajax.post({
            'url':url,
            'data':{
                'name':name,
                'image_url':image_url,
                'link_url':link_url,
                'priority':priority,
                'banner_id':bannerId
            },
            'success':function (data) {
                dialog.modal('hide');
                if(data['code']==200){
                    window.location.reload()
                }else{
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail':function () {
                zlalert.alertNetworkError();
            }
        })
    })
})


$(function () {
    $(".edit-banner-btn").click(function (event) {
        var self = $(this);
        var dialog = $('#banner-dialog');
        dialog.modal('show');

        var tr = self.parent().parent();
        var name = tr.attr("data-name");
        var image_url = tr.attr("data-image");
        var link_url = tr.attr("data-link");
        var priority = tr.attr("data-priority");


        var nameInput = dialog.find("input[name='name']");
        var imageInput = dialog.find("input[name='image_url']");
        var linkInput = dialog.find("input[name='link_url']");
        var priorityInput = dialog.find("input[name='priority']");
        var savebtn = dialog.find("#save-banner-btn");

        nameInput.val(name);
        imageInput.val(image_url);
        linkInput.val(link_url);
        priorityInput.val(priority);
        savebtn.attr("data-type",'update');
        savebtn.attr("data-id",tr.attr('data-id'));
    })
})


$(function () {
    $('.delete-banner-btn').click(function (event) {
        var self = $(this)
        var tr = self.parent().parent();
        var banner_id = tr.attr('data-id');
        zlalert.alertConfirm({
            'msg':'您确定要删除这个轮播图吗？',
            'confirmCallback':function () {
                zlajax.post({
                    'url':'/cms/dbanner/',
                    'data':{
                        'banner_id':banner_id
                    },
                    'success':function (data) {
                        if(data['code']==200){
                            window.location.reload()
                        }else{
                            zlalert.alertError(data['message'])
                        }
                    }
                })
            }
        })
    })
})

