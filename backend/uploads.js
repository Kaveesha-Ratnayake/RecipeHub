import express from 'express';
import {randomUUID} from 'node:crypto';
import {mkdir,writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {authenticate} from './auth.js';
const dir=resolve('.local/uploads');
export function uploadRoutes(app){
app.use('/uploads',express.static(dir,{dotfiles:'deny',setHeaders:res=>{res.setHeader('X-Content-Type-Options','nosniff');res.setHeader('Content-Security-Policy',"default-src 'none'");}}));
app.post('/api/uploads',authenticate,express.raw({type:['image/jpeg','image/png','image/webp'],limit:'5mb'}),async(req,res,next)=>{try{const b=req.body;if(!Buffer.isBuffer(b))return res.status(400).json({message:'Select a JPEG, PNG or WebP image.'});let ext;if(b.length>8&&b.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])))ext='png';else if(b.length>3&&b[0]===255&&b[1]===216&&b[2]===255)ext='jpg';else if(b.length>12&&b.toString('ascii',0,4)==='RIFF'&&b.toString('ascii',8,12)==='WEBP')ext='webp';if(!ext)return res.status(400).json({message:'This file is not a supported image.'});await mkdir(dir,{recursive:true});const filename=randomUUID()+'.'+ext;await writeFile(resolve(dir,filename),b,{flag:'wx'});res.status(201).json({url:'http://127.0.0.1:4000/uploads/'+filename});}catch(e){next(e);}});
}
