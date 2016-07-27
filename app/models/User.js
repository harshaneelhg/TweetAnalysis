var mongoose = require('mongoose');

var userSchema = new mongoose.Schema({
    username : {type: String, unique: true},
    password : {type: String}
});

var User = mongoose.model('userModel', userSchema);
module.exports = User;
