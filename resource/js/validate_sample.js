// 表单验证不能出现中文
export function validateChinese(rule, value, callback) {
    const regNu = /^[a-zA-Z0-9_]{0,}$/;
    if (!regNu.test(value)) {
        return callback(new Error('不能出现中文字符!'));
    } else {
        callback();
    }
}
//表单验证填写 (必须为数字)
export function validateNumber(rule, value, callback) {
    const regNu = /^[0-9]*$/;
    if (!regNu.test(value)) {
        return callback(new Error('请输入数字'));
    } else {
        callback();
    }
};
//表单验证填写（必填项不能为空）
export function validateNull(rule, value, callback) {
    if (value === "") {
       return callback(new Error('必填项不能为空！'));
    } else {
        callback();
    }
};

//表单验证填写（长度验证）
export function validateLength (rule, value, callback) {
    if (value.length >= 14 || value.length < 2) {
          return callback(new Error('长度为3位 ~ 14位！'));
    } else {
        callback();
    }
};

//表单中出现空格验证
export function validateSpace(rule, value, callback) {
    if (typeof value != 'string') {
        console.warn('表单验证接收value的类型错误');
    }
    if (value.indexOf(" ") == -1) {
        callback();
    } else {
        return callback(new Error('不能包含空格！'));
    }
};

// 表单中输入中出现特殊字符
export function validateSpecial(rule, value, callback) {
    const regEn = /[`~!@#$%^&*()_+<>?:"{},.\/;'[\]]/im;
    const regCn = /[·！#￥（——）：；“”‘、，|《。》？、【】[\]]/im;
    if (regEn.test(value) || regCn.test(value)) {
        return callback(new Error('不能包含特殊字符！'));
    } else {
        callback();
    }
};

//表单中输入手机号验证
export function validateMobile(rule, value, callback) {
    const mobile = /^[1][3,4,5,7,8,6][0-9]{9}$/;
    if (mobile.test(value)) {
        callback();
    } else {
        return callback(new Error('手机号输入错误！'));
    }
}

//表单中输入邮箱验证
export function validateEmail(rule, value, callback) {
    const email = /^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$/;
    if (email.test(value)) {
        callback();
    } else {
        return callback(new Error('邮箱输入错误！'));
    }
}
//验证网址
export function validateHttps(rule, value, callback) {
    const htps = /^((https?|ftp|file):\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
    if (htps.test(value)) {
        callback();
    } else {
        return callback(new Error('请输入正确网址！'));
    }
}