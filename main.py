import click
import subprocess
import os
import sys
from yaspin import yaspin
from datetime import datetime

from scrape import scrape_multiple
from search import get_search_results
from llm import get_llm, refine_query, filter_results, generate_summary
from llm_utils import get_model_choices

MODEL_CHOICES = get_model_choices()

@click.group()
@click.version_option()
def architect_ai():
    """Architect AI — Local Intelligence Suite (Ollama Only)."""
    pass

@architect_ai.command()
@click.option("--model", "-m", default="architect", show_default=True,
              type=click.Choice(MODEL_CHOICES),
              help="Model to use (local Ollama only)")
@click.option("--query", "-q", required=True, type=str)
@click.option("--threads", "-t", default=5, show_default=True, type=int)
@click.option("--output", "-o", type=str)
def cli(model, query, threads, output):
    """Command-line OSINT runner."""
    llm = get_llm(model)

    with yaspin(text="Processing...", color="cyan") as sp:
        refined = refine_query(llm, query)
        results = get_search_results(refined.replace(" ", "+"), max_workers=threads)
        filtered = filter_results(llm, refined, results)
        scraped = scrape_multiple(filtered, max_workers=threads)
        sp.ok("✔")

    summary = generate_summary(llm, query, scraped)

    if not output:
        filename = f"architect_ai_summary_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md"
    else:
        filename = f"{output}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(summary)

    click.echo(f"[OUTPUT] File saved: {filename}")

@architect_ai.command()
@click.option("--ui-port", default=8501, show_default=True, type=int)
@click.option("--ui-host", default="localhost", show_default=True, type=str)
def ui(ui_port, ui_host):
    """Launch the Streamlit UI."""
    from streamlit.web import cli as stcli

    base = os.path.dirname(os.path.abspath(__file__))
    ui_script = os.path.join(base, "ui.py")

    sys.argv = [
        "streamlit",
        "run",
        ui_script,
        f"--server.port={ui_port}",
        f"--server.address={ui_host}",
        "--global.developmentMode=false",
    ]

    sys.exit(stcli.main())

if __name__ == "__main__":
    architect_ai()
