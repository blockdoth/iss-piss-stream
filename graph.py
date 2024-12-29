import argparse, csv
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates


def pissualize(log_file_path, plot, save_plot, plot_out_path):
  timestamps = []
  values = []
  previous_timestamp = None
  with open(log_file_path, "r") as file:
    reader = csv.reader(file)
    for row in reader:
      timestamp, value = row[0].strip(), int(row[1].strip())
      date_object = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
      
      # Set gaps to zero
      if previous_timestamp and (date_object - previous_timestamp).seconds > 5 * 3600:  
        timestamps.append(None)
        values.append(None)
      else:
        timestamps.append(date_object)
        values.append(value)
      previous_timestamp = date_object

  plt.xkcd()
  plt.figure(figsize=(10,5))
  plt.ylim(0, 100)

  if plt.gcf().canvas.manager.toolbar:
    plt.gcf().canvas.manager.toolbar.pack_forget()  
  
  ax = plt.gca()
  ax.yaxis.set_major_formatter(mtick.PercentFormatter(100))
  ax.xaxis.set_major_locator(mdates.DayLocator())
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

  plt.xlabel("Time")
  plt.ylabel("Fullness of piss tank")
  plt.title("International Space Station urine tank piss level")
  plt.plot(timestamps, values)
  plt.tight_layout()
  if save_plot:
    plt.savefig(plot_out_path)
  if plot:
    plt.show()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Pissualizer')
  parser.add_argument('-f','--log_file_path', type=str, default = "pisslog.csv")
  parser.add_argument('-o','--plot_out_path', type=str, default = "pissplot.png")
  parser.add_argument('-p','--plot', action = "store_false")
  parser.add_argument('-s','--save_plot', action = "store_true")
  args = parser.parse_args()

  pissualize(args.log_file_path, args.plot, args.save_plot, args.plot_out_path)