const net = require('net');
 const fs = require('fs');

 const mode = process.argv[2];
 const port = parseInt(process.argv[3], 10);
 const filePath = process.argv[4];

if (!mode || !port) {
     console.log("Usage:");
     console.log("  Receiver: node node.js receive 3000");
     console.log("  Sender:   node node.js send 3000 path/to/file.mp4");
     process.exit(1);
}

if (mode === 'receive') {
     const server = net.createServer((socket) => {
         const writeStream =
fs.createWriteStream('received_file.txt');

         socket.pipe(writeStream);

         writeStream.on('close', () => {
             console.log('File received and saved as received_file.txt');
         });
     });

     server.listen(port, () => {
         console.log(`Receiver: Waiting for incoming file on port
 ${port}...`);
     });
 } else if (mode === 'send') {
     if (!filePath) {
         console.log("Error: You must specify a file to send.");
         process.exit(1);
     }

     const socket = net.createConnection({ port: port, host:
 '127.0.0.1' }, () => {
         console.log(`Connected to server on port ${port}`);

         const readStream = fs.createReadStream(filePath);

         readStream.pipe(socket);

         readStream.on('end', () => {
             console.log(`Sent file: ${filePath}`);
             socket.end();
         });
     });

     socket.on('error', (err) => {
         console.error("Connection error:", err.message);
         process.exit(1);
     });
 } else {
     console.log("Invalid mode. Use 'receive' or 'send'.");
     process.exit(1);
 }
