from typing import List, Optional

import typer

from nltsecret import load_secret_db, read_secret, save_secret_db, write_secret

app = typer.Typer(help="nltsecret command line interface")


@app.callback()
def main() -> None:
    """nltsecret command group."""


@app.command()
def read(
    categories: List[str] = typer.Argument(
        ..., metavar="CATE1 CATE2 [CATE3] [CATE4] [CATE5]", help="Secret category path"
    )
) -> None:
    if len(categories) < 2 or len(categories) > 5:
        raise typer.BadParameter("read requires 2 to 5 category arguments")

    padded = categories + [""] * (5 - len(categories))
    value = read_secret(*padded)
    if value is None:
        raise typer.Exit(code=1)
    typer.echo(value)


@app.command()
def write(
    value: str = typer.Argument(..., help="Secret value to store"),
    categories: List[str] = typer.Argument(
        ..., metavar="CATE1 CATE2 [CATE3] [CATE4] [CATE5]", help="Secret category path"
    ),
) -> None:
    if len(categories) < 2 or len(categories) > 5:
        raise typer.BadParameter("write requires 2 to 5 category arguments")

    padded = categories + [""] * (5 - len(categories))
    write_secret(value, *padded)


@app.command()
def load(
    db_url: str = typer.Argument(..., help="Database URL to load secrets from"),
    cipher_key: Optional[str] = typer.Option(None, help="Cipher key for the source database"),
) -> None:
    load_secret_db(url=db_url, cipher_key=cipher_key)


@app.command()
def save(
    db_url: str = typer.Argument(..., help="Database URL to save secrets to"),
    cipher_key: Optional[str] = typer.Option(None, help="Cipher key for the target database"),
) -> None:
    save_secret_db(url=db_url, cipher_key=cipher_key)


if __name__ == "__main__":
    app()
