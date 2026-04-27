import typer
import 

app = typer.Typer()

@app.command()
def merge():
    print("PDFを結合します")

@app.command()
def split():
    print("PDFを分割します")

if __name__ == "__main__":
    app()

if __name__ == "__main__":
    app()