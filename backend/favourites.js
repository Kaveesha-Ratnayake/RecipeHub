import mongoose from 'mongoose';
import {authenticate} from './auth.js';
const schema=new mongoose.Schema({user:{type:mongoose.Schema.Types.ObjectId,required:true,ref:'User'},recipe:{type:mongoose.Schema.Types.ObjectId,required:true,ref:'Recipe'}},{timestamps:true});
schema.index({user:1,recipe:1},{unique:true});
const Favourite=mongoose.model('Favourite',schema);
export function favouriteRoutes(app){
app.get('/api/favourites',authenticate,async(req,res,next)=>{try{const items=await Favourite.find({user:req.user._id}).populate('recipe','_id');res.json(items.filter(x=>x.recipe).map(x=>x.recipe._id.toString()));}catch(e){next(e);}});
app.put('/api/favourites/:id',authenticate,async(req,res,next)=>{try{if(!mongoose.isValidObjectId(req.params.id))return res.status(400).json({message:'Invalid recipe ID.'});if(!await mongoose.model('Recipe').exists({_id:req.params.id}))return res.status(404).json({message:'Recipe no longer exists.'});try{await Favourite.updateOne({user:req.user._id,recipe:req.params.id},{$setOnInsert:{user:req.user._id,recipe:req.params.id}},{upsert:true});}catch(e){if(e.code!==11000)throw e;}res.sendStatus(204);}catch(e){next(e);}});
app.delete('/api/favourites/:id',authenticate,async(req,res,next)=>{try{if(!mongoose.isValidObjectId(req.params.id))return res.status(400).json({message:'Invalid recipe ID.'});await Favourite.deleteOne({user:req.user._id,recipe:req.params.id});res.sendStatus(204);}catch(e){next(e);}});
}
