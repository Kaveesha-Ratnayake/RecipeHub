import {spawn} from 'node:child_process';
import {existsSync,mkdirSync,readdirSync} from 'node:fs';
import {resolve,join} from 'node:path';
import net from 'node:net';
const running=await new Promise(resolve=>{const socket=net.connect({host:'127.0.0.1',port:27017});socket.setTimeout(1000);socket.once('connect',()=>{socket.destroy();resolve(true);});socket.once('error',()=>resolve(false));socket.once('timeout',()=>{socket.destroy();resolve(false);});});
if(running){console.log('Port 27017 is already in use. If MongoDB is running, leave it running and use npm run server.');process.exit(0);}
const root=resolve('.local/mongodb');
const folder=existsSync(root)?readdirSync(root).find(n=>existsSync(join(root,n,'bin','mongod.exe'))):null;
const program=process.env.MONGOD_PATH||(folder?join(root,folder,'bin','mongod.exe'):'mongod');
const db=resolve('.local/data');mkdirSync(db,{recursive:true});
const child=spawn(program,['--dbpath',db,'--bind_ip','127.0.0.1','--port','27017'],{stdio:'inherit',windowsHide:true});
child.on('error',e=>{console.error(e.code==='ENOENT'?'MongoDB executable not found. Install MongoDB Community Server and start its service, add mongod to PATH, set MONGOD_PATH, or configure MongoDB Atlas in backend/.env. See README.md.':e.message);process.exitCode=1;});
child.on('exit',code=>{process.exitCode=code||0;});
process.on('SIGINT',()=>child.kill('SIGINT'));
