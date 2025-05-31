import re,typer,json
from pathlib import Path
from datetime import datetime

app=typer.Typer()


@app.command()
def parser(file:Path,stats:bool=False):
    
    pattern = r"(?P<date>\d{6})\s+(?P<time>\d{6})\s+(?P<id>\d+)\s+(?P<level>[A-Z]+)\s+(?P<component>[a-zA-Z0-9\.$]+):\s+(?P<message>.*)"
    
    if not file.exists():
        return
    
    total=0
    count_info=0
    count_error=0
    count_warn=0
    buffer=[]
    
    with file.open("r",encoding="utf-8") as f:     
        for log_line in f:
            match = re.match(pattern, log_line)
            total+=1
            if match:
                data = match.groupdict()

                if data['level']=="INFO":
                    count_info+=1

                if data['level']=="ERROR":
                    count_error+=1

                if data['level']=="WARN":
                    count_warn+=1

                # Convert to ISO timestamp (for compaction)
                try:
                    dt = datetime.strptime(f"{data['date']} {data['time']}", "%y%m%d %H%M%S")
                    data["timestamp"] = dt.isoformat()
                except ValueError:
                    data["timestamp"] = "invalid"
                buffer.append(data)

                
            else:
                typer.echo({"error": "Failed to parse"})

        typer.echo(json.dumps(buffer, indent=2))

    if stats:
        percent_info=(count_info/total)*100 if total>0 else 0
        percent_error=(count_error/total)*100 if total>0 else 0
        percent_warn=(count_warn/total)*100 if total>0 else 0

        try:
            timestamps=[]
            for i in range(len(buffer)):
                ts_str = buffer[i]["timestamp"]
                ts_obj = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S")
                timestamps.append(ts_obj)
            eventsec = Event(timestamps)
        except ValueError:
            print("EXit")
        typer.echo(f"\nTop log levels: INFO ({percent_info:.2f}%), ERROR ({percent_error:.2f}%), WARN ({percent_warn:.2f}%) | Avg. {eventsec:.5f} events/sec")


# events/sec calculation

def Event(timestamps:list)->float:  
    
    if not timestamps:
        return 0.0
                    
    earliest = min(timestamps)
    latest = max(timestamps)
    duration = (latest - earliest).total_seconds()
                    
    if duration == 0:
        return len(timestamps)  # all events at same second
    avg_events_per_sec = len(timestamps) / duration
                    
    return avg_events_per_sec
    
if __name__=="__main__":
    app()

