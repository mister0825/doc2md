"""Program to convert PDF, HTML and other document formats to
markdown format using the Docling library with CLI-based menu system and file naming"""

from docling.document_converter import DocumentConverter
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
import os
import re

def display_menu():
    """Display the main menu with 4 options"""
    console = Console()
    console.print(Panel.fit(
        "[bold blue]URL to Markdown Converter[/bold blue]",
        border_style="blue"
    ))
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Option", style="cyan", width=6)
    table.add_column("Action", style="white")
    
    table.add_row("1", "Enter URL")
    table.add_row("2", "Enter local file path")
    table.add_row("3", "Help")
    table.add_row("4", "Exit")
    
    console.print(table)
    console.print("\n")


def get_url_input():
    """Get and validate URL input from user"""
    console = Console()
    url = input("Enter the URL of the document to convert: ").strip()
    
    if not url:
        console.print("[bold red]Error: Please enter a valid URL for the document.[/bold red]")
        return None
    
    # Basic URL validation
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not url_pattern.match(url):
        console.print("[bold red]Error: Please enter a valid URL (e.g., https://example.com/document.pdf)[/bold red]")
        return None
    
    return url


def get_local_file_input():
    """Get and validate local file input from user"""
    console = Console()
    file_path = input("Enter the path to the local file: ").strip()
    
    if not file_path:
        console.print("[bold red]Error: Please enter a file path.[/bold red]")
        return None
    
    # Check if file exists
    if not os.path.exists(file_path):
        console.print(f"[bold red]Error: File not found: {file_path}[/bold red]")
        return None
    
    # Check if file is readable
    if not os.access(file_path, os.R_OK):
        console.print(f"[bold red]Error: File is not readable: {file_path}[/bold red]")
        return None
    
    # Check for compatible file extensions
    compatible_extensions = {'.pdf', '.html', '.htm', '.docx', '.doc', '.txt', '.md'}
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext not in compatible_extensions:
        console.print(f"[bold yellow]Warning: File extension '{file_ext}' may not be fully supported. Proceeding anyway...[/bold yellow]")
    
    return file_path


def get_output_filename():
    """Prompt user for output filename with default"""
    console = Console()
    filename = input("Enter output filename (default: converted_doc.md): ").strip()
    
    if not filename:
        return "converted_doc.md"
    
    # Ensure .md extension
    if not filename.endswith('.md'):
        filename += '.md'
    
    return filename


def show_help():
    """Display help information"""
    console = Console()
    console.print("\n")
    console.print(Panel.fit(
        "[bold green]Help - URL to Markdown Converter[/bold green]",
        border_style="green"
    ))
    
    help_table = Table(show_header=True, header_style="bold magenta")
    help_table.add_column("Feature", style="cyan", width=20)
    help_table.add_column("Description", style="white")
    
    help_table.add_row("URL Input", "Convert documents from web URLs")
    help_table.add_row("Local File", "Convert documents from local files")
    help_table.add_row("Supported Formats", "PDF, HTML, DOCX, TXT, MD")
    help_table.add_row("Output", "Markdown format with UTF-8 encoding")
    help_table.add_row("File Naming", "Custom filename or use default")
    
    console.print(help_table)
    console.print("\n")


def exit_program():
    """Exit the program gracefully"""
    console = Console()
    console.print("\n")
    console.print(Panel.fit(
        "[bold blue]Thank you for using URL to Markdown Converter![/bold blue]",
        border_style="blue"
    ))
    console.print("\n")


def convert_document(source, source_type):
    """Convert a document and display/save the result"""
    console = Console()
    converter = DocumentConverter()
    
    try:
        with console.status("[bold green]Processing document...") as status:
            result = converter.convert(source)
            markdown_content = result.document.export_to_markdown()
            console.print("[bold green]Conversion completed successfully.[/bold green]")
        
        # Render Markdown in terminal
        console.print("\n--- Converted Content ---\n")
        console.print(Markdown(markdown_content))
        console.print("\n--------------------------\n")
        
        # Get output filename
        output_file = get_output_filename()
        
        # Save to file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        console.print(f"[bold green]Content saved to [italic]{output_file}[/italic][/bold green]")
        return True
        
    except RuntimeError as e:
        console.print(f"[bold red]Error converting document:[/bold red] {e}")
        return False
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")
        return False


def main():
    """Main program loop with menu system"""
    console = Console()
    console.print("This tool uses Docling to convert various document formats into Markdown format.\n")
    
    while True:
        display_menu()
        
        try:
            choice = input("Select an option (1-4): ").strip()
            
            if choice == "1":
                # URL Input
                url = get_url_input()
                if url:
                    convert_document(url, "URL")
            
            elif choice == "2":
                # Local File Input
                file_path = get_local_file_input()
                if file_path:
                    convert_document(file_path, "Local File")
            
            elif choice == "3":
                # Help
                show_help()
            
            elif choice == "4":
                # Exit
                exit_program()
                break
            
            else:
                console.print("[bold red]Invalid option. Please enter a number between 1 and 4.[/bold red]")
            
            # Pause before showing menu again
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Program interrupted by user.[/bold yellow]")
            exit_program()
            break
        except Exception as e:
            console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
