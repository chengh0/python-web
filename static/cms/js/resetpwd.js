/**
 * Created by hynev on 2017/11/25.
 */

$(function () {
    $("#submit").click(function (event) {
        // event.preventDefault
        // 是阻止按钮默认的提交表单的事件
        event.preventDefault();

        var oldpwdE = $("input[name=oldpwd]");
        var newpwdE = $("input[name=newpwd]");
        var newpwd1E = $("input[name=newpwd1]");

        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd1 = newpwd1E.val();

        // 1. 要在模版的meta标签中渲染一个csrf-token
        // 2. 在ajax请求的头部中设置X-CSRFtoken
        zlajax.post({
            'url': '/cms/resetpwd/',
            'data': {
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'newpwd1': newpwd1
            },
            'success': function (data) {
                if (data['code']==200){
                    zlalert.alertSuccessToast("恭喜！,密码修改成功")
                    oldpwdE.val("")
                    newpwdE.val("")
                    newpwd1E.val("")
                }else{
                    var message = data['message'];
                    zlalert.alertInfo(message);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });
    });
});