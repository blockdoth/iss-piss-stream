#!/usr/bin/env python3

from lightstreamer.client import *
from datetime import datetime, timedelta
import time, argparse

parser = argparse.ArgumentParser(description='Piss stream straight from space')
parser.add_argument('-l','--log', action = "store_true")
parser.add_argument('-f','--log_file_path', type=str, default = "./pisslog.csv")
parser.add_argument('-p','--percentage_only', action = "store_true")
parser.add_argument('-u','--unix', action = "store_true")

args = parser.parse_args()
percentage_only = args.percentage_only
log = args.log
log_file_path = args.log_file_path
unix = args.unix



class SubListener(SubscriptionListener):
  def __init__(self, file_path, percentage_only):
    self.file_path = file_path  
    self.percentage_only = percentage_only
  
  def onItemUpdate(self, update):
    piss_level = update.getValue("Value")
    if percentage_only:
      print(piss_level, flush=True) 
      return 
    timestamp = update.getValue("TimeStamp")
    
    date = datetime.now() - timedelta(milliseconds=float(timestamp))
    formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"[{formatted_date}] International Space Station piss tank level: {piss_level}%", flush=True)
    
    if unix:
      write_date = datetime.timestamp(date)
    else:
      write_date = formatted_date
    if log:
      with open(self.file_path, "a") as file:
        file.write(f"{write_date}, {piss_level}\n")

sub = Subscription(
  mode="MERGE",
  items=["NODE3000005"],
  fields = ["Value", "TimeStamp"]
)

sub.addListener(SubListener(log_file_path, percentage_only))
sub.setRequestedSnapshot("yes")

client = LightstreamerClient("http://push.lightstreamer.com","ISSLIVE")
client.subscribe(sub)

if not percentage_only:
  print("Connecting to stream...")
client.connect()

start_time = time.monotonic() 
timeout = 10  

while client.getStatus() != "CONNECTED:WS-STREAMING":
  if time.monotonic() - start_time > timeout:
    if not percentage_only:
      print(f"Connection attempt timed out after {timeout} seconds.")
    client.disconnect()
    exit(1) 

if not percentage_only:
  print("Connected")

try:
  while True:
    time.sleep(1) 
except KeyboardInterrupt:
  client.disconnect()
  if not percentage_only:
    print("\nDisconnected")