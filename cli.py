"""
Legal Case AI - Professional CLI Interface
============================================

Enterprise-grade command-line interface with rich terminal output,
progress tracking, and comprehensive extraction capabilities.
"""

from __future__ import annotations

import json
import logging
import sys
import warnings
from pathlib import Path
from typing import Optional, List

# Suppress annoying Pydantic V1/Py3.14 warnings
warnings.filterwarnings("ignore", category=UserWarning, module="confection")
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

try:
    import typer
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.syntax import Syntax
    from rich.tree import Tree
    from rich import print as rprint
    HAS_CLI_DEPS = True
except ImportError:
    HAS_CLI_DEPS = False

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Settings, get_settings, ExtractionMode
from src.extractor import HybridExtractor, create_extractor
from src.models import CaseMetadata


# =============================================================================
# CLI SETUP
# =============================================================================

if HAS_CLI_DEPS:
    # Force UTF-8 encoding on Windows
    import os
    if sys.platform == 'win32':
        os.system('')  # Enable VT100 escape sequences
    
    app = typer.Typer(
        name="legal-case-ai",
        help="Enterprise-grade AI-powered Legal Case Metadata Extraction System",
        add_completion=False,
        rich_markup_mode="rich",
    )
    console = Console(force_terminal=True)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def display_header():
    """Display application header."""
    header = """
[bold blue]+====================================================================+[/]
[bold blue]|[/]         [bold white]LEGAL CASE AI[/] - Metadata Extraction System           [bold blue]|[/]
[bold blue]|[/]         [dim]Enterprise Edition v1.0.0[/]                              [bold blue]|[/]
[bold blue]+====================================================================+[/]
"""
    console.print(header)


