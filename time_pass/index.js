const fs = require('fs');
const crypto = require('crypto');


async function hashfile(filepath){
  return new Promise((resolve,reject)=> {
    const hash = crypto.createHash('sha256');
    const stream = fs.createReadStream(filepath);

    stream.on('data',(chunk) => {
      hash.update(chunk);
    })
    stream.on('end',()=>{
      resolve(hash.digest('hex'))
    })
    stream.on('error',(err)=> {
      reject(err)
    })
  })
}

async function main(){
  const file1 = process.argv[2];
  const file2 = process.argv[3];

  if(!file1 || !file2){
    console.log('Usage: node index.js file1.txt file2.txt');
    process.exit(1);
  }
  try {
    const hash1 = await hashfile(file1);
    const hash2 = await hashfile(file2);

    if (hash1 == hash2){
      console.log('Match');
    } else {
      console.log('Tampered/Mismatch');
    }
  }
  catch (err) {
    console.error('Error:', err.message);
  }
}

main();
