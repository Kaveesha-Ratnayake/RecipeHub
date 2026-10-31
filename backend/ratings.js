import mongoose from 'mongoose';
import {authenticate} from './auth.js';
const schema=new mongoose.Schema({user:{type:mongoose.Schema.Types.ObjectId,required:true},recipe:{type:mongoose.Schema.Types.ObjectId,required:true},value:{type:Number,min:1,max:5,required:true}});schema.index({user:1,recipe:1},{unique:true});
const Rating=mongoose.model('Rating',schema);
export async function summary(){return Rating.aggregate([{$group:{_id:'$recipe',average:{$avg:'$value'},count:{$sum:1}}}]);}
export function ratingRoutes(app){
app.get('/api/ratings',async(req,res,next)=>{try{res.json(await summary());}catch(e){next(e);}});
app.get('/api/ratings/mine',authenticate,async(req,res,next)=>{try{res.json(Object.fromEntries((await Rating.find({user:req.user._id})).map(r=>[r.recipe.toString(),r.value])));}catch(e){next(e);}});
app.put('/api/ratings/:id',authenticate,async(req,res,next)=>{try{const value=req.body.value;if(!mongoose.isValidObjectId(req.params.id)||!Number.isInteger(value)||value<1||value>5)return res.status(400).json({message:'Choose a whole-number rating from 1 to 5.'});if(!await mongoose.model('Recipe').exists({_id:req.params.id}))return res.status(404).json({message:'Recipe not found.'});const filter={user:req.user._id,recipe:req.params.id};try{await Rating.updateOne(filter,{$set:{value}},{upsert:true,runValidators:true});}catch(e){if(e.code!==11000)throw e;await Rating.updateOne(filter,{$set:{value}},{runValidators:true});}res.json((await summary()).find(r=>r._id.toString()===req.params.id));}catch(e){next(e);}});
}
