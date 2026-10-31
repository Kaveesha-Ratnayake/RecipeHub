import mongoose from 'mongoose';
await mongoose.connect(process.env.MONGODB_URI);
try {
const result=await mongoose.connection.collection('recipes').updateOne({title:'Iced lemon mint tea',sampleKey:'expanded:Iced lemon mint tea'},{$set:{image:'/images/iced-lemon-mint-tea.png',updatedAt:new Date()}});
if(result.matchedCount!==1)throw Error('Tea recipe not found');
console.log('Updated Iced lemon mint tea photo.');
}finally{await mongoose.disconnect();}
