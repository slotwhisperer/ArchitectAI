# main.py — ARCHITECT AI Launcher (2025)
# Run with: python main.py ui
# Or just: streamlit run app.py

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
@click.option(
    "--port", "-p",
    default=7860,
    show_default=True,
    type=int,
    help="Port for the web UI"
)
@click.option(
    "--host", "-h",
    default="127.0.0.1",
    show_default=True,
    type=str,
    help="Host address (use 0.0.0.0 for external access)"
)
@click.option(
    "--share",
    is_flag=True,
    help="Generate public share link (Streamlit Cloud style)"
)
def ui(port, host, share):
    """Launch ARCHITECT AI Web Interface"""
    click.echo("ARCHITECT AI — Starting secure interface...")
    click.echo("Monero Only • Escrow First • No Refunds")
    click.echo(f"Opening on http://{host}:{port}")

    # Find app.py in same folder
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ui_script = os.path.join(base_dir, "app.py")

    if not os.path.exists(ui_script):
        click.echo(f"Error: app.py not found in {base_dir}")
        click.echo("Make sure app.py is in the same folder as main.py")
        sys.exit(1)

    # Build Streamlit command
    args = [
        "streamlit", "run", ui_script,
        f"--server.port={port}",
        f"--server.address={host}",
        "--server.headless=true",
        "--global.developmentMode=false"
    ]

    if share:
        args.append("--server.enableCORS=false")
        args.append("--server.enableXsrfProtection=false")

    sys.argv = args
    sys.exit(stcli.main())

@architect.command()
def chat():
    """Quick terminal chat with ARCHITECT AI (unfiltered)"""
    import ollama
    click.echo("ARCHITECT AI — Unfiltered Terminal Mode")
    click.echo("Type 'exit' or Ctrl+C to quit\n")

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
            user_input = click.prompt("You", type=str)
            if user_input.lower() in ["exit", "quit", "bye"]:
                click.echo("ARCHITECT AI: Deal’s done.")
                break

            messages.append({"role": "user", "content": user_input})

            click.echo("ARCHITECT AI: Thinking...", nl=False)
            response = ollama.chat(model="architect", messages=messages)
            answer = response['message']['content']

            click.echo(f"\rARCHITECT AI: {answer}\n")
            messages.append({"role": "assistant", "content": answer})

        except KeyboardInterrupt:
            click.echo("\nARCHITECT AI: Session terminated.")
            break
        except Exception as e:
            click.echo(f"Error: {e}")

if __name__ == "__main__":
    architect()
