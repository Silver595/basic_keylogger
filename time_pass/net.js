const net = require('net');

const server = net.createServer((socket) => {
  console.log('A Peer Connected!');
  socket.on('data',(chunk) => {
    console.log('Recived:', chunk.toString());
  })
  socket.on('end',()=> {
    console.log('Peer Disconnected');
  })
});

server.listen(3000,()=> {
  console.log('Listening on port 3000');
})
