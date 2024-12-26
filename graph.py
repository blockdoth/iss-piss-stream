    
import argparse, csv
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


parser = argparse.ArgumentParser(description='Pissualizer')
parser.add_argument('-f','--log_file_path', type=str, default = None)
args = parser.parse_args()
    

if args.log_file_path:
  log_file_path = args.log_file_path
else:
  log_file_path = "pisslog.csv"    

timestamps = []
values = []


with open(log_file_path, "r") as file:
  reader = csv.reader(file)
  for row in reader:
    timestamp, value = row[0].strip(), int(row[1].strip())
    date_object = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    timestamps.append(date_object)
    values.append(value)

# plt.xkcd()
plt.ylim(0, 100)
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(100))

plt.title("ISS piss flow over time")
plt.tight_layout()
plt.plot(timestamps, values)
plt.show()