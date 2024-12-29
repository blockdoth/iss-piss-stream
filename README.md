# ISS Piss Stream Monitor
---

Ever wanted to know the contents of the piss tank of the international space station? Now you do!

# Features
- Real-Time Piss Level Monitoring
- Logging
- Minimal mode, for embedding into taskbars
- XKCD style graph
  
# Setup
- Specify it a as a flake input, (pick a commit, its likely I will break things)
```
iss-piss-stream.url = "github:blockdoth/iss-piss-stream/{OPTIONAL-COMMIT_HASH}}";
```
- Or use `nix run` to run it without installing
```
nix run github:blockdoth/iss-piss-stream 
```

- Alternatively: 
```
git clone git@github.com:blockdoth/iss-piss-stream.git
some venv thing? idk I dont use them
pip install lightstreamer-client
```
# Usage

Run the script using:
```
./piss_stream.py [-o LOG_FILE_PATH] [-p]
```
Options:
- `-o, --log_file_path` \
    Specify the path for the log file. Default: pisslog.csv.

- `-p, --percentage_only` \
    Print only the percentage values to the console without timestamps or logging.
