<!--这里是搜索的scripts-->
function doSearch(e) {
    if (e != null && e.keyCode !== 13) {
        return false;
    }
    //# 代表id， .代表class
    var keyword = $.trim($("#search").val());
    console.log(keyword)
    if (keyword.length === 0 || keyword.length > 10 || keyword.indexOf('%') >= 0) {

        alert('输入的搜索关键字不符合要求');
        $("#search");
        return false;
    }
    location.href = '/search_list/1-' + keyword;
    window.event.returnValue = false
}

//    //这里是登录的scripts
function doLogin(e) {
    if (e != null && e.keyCode != 13) {
        return false;
    }

    var loginname = $.trim($("#loginname").val());
    var loginpass = $.trim($("#loginpass").val());
    var logincode = $.trim($("#logincode").val());

    if (loginname.length < 5 || loginpass.length < 5) {
        alert("用户名和密码少于5位.");
        return false;
    } else {
        // 构建POST请求的正文数据
        var param = "username=" + loginname;
        param += "&password=" + loginpass;
        param += "&vcode=" + logincode;
        // 利用jQuery框架发送POST请求，并获取到后台登录接口的响应内容
        $.post('/login', param, function (data) {
            if (data == "vcode-error") {
                alert("验证码无效.");
                $("#logincode").val('');  // 清除验证码框的值
                $("#logincode").focus();   // 让验证码框获取到焦点供用户输入
            } else if (data == "login-pass") {
                alert("恭喜你，登录成功.");
                // 注册成功后，延迟1秒钟重新刷新当前页面即可
                setTimeout('location.reload();', 1000);

            } else if (data == "login-fail") {
                alert("登录失败，请联系管理员.");
            }
        });
    }
}