def display_metadata(metadata: CaseMetadata, show_confidence: bool = True):
    """Display extracted metadata in a rich format."""
    # Case Identity Panel
    identity_table = Table(show_header=False, box=None, padding=(0, 2))
    identity_table.add_column("Field", style="cyan")
    identity_table.add_column("Value", style="white")
    
    identity_table.add_row("Case Name", metadata.case_name or "[dim]Not found[/]")
    identity_table.add_row("Court", metadata.court_name or "[dim]Not found[/]")
    identity_table.add_row("Jurisdiction", str(metadata.jurisdiction_level.value) if metadata.jurisdiction_level else "[dim]Not found[/]")
    identity_table.add_row("Date Decided", str(metadata.date_decided) if metadata.date_decided else "[dim]Not found[/]")
    
    if metadata.citation:
        identity_table.add_row("Citation", metadata.citation.full_citation)
    
    console.print(Panel(identity_table, title="[bold]Case Identity[/]", border_style="blue"))
    
    # Parties Panel
    if metadata.plaintiffs or metadata.defendants:
        parties_table = Table(show_header=True, header_style="bold")
        parties_table.add_column("Role", style="cyan")
        parties_table.add_column("Name", style="white")
        parties_table.add_column("Type", style="dim")
        
        for p in metadata.plaintiffs:
            parties_table.add_row("Plaintiff", p.name, p.type.value if hasattr(p.type, 'value') else str(p.type))
        for d in metadata.defendants:
            parties_table.add_row("Defendant", d.name, d.type.value if hasattr(d.type, 'value') else str(d.type))
        
        console.print(Panel(parties_table, title="[bold]Parties[/]", border_style="green"))
    
    # Judges Panel
    if metadata.judges:
        judges_text = ", ".join(metadata.judges)
        if metadata.author_judge:
            judges_text += f" [dim](Opinion by: {metadata.author_judge})[/]"
        console.print(Panel(judges_text, title="[bold]Judges[/]", border_style="yellow"))
    
    # Subject Matter Panel
    subject_table = Table(show_header=False, box=None, padding=(0, 2))
    subject_table.add_column("Field", style="cyan")
    subject_table.add_column("Value", style="white")
    
    if metadata.primary_topic:
        subject_table.add_row("Primary Topic", metadata.primary_topic)
    if metadata.specific_cause_of_action:
        subject_table.add_row("Cause of Action", metadata.specific_cause_of_action)
    if metadata.industry_sector:
        subject_table.add_row("Industry", metadata.industry_sector)
    
    if metadata.primary_topic or metadata.specific_cause_of_action:
        console.print(Panel(subject_table, title="[bold]Subject Matter[/]", border_style="magenta"))
    
    # Outcome Panel
    outcome_table = Table(show_header=False, box=None, padding=(0, 2))
    outcome_table.add_column("Field", style="cyan")
    outcome_table.add_column("Value", style="white")
    
    if metadata.procedural_posture:
        outcome_table.add_row("Procedural Posture", metadata.procedural_posture)
    if metadata.disposition:
        disp = metadata.disposition.value if hasattr(metadata.disposition, 'value') else str(metadata.disposition)
        outcome_table.add_row("Disposition", f"[bold]{disp}[/]")
    if metadata.prevailing_party:
        pp = metadata.prevailing_party.value if hasattr(metadata.prevailing_party, 'value') else str(metadata.prevailing_party)
        outcome_table.add_row("Prevailing Party", pp)
    if metadata.monetary_damages:
        outcome_table.add_row("Damages", f"${metadata.monetary_damages:,.2f}")
    
    if metadata.disposition or metadata.procedural_posture:
        console.print(Panel(outcome_table, title="[bold]Outcome[/]", border_style="red"))
    
    # Evidence Panel
    if metadata.evidence_types:
        evidence_list = ", ".join([e.value if hasattr(e, 'value') else str(e) for e in metadata.evidence_types])
        console.print(Panel(evidence_list, title="[bold]Evidence Types[/]", border_style="cyan"))
    
    # Taxonomy Panel (Hierarchical Classifications)
    if hasattr(metadata, 'topic_taxonomy') and metadata.topic_taxonomy:
        tax_table = Table(show_header=False, box=None, padding=(0, 2))
        tax_table.add_column("Level", style="dim", width=15)
        tax_table.add_column("Classification", style="white")
        
        # Topic taxonomy path
        topic = metadata.topic_taxonomy
        tax_table.add_row("Domain", f"[bold cyan]{topic.domain}[/]")
        if topic.area:
            tax_table.add_row("  Area", f"[cyan]{topic.area}[/]")
        if topic.specific:
            tax_table.add_row("    Specific", f"[dim cyan]{topic.specific}[/]")
        
        # Show industry if available
        if hasattr(metadata, 'industry_taxonomy') and metadata.industry_taxonomy:
            ind = metadata.industry_taxonomy
            tax_table.add_row("Industry", f"[yellow]{ind.domain}[/]" + (f" > {ind.area}" if ind.area else ""))
        
        # Show procedural stage if available
        if hasattr(metadata, 'procedural_taxonomy') and metadata.procedural_taxonomy:
            proc = metadata.procedural_taxonomy
            proc_path = proc.stage
            if proc.type:
                proc_path += f" > {proc.type}"
            tax_table.add_row("Procedure", f"[magenta]{proc_path}[/]")
        
        # Show group ID
        if hasattr(metadata, 'group_id') and metadata.group_id:
            tax_table.add_row("Group ID", f"[dim]{metadata.group_id}[/]")
        
        console.print(Panel(tax_table, title="[bold]Taxonomy Classification[/]", border_style="blue"))
    
    # All topic matches
    if hasattr(metadata, 'all_topic_taxonomies') and metadata.all_topic_taxonomies and len(metadata.all_topic_taxonomies) > 1:
        topics_list = []
        for t in metadata.all_topic_taxonomies[:5]:
            path = t.domain
            if t.area:
                path += f" > {t.area}"
            if t.specific:
                path += f" > {t.specific}"
            topics_list.append(f"[dim]-[/] {path}")
        console.print(Panel("\n".join(topics_list), title="[bold]All Detected Topics[/]", border_style="dim blue"))
    
    # Nearest Examples (Precedents) Panel
    if hasattr(metadata, 'similar_cases') and metadata.similar_cases:
        sim_table = Table(show_header=True, box=None, padding=(0, 2), title_style="bold")
        sim_table.add_column("Match", style="bold green", justify="right", width=8)
        sim_table.add_column("Case Precedent", style="cyan")
        sim_table.add_column("Context", style="white")
        
        for case in metadata.similar_cases[:3]:
            sim_table.add_row(
                f"{case.similarity_score:.0%}",
                f"[bold]{case.case_name}[/]\n[dim]{case.date}[/]",
                f"[yellow]{case.category}[/]\n{case.summary[:100]}..."
            )
            sim_table.add_section()
            
        console.print(Panel(sim_table, title="[bold]Nearest Examples (2000-2024)[/]", border_style="green"))

    # Confidence Panel
    if show_confidence and metadata.confidence:
        conf = metadata.confidence
        conf_table = Table(show_header=False, box=None)
        conf_table.add_column("Metric", style="dim")
        conf_table.add_column("Score", justify="right")
        
        def score_color(score: float) -> str:
            if score >= 0.8:
                return "green"
            elif score >= 0.5:
                return "yellow"
            return "red"
        
        conf_table.add_row("Overall", f"[{score_color(conf.overall)}]{conf.overall:.0%}[/]")
        conf_table.add_row("Case Identity", f"[{score_color(conf.case_identity)}]{conf.case_identity:.0%}[/]")
        conf_table.add_row("Parties", f"[{score_color(conf.parties)}]{conf.parties:.0%}[/]")
        conf_table.add_row("Subject Matter", f"[{score_color(conf.subject_matter)}]{conf.subject_matter:.0%}[/]")
        conf_table.add_row("Outcome", f"[{score_color(conf.outcome)}]{conf.outcome:.0%}[/]")
        
        console.print(Panel(conf_table, title="[bold]Confidence Scores[/]", border_style="dim"))


