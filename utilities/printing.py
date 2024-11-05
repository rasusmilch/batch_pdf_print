import subprocess
from .log_util import *

def print_pdf_with_ghostscript(filename, printer=None):
    """
    Try printing with the Ghostscript library first. If it fails, fallback to using the Ghostscript subprocess command.
    """
    try:
        # Attempt to print using the Ghostscript Python library
        print_pdf_with_ghostscript_library(filename, printer)
    except (ImportError, RuntimeError) as e:
        # If there's an ImportError or RuntimeError, log it and try the subprocess method
        logger.warning(f"Failed using Ghostscript library: {e}. Falling back to subprocess method.")
        try:
            print_pdf_with_ghostscript_subprocess(filename, printer)
        except subprocess.CalledProcessError as e:
            if e.returncode == 1:  # Typically return code 1 indicates cancellation in Ghostscript
                logger.warning(f"Print job {filename} was canceled by the user.")
            else:
                log_error(f"Failed to print {filename} using subprocess method: {e}")
                raise

def print_pdf_with_ghostscript_library(filename, printer=None):
    try:
        import ghostscript  # Import the ghostscript module inside the try block
        args = [
            "gs",
            "-dNOPAUSE",
            "-dBATCH",
            "-dSAFER",
            "-sDEVICE=mswinpr2"
        ]

        # If a printer is specified, append it to the output file command
        if printer:
            args.append(f"-sOutputFile=%printer%{printer}")
        else:
            args.append("-sOutputFile=%printer%")

        args.append(filename)

        ghostscript.Ghostscript(*args)
        logger.info(f"Printed {filename} successfully using Ghostscript library.")
    except ImportError as e:
        logger.error(f"Ghostscript library not installed: {e}")
        raise
    except RuntimeError as e:
        logger.error(f"Error using Ghostscript library: {e}")
        raise

def print_pdf_with_ghostscript_subprocess(filename, printer=None):
    """
    @brief Sends a PDF file to the specified printer or the default printer using Ghostscript subprocess.

    If a printer is specified, it appends the printer name to the Ghostscript command. 
    Otherwise, it defaults to showing the system print dialog.

    @param filename The path to the PDF file to print.
    @param printer Optional; the name of the printer to which the file should be printed.
    """
    ghostscript_command = [
        "gswin64c",
        "-dNOPAUSE",
        "-dBATCH",
        "-dSAFER",
        "-sDEVICE=mswinpr2"
    ]

    # If a printer is specified, append it to the output file command
    if printer:
        ghostscript_command.append(f"-sOutputFile=%printer%{printer}")
    else:
        ghostscript_command.append("-sOutputFile=%printer%")

    ghostscript_command.append(filename)

    try:
        subprocess.run(ghostscript_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        logger.info(f"Printed {filename} successfully using Ghostscript subprocess.")
    except subprocess.CalledProcessError as e:
        # Check if the error is due to the user canceling the print job
        if e.returncode == 1:
            logger.warning(f"Print job {filename} was canceled by the user.")
        else:
            log_error(f"Error printing the file {filename} using Ghostscript subprocess: {e}")
            raise

def merge_pdfs_with_ghostscript(pdf_files, output_file):
    """
    Merges multiple PDF files into a single PDF using the Ghostscript library or falls back to subprocess if unavailable.
    
    Args:
        pdf_files (list of str): List of paths to PDF files to merge.
        output_file (str): The path to the output merged PDF file.
    """
    try:
        merge_pdfs_with_ghostscript_library(pdf_files, output_file)
    except (ImportError, RuntimeError) as e:
        logger.warning(f"Failed to merge PDFs using Ghostscript library: {e}. Falling back to subprocess method.")
        try:
            merge_pdfs_with_ghostscript_subprocess(pdf_files, output_file)
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to merge PDFs using Ghostscript subprocess method: {e}")
            raise

def merge_pdfs_with_ghostscript_library(pdf_files, output_file):
    """
    Attempts to merge PDFs using the Ghostscript Python library.

    Args:
        pdf_files (list of str): List of paths to PDF files to merge.
        output_file (str): The path to the output merged PDF file.
    """
    try:
        import ghostscript  # Import ghostscript within the function
        args = [
            "gs",
            "-dBATCH",
            "-dNOPAUSE",
            "-q",
            "-sDEVICE=pdfwrite",
            f"-sOutputFile={output_file}"
        ] + pdf_files

        ghostscript.Ghostscript(*args)
        logger.info(f"Merged PDFs into '{output_file}' successfully using Ghostscript library.")
    except ImportError as e:
        logger.error(f"Ghostscript library not installed: {e}")
        raise
    except RuntimeError as e:
        logger.error(f"Error using Ghostscript library: {e}")
        raise

def merge_pdfs_with_ghostscript_subprocess(pdf_files, output_file):
    """
    Merges multiple PDF files into a single PDF using Ghostscript via subprocess.
    
    Args:
        pdf_files (list of str): List of paths to PDF files to merge.
        output_file (str): The path to the output merged PDF file.
    """
    gs_command = [
        "gs",
        "-dBATCH",
        "-dNOPAUSE",
        "-q",
        "-sDEVICE=pdfwrite",
        f"-sOutputFile={output_file}"
    ] + pdf_files

    try:
        subprocess.run(gs_command, check=True)
        logger.info(f"Merged PDFs into '{output_file}' successfully using Ghostscript subprocess.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to merge PDFs using Ghostscript subprocess: {e}")
        raise