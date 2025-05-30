import typer
import re
from collections import deque
from pathlib import Path

app=typer.Typer()


@app.command()
def logread(file:Path,lines:int = typer.Option(10, help="Number of lines to show")):
    if not file.exists():
        typer.echo("File doesn't exist")
        raise typer.Exit(code=1)
    
    with file.open("r",encoding='utf-8',errors='replace') as f:
        buffer=[]
        for line in f:
            buffer.append(line)
            if len(buffer)>lines:
                buffer.pop()
                break
        typer.echo("".join(buffer))

@app.command()
def loggrep(file:Path,pattern:str,stats:bool=False):
    total=0
    matched=0
    regex=re.compile(pattern)
    
    if not file.exists():
        typer.echo("File doesn't exist")
        raise typer.Exit(code=1)
    
    with file.open("r",encoding="utf-8",errors='replace') as f:
        for line in f:
            total+=1
            if regex.search(line):
                matched+=1
                typer.echo(line.strip())

    if stats:
        percent=(matched/total)*100 if total>0 else 0
        typer.echo(f"\nStats: {matched}/{total} lines matched ({percent:.2f}%)")

@app.command()
def logtail(file: Path, num_lines: int = typer.Option(10, help="Number of lines to show")):
    if not file.exists():
        typer.echo("File doesn't exist")
        raise typer.Exit(code=1)

    with file.open("r", encoding="utf-8",errors='replace') as f:
        last_lines = deque(f, maxlen=num_lines)

    typer.echo("".join(last_lines))

if __name__=='__main__':
    app()