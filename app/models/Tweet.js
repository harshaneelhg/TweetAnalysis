var mongoose = require('mongoose');

var tweetSchema = new mongoose.Schema({
    username : {type: String, unique: true},
    tweet: {type:String},
    hashtags: [{type: String}],
    mentions: [{type: String}],
    timestamp: {type: String}
});

var Tweet = mongoose.model('tweetModel', tweetSchema);
module.exports = Tweet;
