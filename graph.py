import argparse, csv
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates
import matplotlib.dates


def load_logs(log_file_path):
  timestamps = []
  values = []
  with open(log_file_path, "r") as file:
    reader = csv.reader(file)
    for row in reader:
      timestamp, value = row[0].strip(), int(row[1].strip())
      date_object = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
      timestamps.append(date_object)
      values.append(value)
  
  return (timestamps, values)


def filter_and_gaps(piss_data, start_date, end_date):
  timestamps = []
  values  = []
  
  previous_timestamp = None
  for (timestamp, value) in zip(*piss_data):
    if (start_date is None or timestamp >= start_date) and (end_date is None or timestamp <= end_date):
      # Remove gaps
      if previous_timestamp and (timestamp - previous_timestamp).seconds > 5 * 3600:  
        timestamps.append(None)
        values.append(None)
      else:
        timestamps.append(timestamp)
        values.append(value)
      
      previous_timestamp = timestamp

  return (timestamps, values)

def build_plot(piss_data):
  timestamps, _ = piss_data
  
  plt.xkcd()
  plt.figure(figsize=(10,5))
  plt.ylim(0, 100)
  
  if plt.gcf().canvas.manager.toolbar:
    plt.gcf().canvas.manager.toolbar.pack_forget()  
  
  ax = plt.gca()
  ax.yaxis.set_major_formatter(mtick.PercentFormatter(100))

  total_days = (timestamps[-1] - timestamps[0]).days
  interval = max(1, total_days // 5)  

  ax.xaxis.set_major_locator(mdates.DayLocator(interval=interval))
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

  plt.xlabel("Time")
  plt.ylabel("Fullness of piss tank")
  plt.title("International Space Station urine tank piss level")
  plt.plot(piss_data)
  plt.tight_layout()
  
  return plt
  
def pissualize(log_file_path, plot, save_plot, plot_out_path):
  piss_plot = build_plot(load_logs(log_file_path))
  if save_plot:
    piss_plot.savefig(plot_out_path)
  if plot:
    piss_plot.show()


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Pissualizer')
  parser.add_argument('-f','--log_file_path', type=str, default = "pisslog.csv")
  parser.add_argument('-o','--plot_out_path', type=str, default = "pissplot.png")
  parser.add_argument('-p','--plot', action = "store_false")
  parser.add_argument('-s','--save_plot', action = "store_true")
  args = parser.parse_args()

  pissualize(args.log_file_path, args.plot, args.save_plot, args.plot_out_path)