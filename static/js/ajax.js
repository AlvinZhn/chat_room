var log = function () {
    console.log.apply(console, arguments)
}

var e = function (sel) {
    return document.querySelector(sel)
}

/*
 ajax 函数
*/
var ajax = function (method, path, data, responseCallback) {
    var r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式为 application/json
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function () {
        if (r.readyState === 4) {
            responseCallback(r.response)
        }
    }
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data)
    // log('data', data)
    // 发送请求
    r.send(data)
}
