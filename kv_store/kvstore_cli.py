import typer,time
import kvstore,sys

"""
    The Commands available are: set -> set key value pair
    get -> get a value if provided key
    delete -> delete a key from existence
    stats -> various info related to keys present in both cache and ttl
    clear -> clear the json file to anew
    store -> shows the keys value pair in both ttl and cache, that is inside the class of kvstore called InMemoryKV 
"""
app=typer.Typer()

kv=kvstore.InMemoryKV()

@app.command()
def set(key:str,value:str,ttl:int = typer.Option(None, help="time to live(ttl) in seconds")):
    kv.set_key_value(key,value,ttl)
    typer.echo("OK")

@app.command()
def get(key:str):
    value=kv.get_value(key)
    if value is not None:
        typer.echo(value)

@app.command()
def delete(key:str):
    kv.delete_key(key)
    typer.echo(f"Key {key} deleted!")


@app.command()
def stats():
    total_keys = len(kv.cache)
    ttl_keys = len(kv.ttl)
    typer.echo(f"Total keys: {total_keys}")
    typer.echo(f"Keys with TTL: {ttl_keys}")

@app.command()
def clear():
    """Clear all data"""
    kv.cache.clear()
    kv.ttl.clear()
    kv.save_to_disk()

    typer.echo("All data cleared!")

@app.command()
def store():
    kv.printall()

if __name__=="__main__":
    app()