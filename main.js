var Ls = require('lightstreamer-client-node');

var sub = new Ls.Subscription("MERGE",["NODE3000005"],["Value"]);

sub.setRequestedSnapshot("yes");
sub.addListener({
    onItemUpdate: function(obj) {
      console.log( "ISS Piss tank level: " + obj.getValue("Value") + "%");
    }
});
var client = new Ls.LightstreamerClient("http://push.lightstreamer.com","ISSLIVE");  
client.connect();
client.subscribe(sub);
