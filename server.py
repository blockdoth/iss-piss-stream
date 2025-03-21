from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from graph import *
from datetime import datetime, timedelta

import io

app = FastAPI()

logs = load_logs("pisslog.csv")

@app.get("/pisslog")
async def static_plot():
  return FileResponse("pisslog.csv")

@app.get("/pissplot")
async def static_plot():
  return FileResponse("pissplot.png")

@app.get("/pissplot/{days}")
async def generate_plot(days):
  end_date = datetime.now()
  start_date = end_date - timedelta(days=int(days))
  filtered_logs = filter_and_gaps(logs, start_date, end_date)
  piss_plot = build_plot(filtered_logs)

  image_buffer = io.BytesIO()
  piss_plot.savefig(image_buffer, format="png")
  image_buffer.seek(0) # Reset file pointer to start for reading

  return StreamingResponse(image_buffer, media_type="image/png")


