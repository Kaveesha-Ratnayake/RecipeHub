import mongoose from 'mongoose';
await mongoose.connect(process.env.MONGODB_URI);
try {
const c=mongoose.connection.collection('recipes');
const filter={sampleKey:'expanded:Iced lemon mint tea',title:'Iced lemon mint tea'};
const recipe=await c.findOne(filter);
if(recipe){await mongoose.connection.collection('archivedRecipes').updateOne({_id:recipe._id},{$setOnInsert:{...recipe,archivedAt:new Date()}},{upsert:true});await c.deleteOne(filter);}
console.log('Removed tea recipe from collection; recoverable copy archived.');
}finally{await mongoose.disconnect();}
