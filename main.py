#!/usr/bin/env python3

from lightstreamer.client import *
from datetime import datetime, timedelta
import time, argparse

parser = argparse.ArgumentParser(description='Piss stream straight from space')
parser.add_argument('-o','--log_file_path', type=str, default = None)
args = parser.parse_args()

if args.log_file_path:
  log_file_path = args.log_file_path
else:
  log_file_path = "pisslog.csv"

class SubListener(SubscriptionListener):
  def __init__(self, file_path):
    self.file_path = file_path  
  
  def onItemUpdate(self, update):
    timestamp = update.getValue("TimeStamp")
    value = update.getValue("Value")
    
    date = datetime.now() - timedelta(milliseconds=float(timestamp))
    formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"{formatted_date} ISS Piss tank level: {value}")
    
    with open(self.file_path, "a") as file:
      file.write(formatted_date + ", " + value + "\n")

sub = Subscription(
  mode="MERGE",
  items=["NODE3000005"],
  fields = ["Value", "TimeStamp"]
)
sub.addListener(SubListener(log_file_path))
sub.setRequestedSnapshot("yes")

client = LightstreamerClient("http://push.lightstreamer.com","ISSLIVE")
client.subscribe(sub)

print("\nConnecting to stream...")
client.connect()

start_time = time.monotonic() 
timeout = 10  

while client.getStatus() != "CONNECTED:WS-STREAMING":
  if time.monotonic() - start_time > timeout:
    print(f"Connection attempt timed out after {timeout} seconds.")
    client.disconnect()
    exit(1) 

print("Connected")

try:
  while True:
    time.sleep(1) 
except KeyboardInterrupt:
  client.disconnect()
  print("\nDisconnected")