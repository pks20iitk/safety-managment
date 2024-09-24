"""
pdf_highlighter.py

This module provides functionality to highlight specific paragraphs in PDF documents.
It uses the PyMuPDF library to manipulate PDF files and add highlight annotations.
"""

import os
import logging
import fitz  # PyMuPDF

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def highlight_paragraphs_in_pdfs(pdf_folder_path, pdf_filenames, paragraphs, page_numbers, output_folder_path):
    """
    Highlights specified paragraphs in a list of PDF files.

    Args:
        pdf_folder_path (str): Path to the folder containing input PDF files.
        pdf_filenames (list): List of PDF filenames to process.
        paragraphs (list): List of paragraphs to highlight.
        page_numbers (list): List of page numbers corresponding to each paragraph.
        output_folder_path (str): Path to the folder where output PDFs will be saved.

    Returns:
        list: List of paths to the output PDF files with highlighted paragraphs.
    """
    logger.info("Starting the highlight_paragraphs_in_pdfs function")
    output_pdf_paths = []
    current_pdf_path = None
    current_pdf_document = None

    try:
        for paragraph, page_number, filename in zip(paragraphs, page_numbers, pdf_filenames):
            input_pdf_path = os.path.join(pdf_folder_path, filename)

            # Check if the PDF document has changed or if it's the first iteration
            if current_pdf_path != input_pdf_path:
                if current_pdf_document:
                    logger.info("Saving and closing previous PDF document")
                    current_pdf_document.save(current_pdf_output_path)
                    current_pdf_document.close()
                    output_pdf_paths.append(current_pdf_output_path)

                logger.info("Opening new PDF document")
                current_pdf_document = fitz.open(input_pdf_path)
                current_pdf_output_path = os.path.join(output_folder_path, filename)
                current_pdf_path = input_pdf_path

            page_number = int(page_number) - 1  # Adjust for zero-based index

            # Ensure the specified page number is within the document range
            if 0 <= page_number < current_pdf_document.page_count:
                logger.info(f"Highlighting paragraph on page {page_number + 1} of {filename}")
                page = current_pdf_document[page_number]
                highlight_paragraph(page, paragraph)
            else:
                logger.warning(f"Page number {page_number + 1} is out of range for {filename}.")

        # Save and close the last PDF document
        if current_pdf_document:
            logger.info("Saving and closing last PDF document")
            current_pdf_document.save(current_pdf_output_path)
            current_pdf_document.close()
            output_pdf_paths.append(current_pdf_output_path)

        logger.info("Finished highlighting paragraphs in PDFs")
        return output_pdf_paths

    except Exception as e:
        logger.error(f"Error in highlight_paragraphs_in_pdfs function: {e}")
        return []

def highlight_paragraph(page, paragraph):
    """
    Highlights the specified paragraph on the given page.

    Args:
        page (fitz.Page): The page object where the paragraph will be highlighted.
        paragraph (str): The paragraph text to highlight.

    Returns:
        None
    """
    text_instances = page.search_for(paragraph)
    for inst in text_instances:
        if isinstance(inst, fitz.Rect):
            highlight = page.add_highlight_annot(inst)
            highlight.set_colors(stroke=(1, 1, 0))  # Set the color to yellow (R, G, B)
            highlight.update()  # Apply the highlight
        else:
            logger.warning("Invalid rect data for highlighting. Skipping annotation.")