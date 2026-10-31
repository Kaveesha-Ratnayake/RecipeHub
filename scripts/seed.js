import mongoose from 'mongoose';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
await mongoose.connect(process.env.MONGODB_URI);
const collection=mongoose.connection.collection('recipes');
if(await collection.countDocuments()===0){const source=readFileSync('frontend/src.jsx','utf8');const start=source.indexOf('const photo=');const end=source.indexOf('const categories=');const data=vm.runInNewContext(source.slice(start,end)+';initial');await collection.insertMany(data.map(({id,...r})=>({...r,createdAt:new Date(),updatedAt:new Date()})));console.log('Added 6 starter recipes.');}else console.log('Recipes already exist; no changes made.');
await mongoose.disconnect();
