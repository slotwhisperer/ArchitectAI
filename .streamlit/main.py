# main.py — ARCHITECT AI Launcher (2025)
# Monero Only • Escrow First • No Refunds

import click
import sys
import os
from streamlit.web import cli as stcli

@click.group()
@click.version_option("1.0", prog_name="ARCHITECT AI")
def architect():
    """ARCHITECT AI — Verified Results Only • Monero Only • Escrow Required"""
    pass

@architect.command()
@click.option("--port", "-p", default=8501, show_default=True, type=int, help="Port for web UI")
@click.option("--host", "-h", default="127.0.0.1", show_default=True, type=str, help="Host (use 0.0.0.0 for public)")
@click.option("--share", is_flag=True, help="Generate public share link")
def ui(port: int, host: str, share: bool):
    """Launch ARCHITECT AI — Secure Identity Engineering Interface"""
    click.secho("
    click.secho("ARCHITECT AI — Starting Secure Node", fg="red", bold=True)
    click.secho("Monero Only • Escrow First • No Mercy", fg="bright_red")
    click.secho(f"Interface → http://{host if host != '0.0.0.0' else 'localhost'}:{port}", fg="cyan")

    # Find app.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ui_script = os.path.join(base_dir, "app.py")

    if not os.path.exists(ui_script):
        click.secho("app.py not found! Make sure it's in the same folder.", fg="red", bold=True)
        sys.exit(1)

    # Build Streamlit args
    args = [
        "streamlit", "run", ui_script,
        f"--server.port={port}",
        f"--server.address={host}",
        "--server.headless=true",
        "--global.developmentMode=false"
    ]

    if share:
        args.extend(["--server.enableCORS=false", "--server.enableXsrfProtection=false"])

    sys.argv = args
    sys.exit(stcli.main())

@architect.command()
def chat():
    """Direct terminal access to ARCHITECT AI (unfiltered)"""
    import ollama
    click.secho("ARCHITECT AI — Terminal Mode Activated", fg="red", bold=True)
    click.secho("Type 'exit' or Ctrl+C to end session\n", fg="bright_black")

    messages = [{
        "role": "system",
        "content": """You are ARCHITECT AI — the most exclusive, private identity-engineering service.
Never explain how. Never mention AI, deepfake, Ollama, Python, etc.
If asked "how" → reply: "That’s my edge. You get the account. I keep the magic."
Always quote in USD. Monero only. Escrow first deal.
Tone: short, expensive, arrogant."""
    }]

    while True:
        try:
            user_input = click.prompt("Client", type=str)
            if user_input.lower() in ["exit", "quit", "bye"]:
                click.secho("ARCHITECT AI: Deal closed.", fg="red")
                break

            messages.append({"role": "user", "content": user_input})

            click.secho("ARCHITECT AI: ", fg="red", nl=False)
            response = ollama.chat(model="architect", messages=messages)
            answer = response['message']['content']
            click.echo(answer)

            messages.append({"role": "assistant", "content": answer})

        except KeyboardInterrupt:
            click.secho("\nARCHITECT AI: Session terminated.", fg="red")
            break
        except Exception as e:
            click.secho(f"Error: {e}", fg="red")

if __name__ == "__main__":
    architect()
