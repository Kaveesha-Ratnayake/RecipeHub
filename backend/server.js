import express from 'express';
import cors from 'cors';
import mongoose from 'mongoose';
import {authRoutes,authenticate} from './auth.js';
import {favouriteRoutes} from './favourites.js';
import {ratingRoutes} from './ratings.js';
import {uploadRoutes} from './uploads.js';
const app=express();
app.use(cors({origin:['http://127.0.0.1:5173','http://127.0.0.1:5174','http://127.0.0.1:5175'],credentials:true}));
app.use(express.json({limit:'100kb'}));
authRoutes(app);
const schema=new mongoose.Schema({owner:{type:mongoose.Schema.Types.ObjectId,ref:'User'},title:{type:String,required:true,maxlength:120},category:{type:String,enum:['Breakfast','Lunch','Dinner','Dessert','Drinks'],required:true},time:{type:Number,min:1,max:1440,required:true},servings:{type:Number,min:1,max:100,required:true},description:{type:String,maxlength:500},image:{type:String,maxlength:2000},ingredients:{type:[String],validate:v=>v.length>0},instructions:{type:[String],validate:v=>v.length>0}},{timestamps:true});
const Recipe=mongoose.model('Recipe',schema);
favouriteRoutes(app);
ratingRoutes(app);
uploadRoutes(app);
const publicRecipe=doc=>{const r=doc.toObject();const owner=r.owner;return {...r,owner:owner?._id?.toString()||null,authorName:owner?.name||'RecipeHub kitchen'};};
const fields=['title','category','time','servings','description','image','ingredients','instructions'];
const pick=b=>Object.fromEntries(fields.filter(k=>b[k]!==undefined).map(k=>[k,b[k]]));
app.get('/api/recipes',async(req,res,next)=>{try{res.json((await Recipe.find().sort({createdAt:-1}).populate('owner','name')).map(publicRecipe));}catch(e){next(e);}});
app.post('/api/recipes',authenticate,async(req,res,next)=>{try{const r=await Recipe.create({...pick(req.body),owner:req.user._id});await r.populate('owner','name');res.status(201).json(publicRecipe(r));}catch(e){next(e);}});
app.put('/api/recipes/:id',authenticate,async(req,res,next)=>{try{const r=await Recipe.findOneAndUpdate({_id:req.params.id,owner:req.user._id},pick(req.body),{new:true,runValidators:true}).populate('owner','name');r?res.json(publicRecipe(r)):res.status(404).json({message:'Recipe not found'});}catch(e){next(e);}});
app.delete('/api/recipes/:id',authenticate,async(req,res,next)=>{try{const r=await Recipe.findOneAndDelete({_id:req.params.id,owner:req.user._id});r?res.sendStatus(204):res.status(404).json({message:'Recipe not found'});}catch(e){next(e);}});
app.use((err,req,res,next)=>{if(err.type==='entity.too.large')return res.status(413).json({message:'Photo must be smaller than 5 MB.'});return res.status(['ValidationError','CastError'].includes(err.name)?400:500).json({message:err.name==='ValidationError'?err.message:err.name==='CastError'?'Invalid recipe ID':'Unable to complete request'});});
if(!process.env.MONGODB_URI)throw new Error('Set MONGODB_URI in backend/.env');
await mongoose.connect(process.env.MONGODB_URI);
app.listen(process.env.PORT||4000,()=>console.log('RecipeHub API: http://127.0.0.1:4000'));


