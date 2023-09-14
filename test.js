const express = require('express');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);

app.use(express.static(__dirname + '/public'));

io.on('connection', (socket) => {
    console.log('User connected');

    socket.on('message', (message) => {
        console.log('Message received:', message);
        // 메시지를 다른 연결된 클라이언트에게 브로드캐스트
        socket.broadcast.emit('message', message);
    });

    socket.on('disconnect', () => {
        console.log('User disconnected');
    });
});

http.listen(3000, () => {
    console.log('Server is running on port 3000');
});
