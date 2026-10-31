import {randomBytes,scrypt as derive,timingSafeEqual,createHash} from 'node:crypto';
import {promisify} from 'node:util';
import mongoose from 'mongoose';
const scrypt=promisify(derive);
const User=mongoose.model('User',new mongoose.Schema({name:{type:String,required:true,maxlength:60},email:{type:String,unique:true,required:true},passwordHash:String,salt:String}));
const Session=mongoose.model('Session',new mongoose.Schema({digest:{type:String,unique:true},user:{type:mongoose.Schema.Types.ObjectId,ref:'User'},expires:{type:Date,expires:0}}));
const hash=t=>createHash('sha256').update(t).digest('hex');
const safe=u=>({id:u._id.toString(),name:u.name,email:u.email});
const cookieOptions='; HttpOnly; SameSite=Strict; Path=/'+(process.env.NODE_ENV==='production'?'; Secure':'');
export async function authenticate(req,res,next){try{const token=req.headers.cookie?.split(';').map(s=>s.trim()).find(s=>s.startsWith('rh_session='))?.slice(11);if(!token)return res.status(401).json({message:'Please log in to manage recipes.'});const session=await Session.findOne({digest:hash(token),expires:{$gt:new Date()}}).populate('user');if(!session?.user)return res.status(401).json({message:'Your session has expired. Please log in again.'});req.user=session.user;req.sessionId=session._id;next();}catch(e){next(e);}}
export function authRoutes(app){
 const attempts=new Map();
 app.use('/api/auth',(req,res,next)=>{if(req.method!=='POST')return next();const now=Date.now();for(const[k,v]of attempts)if(v.until<now)attempts.delete(k);const key=req.ip;const a=attempts.get(key)||{count:0,until:now+60000};a.count++;attempts.set(key,a);if(a.count>20)return res.status(429).json({message:'Too many attempts. Please try again in a minute.'});next();});
 async function enter(req,res,next){try{const register=req.path.endsWith('/register');const{password}=req.body;const email=typeof req.body.email==='string'?req.body.email.trim().toLowerCase():'';const name=typeof req.body.name==='string'?req.body.name.trim():'';if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)||email.length>254||typeof password!=='string'||password.length>128||password.length<(register?8:1)||(register&&(name.length<2||name.length>60)))return res.status(400).json({message:'Enter a valid email, name and password (at least 8 characters for registration).'});let user=await User.findOne({email});if(register){if(user)return res.status(409).json({message:'An account with this email already exists.'});const salt=randomBytes(16).toString('hex');const passwordHash=(await scrypt(password,salt,64)).toString('hex');user=await User.create({name,email,salt,passwordHash});}else{const result=await scrypt(password,user?.salt||'invalid-user-salt',64);if(!user||!timingSafeEqual(result,Buffer.from(user.passwordHash,'hex')))return res.status(401).json({message:'Email or password is incorrect.'});}const token=randomBytes(32).toString('hex');await Session.create({digest:hash(token),user:user._id,expires:new Date(Date.now()+86400000)});res.setHeader('Set-Cookie','rh_session='+token+cookieOptions+'; Max-Age=86400');res.status(register?201:200).json({user:safe(user)});}catch(e){if(e.code===11000)return res.status(409).json({message:'An account with this email already exists.'});next(e);}}
 app.post('/api/auth/register',enter);app.post('/api/auth/login',enter);
 app.get('/api/auth/me',authenticate,(req,res)=>res.json({user:safe(req.user)}));
 app.post('/api/auth/logout',async(req,res,next)=>{try{const token=req.headers.cookie?.split(';').map(s=>s.trim()).find(s=>s.startsWith('rh_session='))?.slice(11);if(token)await Session.deleteOne({digest:hash(token)});res.setHeader('Set-Cookie','rh_session='+cookieOptions+'; Max-Age=0');res.sendStatus(204);}catch(e){next(e);}});
}

