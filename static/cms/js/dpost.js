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
                        'banner_id':post_id
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