# =============================================================================
# CLI COMMANDS
# =============================================================================

if HAS_CLI_DEPS:
    
    @app.command("extract")
    def extract_command(
        file: Path = typer.Argument(..., help="Path to case file (.txt)"),
        output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output JSON file"),
        format: str = typer.Option("rich", "--format", "-f", help="Output format: rich, json, compact"),
        mode: str = typer.Option("hybrid", "--mode", "-m", help="Extraction mode: hybrid, llm_only, regex_only"),
    ):
        """
        Extract metadata from a court case file.
        
        Examples:
            legal-case-ai extract case.txt
            legal-case-ai extract case.txt -o result.json
            legal-case-ai extract case.txt --format json
        """
        display_header()
        
        if not file.exists():
            console.print(f"[red]Error:[/] File not found: {file}")
            raise typer.Exit(1)
        
        # Load file
        console.print(f"[dim]Loading:[/] {file}")
        text = file.read_text(encoding='utf-8')
        console.print(f"[dim]Size:[/] {len(text):,} characters")
        
        # Create extractor
        settings = get_settings()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Extracting metadata...", total=None)
            
            extractor = create_extractor(settings)
            result = extractor.extract(text)
        
        if not result.success:
            console.print(f"[red]Extraction failed:[/] {result.error}")
            raise typer.Exit(1)
        
        metadata = result.metadata
        console.print(f"[green][OK][/] Extraction complete in {result.processing_time_ms:.0f}ms")
        console.print()
        
        # Display output
        if format == "json":
            syntax = Syntax(metadata.to_json(), "json", theme="monokai", line_numbers=True)
            console.print(syntax)
        elif format == "compact":
            console.print(json.dumps(metadata.to_compact_dict(), indent=2))
        else:
            display_metadata(metadata)
        
        # Save to file if requested
        if output:
            output.write_text(metadata.to_json())
            console.print(f"\n[green][OK][/] Saved to: {output}")
    
    
    @app.command("batch")
    def batch_command(
        directory: Path = typer.Argument(..., help="Directory containing case files"),
        output: Path = typer.Option(Path("results"), "--output", "-o", help="Output directory"),
        pattern: str = typer.Option("*.txt", "--pattern", "-p", help="File pattern to match"),
    ):
        """
        Batch process multiple case files.
        
        Examples:
            legal-case-ai batch ./cases/
            legal-case-ai batch ./cases/ -o ./results/ -p "*.txt"
        """
        display_header()
        
        if not directory.is_dir():
            console.print(f"[red]Error:[/] Not a directory: {directory}")
            raise typer.Exit(1)
        
        files = list(directory.glob(pattern))
        if not files:
            console.print(f"[yellow]Warning:[/] No files matching '{pattern}' in {directory}")
            raise typer.Exit(0)
        
        console.print(f"[dim]Found {len(files)} files to process[/]")
        
        output.mkdir(parents=True, exist_ok=True)
        
        extractor = create_extractor()
        
        successful = 0
        failed = 0
        
        with Progress(console=console) as progress:
            task = progress.add_task("Processing files...", total=len(files))
            
            for file in files:
                try:
                    text = file.read_text(encoding='utf-8')
                    result = extractor.extract(text)
                    
                    if result.success:
                        output_file = output / f"{file.stem}.json"
                        output_file.write_text(result.metadata.to_json())
                        successful += 1
                    else:
                        failed += 1
                        console.print(f"[red][FAIL][/] {file.name}: {result.error}")
                        
                except Exception as e:
                    failed += 1
                    console.print(f"[red][FAIL][/] {file.name}: {e}")
                
                progress.update(task, advance=1)
        
        console.print()
        console.print(f"[green][OK] Successful:[/] {successful}")
        console.print(f"[red][FAIL] Failed:[/] {failed}")
        console.print(f"[dim]Output directory:[/] {output}")
    
    
    @app.command("config")
    def config_command(
        show: bool = typer.Option(True, "--show", help="Show current configuration"),
    ):
        """
        Display current configuration.
        """
        display_header()
        
        settings = get_settings()
        
        config_table = Table(title="Configuration", show_header=True)
        config_table.add_column("Setting", style="cyan")
        config_table.add_column("Value", style="white")
        
        # API Status
        api_status = settings.validate_api_keys()
        gemini_status = "[green][OK] Configured[/]" if api_status['gemini'] else "[red][X] Not set[/]"
        
        config_table.add_row("Gemini API", gemini_status)
        config_table.add_row("Extraction Mode", settings.extraction_mode.value)
        config_table.add_row("Effective Mode", settings.effective_mode.value)
        config_table.add_row("Gemini Model", settings.gemini_model)
        config_table.add_row("Confidence Threshold", f"{settings.llm_confidence_threshold:.0%}")
        config_table.add_row("Cache Enabled", str(settings.enable_cache))
        config_table.add_row("Log Level", settings.log_level.value)
        
        console.print(config_table)
        
        console.print()
        console.print("[dim]To configure, create a .env file from .env.example[/]")
    
    
    @app.command("demo")
    def demo_command():
        """
        Run a demonstration extraction on sample text.
        """
        display_header()
        
        sample_text = """
UNITED STATES COURT OF APPEALS FOR THE NINTH CIRCUIT

No. 19-55977

APPLE INC., a California corporation,
                                    Plaintiff-Appellant,
    v.

QUALCOMM INC., a Delaware corporation,
                                    Defendant-Appellee.

Appeal from the United States District Court for the
Southern District of California
D.C. No. 3:17-cv-00108-GPC-MDD

Filed March 15, 2020

Before: NGUYEN, HURWITZ, and CHRISTEN, Circuit Judges.

NGUYEN, Circuit Judge:

This case involves a complex dispute over patent licensing practices 
in the telecommunications industry. Apple Inc. brought this action 
against Qualcomm Inc. alleging antitrust violations and seeking damages 
of $15 million for alleged overcharges on chip royalties.

Apple contends that Qualcomm engaged in anticompetitive conduct by 
conditioning the sale of chips on patent license agreements.

Theodore J. Boutrous Jr., Gibson, Dunn & Crutcher LLP, argued for 
plaintiff-appellant Apple Inc.

The District Court granted summary judgment in favor of Qualcomm.

After reviewing the record and the documentary evidence, we find that 
the District Court properly analyzed the relevant market.

For the foregoing reasons, the judgment of the District Court is 
AFFIRMED.
"""
        
        console.print("[dim]Running demo extraction on sample case...[/]")
        console.print()
        
        extractor = create_extractor()
        result = extractor.extract(sample_text)
        
        if result.success:
            console.print(f"[green][OK][/] Extraction complete in {result.processing_time_ms:.0f}ms")
            console.print()
            display_metadata(result.metadata)
        else:
            console.print(f"[red]Extraction failed:[/] {result.error}")


    @app.command("set-model")
    def set_model_command(model_path: str = typer.Argument(..., help="Path to the trained model folder or zip")):
        """
        Configure the system to use a specific NER model (e.g., from cloud training).
        """
        display_header()
        
        # Verify path
        path_obj = Path(model_path)
        if not path_obj.exists():
            console.print(f"[red]Error:[/] Model path not found: {model_path}")
            # Check if it is in models dir
            alt_path = Path("models") / model_path
            if alt_path.exists():
                model_path = str(alt_path)
                console.print(f"[yellow]Found in models directory:[/] Using {model_path}")
            else:
                return

        # Update .env file
        env_path = Path(".env")
        lines = []
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        
        # Remove existing NER_MODEL_PATH
        lines = [l for l in lines if not l.startswith("NER_MODEL_PATH=")]
        
        # Add new path
        lines.append(f"\nNER_MODEL_PATH={model_path}\n")
        
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
            
        console.print(f"[green]Successfully configured model:[/] {model_path}")
        console.print("Future extractions will use this model.")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main entry point."""
    if not HAS_CLI_DEPS:
        print("CLI dependencies not installed. Run: pip install typer rich")
        print("\nFalling back to basic extraction...")
        
        from src.extractor import RegexExtractor
        
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            extractor = RegexExtractor()
            result = extractor.extract(text)
            print(json.dumps(result, indent=2, default=str))
        else:
            print("Usage: python cli.py <case_file.txt>")
        return
    
    app()


if __name__ == "__main__":
    main()
