// Router setup
var express    = require('express');
var router     = express.Router();
var User       = require('../models/User');
var Tweet      = require('../models/Tweet');
var mongoose   = require('mongoose');
var assert     = require('assert');
var modules    = require('./modules');

mongoose.connect('mongodb://localhost:8081/TwitterDB',{server:{poolSize:25}},function(err){
  if(err)
    console.log(err);
  else
    console.log("Successfully connected to MongoDB on port 8081.");
});

router.get('/', function(req, res) {
    res.status(200).send({ message: 'Welcome to Tweet analysis API' });
});

// Login functionality.
router.post('/login', function(req,res){
  var username = req.body.username;
  var password = req.body.password;

  if(typeof username == 'undefined' ||  typeof password == 'undefined')
    return res.status(400).send({message:'Invalid request parameters'});

  if(password==''){
    return res.status(400).send({message:'Invalid Credentials. Password is empty'});
  }
  User.findOne({username: username, password: password}, function(err,user){
    if(err){
      console.log(err);
      return res.status(500).send({message: 'Internal server error. Check back in later.'});
    }
    if(!user){
      return res.status(404).send({message: 'Invalid credentials. User not found.'});
    }
    return res.status(200).send({message: 'Login Successful.', user:user});
  });
});

// Register new user.
router.post('/register', function(req, res){
  var username = req.body.username;
  var password = req.body.password;

  if(typeof username == 'undefined' ||  typeof password == 'undefined')
    return res.status(400).send({message:'Invalid request parameters'});

  User.findOne({username: username}, function(err,user){
    if(err){
      console.log(err);
      return res.status(500).send({message: 'Internal server error. Check back in later.'});
    }
    if(!user){
      var newuser = new User();
      newuser.username = username;
      newuser.password = password;

      newuser.save(function(err, savedUser){
        if(err){
          return res.status(500).send({message: 'Internal server error. Check back in later.'});
        }
        return res.status(200).send({message:'Registered successlly.', user:savedUser});
      });
    }
    else
      return res.status(400).send({message: 'Username already exists.'});
  });
});

// Obtain tweets by a user.
router.post('/tweet', function(req,res){
  var username = req.body.username;

  User.findOne({username: username}, function(err,user){
    if(err){
      console.log(err);
      return res.status(500).send({message: 'Internal server error. Check back in later.'});
    }
    if(!user){
        return res.status(400).send({message:'Invalid Username. Cannot add tweet for invalid user.'});
    }
    else{
      var tweetText = req.body.tweetText;
      var timestamp =req.body.timestamp;
      var hashtags = modules.getHashtags(tweetText);
      var mentions = modules.getMentions(tweetText);

      if(typeof username == 'undefined' ||  typeof tweetText == 'undefined' || typeof timestamp == 'undefined')
        return res.status(400).send({message:'Invalid request parameters'});

      var newTweet = new Tweet();
      newTweet.username = username;
      newTweet.tweet = tweetText;
      newTweet.hashtags = hashtags;
      newTweet.mentions = mentions;
      newTweet.timestamp = timestamp;

      newTweet.save(function(err, savedTweet){
        if(err){
          return res.status(500).send({message: 'Internal server error. Check back in later.'});
        }
        return res.status(200).send({message:'Tweet added successlly.', tweet:savedTweet});
      });
    }
  });
});

// Find tweets by hashtags.
router.post('/findTweetsByHashtag',function(req,res){
  var queryTag = req.body.queryTag

  if(typeof queryTag == 'undefined')
    return res.status(400).send({message:'Invalid request parameters'});

  Tweet.find({ hashtags:{ $in:[queryTag] } }, function(err,foundTweets){
    if(err){
      console.log(err);
      return res.status(500).send({message: 'Internal server error. Check back in later.'});
    }
    if(foundTweets.length == 0)
      return res.status(200).send({message: 'No tweets found.', query: queryTag});
    else
      return res.status(200).send({message: 'Tweets found.', query: queryTag, tweets:foundTweets});
  });

});

// Find tweets by mentions
router.post('/findTweetsByMentions',function(req,res){
  var queryMention = req.body.queryMention

  if(typeof queryMention == 'undefined')
    return res.status(400).send({message:'Invalid request parameters'});

  Tweet.find({ mentions:{ $in:[queryMention] } }, function(err,foundTweets){
    if(err){
      console.log(err);
      return res.status(500).send({message: 'Internal server error. Check back in later.'});
    }
    if(foundTweets.length == 0)
      return res.status(200).send({message: 'No tweets found.', query: queryMention});
    else
      return res.status(200).send({message: 'Tweets found.', query: queryMention, tweets:foundTweets});
  });

});

module.exports = router;
