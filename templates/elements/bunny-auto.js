function suggest(data,query,excludes){
    // Only run this when the user has just finished writing a new word
    if(query[query.length-1] != " ")return;
    
    // Clear the output
    var output = [];

    // Go through each word
    var words = query.split(" "); //words.pop();
    var rgxQuery = "";
    for(var id in words){
        
        // Short words don't matter
        if(words[id].length < 3)continue;
        
        // Neither do excluded words
        var ct = false;
        for(var exid in excludes){
            if(excludes[exid] == words[id].toLowerCase()){
                ct = true;
                break;
            }
        }
        if(ct)continue;
        
        // Combine every useful word into a regex query
        if(rgxQuery!=="")rgxQuery+="|";
        words[id] = words[id].replace(/[,.\?\"\'\\\/]/,"");
        rgxQuery += words[id]+"[^a-zA-Z0-9]+";
    }
    if(words.length<1 || rgxQuery=="")return;
    var rgx = new RegExp("("+rgxQuery+")","ig");
    
    // Run the query, pull out matches
    for(id in data){
        var oNote = this.data[id];
        var matches = (oNote.head+" "+oNote.body+" ").match(rgx);
        
        // This sneaky algorithm uses average word length to help determine relevance
        var averageWordLength = 0;
        for(var wid in matches){ averageWordLength += matches[wid].length / matches.length };
        
        var age = new Date().getTime() - oNote.time;
        
        if(matches != null && matches.length > 0){
            oNote["queryRank"] = oNote.rank * matches.length * parseInt(Math.sqrt(averageWordLength) + 5000/age);
            oNote["found"] = oNote.note;//.replace(rgx,"<b>\$1</b>");
            output.push(oNote);
        }
    }
    
    // Sort the output by rank
    output.sort(function(a,b){return a.queryRank < b.queryRank});
    return output;
}