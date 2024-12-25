print("Rebuild")
from lightstreamer.client import *

import sys, logging

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

loggerProvider = ConsoleLoggerProvider(ConsoleLogLevel.DEBUG)
LightstreamerClient.setLoggerProvider(loggerProvider)

sub = Subscription(
    mode="MERGE",
    items=["NODE3000005"],
    fields = ["TimeStamp"]
)

class SubListener(SubscriptionListener):
  def onItemUpdate(self, update):
    print("UPDATE")


sub.addListener(SubListener())


client = LightstreamerClient("http://push.lightstreamer.com","ISSLIVE")
client.subscribe(sub)

print("Connecting")

client.connect()
