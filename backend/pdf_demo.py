import os
import datetime as dt
import re
from pathlib import Path

# Import PDF generation libraries
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def save_transcript_to_pdf(video_data):
    """
    Save the transcript of a YouTube video to a PDF file.
    
    Args:
        video_data (dict): Dictionary containing video information including transcript
    
    Returns:
        str: Path to the saved PDF file or None if saving failed
    """
    try:
        # Create transcripts directory if it doesn't exist
        transcripts_dir = Path(os.path.join(os.path.dirname(__file__), '..', 'transcripts'))
        transcripts_dir.mkdir(exist_ok=True)
        
        # Extract video information
        video_id = video_data.get('video_id', 'unknown')
        title = video_data.get('title', 'Untitled')
        
        # Clean the title to make it suitable for a filename
        clean_title = re.sub(r'[\\/*?:"<>|]', '', title)  # Remove invalid filename characters
        clean_title = re.sub(r'\s+', '_', clean_title)    # Replace spaces with underscores
        
        # Create a timestamp
        timestamp = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create the filename
        filename = f"{clean_title}-{timestamp}-{video_id}.pdf"
        filepath = transcripts_dir / filename
        
        # Get the transcript text
        transcript_text = video_data.get('transcript_text', '')
        
        if not transcript_text:
            print(f"No transcript available for video: {title} ({video_id})")
            return None
        
        # Create a PDF document
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        heading_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Create document elements
        elements = []
        
        # Add title
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Add metadata table
        metadata = [
            ["Video ID:", video_id],
            ["URL:", video_data.get('url', '')],
            ["Channel:", video_data.get('channel_name', '')],
            ["Upload Date:", video_data.get('upload_date', '')],
            ["Duration:", f"{video_data.get('duration_seconds', 0)} seconds"]
        ]
        
        # Create the table with metadata
        metadata_table = Table(metadata, colWidths=[1.5*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(metadata_table)
        elements.append(Spacer(1, 0.5 * inch))
        
        # Add transcript heading
        elements.append(Paragraph("TRANSCRIPT", heading_style))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Add transcript text - split into paragraphs for better formatting
        paragraphs = transcript_text.split('\n\n')
        for para in paragraphs:
            if para.strip():
                elements.append(Paragraph(para.replace('\n', '<br/>'), normal_style))
                elements.append(Spacer(1, 0.1 * inch))
        
        # Build the PDF
        doc.build(elements)
        
        print(f"Transcript PDF saved to: {filepath}")
        return str(filepath)
        
    except Exception as e:
        print(f"Error saving transcript to PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def save_transcript_to_file(video_data):
    """
    Save the transcript of a YouTube video to a text file.
    
    Args:
        video_data (dict): Dictionary containing video information including transcript
    
    Returns:
        str: Path to the saved transcript file or None if saving failed
    """
    try:
        # Create transcripts directory if it doesn't exist
        transcripts_dir = Path(os.path.join(os.path.dirname(__file__), '..', 'transcripts'))
        transcripts_dir.mkdir(exist_ok=True)
        
        # Extract video information
        video_id = video_data.get('video_id', 'unknown')
        title = video_data.get('title', 'Untitled')
        
        # Clean the title to make it suitable for a filename
        clean_title = re.sub(r'[\\/*?:"<>|]', '', title)  # Remove invalid filename characters
        clean_title = re.sub(r'\s+', '_', clean_title)    # Replace spaces with underscores
        
        # Create a timestamp
        timestamp = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create the filename
        filename = f"{clean_title}-{timestamp}-{video_id}.txt"
        filepath = transcripts_dir / filename
        
        # Get the transcript text
        transcript_text = video_data.get('transcript_text', '')
        
        if not transcript_text:
            print(f"No transcript available for video: {title} ({video_id})")
            return None
        
        # Write the transcript to the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\n")
            f.write(f"Video ID: {video_id}\n")
            f.write(f"URL: {video_data.get('url', '')}\n")
            f.write(f"Channel: {video_data.get('channel_name', '')}\n")
            f.write(f"Upload Date: {video_data.get('upload_date', '')}\n")
            f.write(f"Duration: {video_data.get('duration_seconds', 0)} seconds\n")
            f.write("\n" + "="*50 + "\n\nTRANSCRIPT:\n\n" + "="*50 + "\n\n")
            f.write(transcript_text)
        
        print(f"Transcript saved to: {filepath}")
        return str(filepath)
        
    except Exception as e:
        print(f"Error saving transcript: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Test the PDF generation with a sample video data
    sample_video_data = {
        "video_id": "sample123",
        "title": "Sample Video Title",
        "channel_name": "Sample Channel",
        "channel_id": "UC123456789",
        "upload_date": "2023-05-09",
        "url": "https://www.youtube.com/watch?v=sample123",
        "language": "en",
        "duration_seconds": 300,
        "transcript_text": "This is a sample transcript.\n\nIt has multiple paragraphs.\n\nEach paragraph will be formatted nicely in the PDF."
    }
    
    # Save to text file
    text_file_path = save_transcript_to_file(sample_video_data)
    print(f"Text file saved to: {text_file_path}")
    
    # Save to PDF file
    pdf_file_path = save_transcript_to_pdf(sample_video_data)
    print(f"PDF file saved to: {pdf_file_path}")
