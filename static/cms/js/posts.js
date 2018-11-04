/**
 * Created by hynev on 2018/1/4.
 */

$(function () {
    $(".highlight-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr("data-id");
        var highlight = parseInt(tr.attr("data-highlight"));
        var url = "";
        if(highlight){
            url = "/cms/uepost/";
        }else{
            url = "/cms/epost/";
        }
        zlajax.post({
            'url': url,
            'data': {
                'post_id': post_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    zlalert.alertSuccessToast('操作成功！');
                    setTimeout(function () {
                        window.location.reload();
                    },500);
                }else{
                    zlalert.alertInfo(data['message']);
                }
            }
        });
    });
});

$(function () {
    $('.delete-post-btn').click(function (event) {
        var self = $(this)
        var tr = self.parent().parent();
        var post_id = tr.attr('data-id');
        zlalert.alertConfirm({
            'msg':'您确定要删除这篇帖子吗？',
            'confirmCallback':function () {
                zlajax.post({
                    'url':'/cms/dpost/',
                    'data':{
                        'post_id':post_id
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