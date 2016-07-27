exports.getHashtags = function getHashtags(tweetText){
  var tags = tweetText.split(" ");
  var hashtags = [];
  for(t in tags){
    if(tags[t][0] == "#")
      hashtags.push(tags[t].substring(1,tags[t].length));
  }
  return hashtags;
}

exports.getMentions = function getMentions(tweetText){
  var tags = tweetText.split(" ");
  var mentions = [];
  for(t in tags){
    if(tags[t][0] == "@")
      mentions.push(tags[t].substring(1,tags[t].length));
  }
  return mentions;
}
