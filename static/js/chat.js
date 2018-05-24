var socket
// 默认进入大厅频道
var current_room = 'Main'

var e = function (sel) {
    return document.querySelector(sel)
}

var apiChatRoomUser = function (callback) {
    var path = '/api/chat/user?room=' + current_room
    ajax('GET', path, '', callback)
}

var loadOnlineUser = function () {
    apiChatRoomUser (function (r) {
        var response = JSON.parse(r)
        $(`.current-user li`).remove()
        var userList = response
        for (const index in userList) {
            $(`.current-user`).append(userListTemplate(userList[index]))
            $(`.current-user #${userList[index].id} span`).text(userList[index].name)
        }
    })
}

var join_room = function (room) {
    clear_board()
    current_room = room
    console.log('切换房间', current_room)
    var data = {
        room: room,
    }
    socket.emit('join', data, function () {
        change_title()
        loadOnlineUser()
    })
}

var change_active_status = function () {
    var mainClass = e('.main-room').parentNode.classList
    var gameClass = e('.game-room').parentNode.classList
    var elseClass = e('.else-room').parentNode.classList
    mainClass.remove('active')
    gameClass.remove('active')
    elseClass.remove('active')
    if (current_room == 'Main') {
        mainClass.add('active')
    } else if (current_room == 'Game') {
        gameClass.add('active')
    } else {
        elseClass.add('active')
    }
}

var change_title = function () {
    var title = 'Chat Room - ZN'
    if (current_room == '') {
        var header = 'Chat Room - Unknow'
    } else {
        var header = 'Chat Room - ' + current_room
        title = 'Chat Room | ' + current_room + ' - ZN'
    }
    var tag = e("#id-rooms-title")
    tag.innerHTML = header
    document.title = title
    change_active_status()
}

var clear_board = function () {
    e("#id_chat_area").value = ''
}

var autoScroll = function () {
    var scrollTop = e("#id_chat_area").scrollHeight
    e("#id_chat_area").scrollTop = scrollTop
}

var userListTemplate = function (data) {
    var url = ''
    if (data.id.indexOf('Guest') == -1) {
        url = `href='/@${data.username}'`
    }
    t = `
        <li id="${data.id}">
            <a ${url} class="has-icon">
                <img src="${data.user_img}" alt="${data.username}" class="is-circle">
                <span class="username"></span>
            </a>
        </li>
    `
    return t
}

var __main = function () {
    // 初始化 websocket
    var namespace = '/chat'
    var url = `ws://${document.domain}:${location.port}${namespace}`
    socket = io.connect(url, {
        transports: ['websocket']
    })
    socket.on('connect', function () {
        console.log('connect')
    })

    var chatArea = e('#id_chat_area')

    socket.on('status', function (data) {
        chatArea.value += `< ${data.message} >\n`
        autoScroll()
        if (data.status == 'leave') {
            $(`.current-user #${data.id}`).remove()
        } else if (data.status == 'join') {
            $(`.current-user`).append(userListTemplate(data.user_info))
            $(`.current-user #${data.user_info.id} span`).text(data.user_info.name)
        }
    })

    socket.on('message', function (data) {
        chatArea.value += (data.message + '\n')
        autoScroll()
    })

    // 加入默认频道
    join_room(current_room)

    var input = e('#id_input_text')
    input.addEventListener('keypress', function (event) {
        // console.log('keypress', event)
        if (event.key == 'Enter') {
            // 得到用户输入的消息
            message = input.value
            if (message.replace(/ /g, "") != '') {
                // 发送消息给后端
                var data = {
                    message: message,
                }
                socket.emit('send', data, function () {
                    // 清空用户输入
                    input.value = ''
                })
            }
            autoScroll()
        }
    })

    // 切换频道
    e('.bar').addEventListener('click', function (event) {
        var self = event.target
        if (self.classList.contains('room')) {
            console.log('redirect to chaneel', self.text)
            // 离开频道
            socket.emit('leave', function () {
                console.log("leave room")
                current_room = self.text
                // 加入房间
                join_room(current_room)
            })
        }
    })

    // 关闭窗口时自动离开频道
    window.onbeforeunload = function () {
        socket.emit('leave', function () {
            console.log("leave room")
        })
    }
}

__main()