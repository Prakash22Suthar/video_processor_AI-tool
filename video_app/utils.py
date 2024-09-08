from moviepy.editor import VideoFileClip

import speech_recognition as sr

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def extract_audio(video_path, audio_path):

    """this function will get audio form video file"""

    print(" :::::::::::::::: extracting audio start ::::::::::::::")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    print(" :::::::::::::::: extracting audio completed ::::::::::::::")


def audio_to_text(audio_path):
    """this function will get text form audio file"""

    print(" :::::::::::::::: audio to text converting ::::::::::::::")
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)

    print(" :::::::::::::::: audio to text converted ::::::::::::::")
    return text


def text_to_pdf(title, text, pdf_path):

    """Generate a PDF file with a custom title and text."""

    print(" :::::::::::::::: pdf generating ::::::::::::::")
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, 750, title)  # Adjust y position based on your title placement  # noqa

    # Text content
    c.setFont("Helvetica", 12)

    width, _ = letter
    lines = []
    current_line = ''

    # Split the text into lines based on logical breakpoints
    words = text.split()
    for word in words:
        if c.stringWidth(current_line + ' ' + word) < (width - 80):
            current_line += ' ' + word
        else:
            lines.append(current_line.strip())
            current_line = word

    # Append the last line
    if current_line:
        lines.append(current_line.strip())

    # Draw the lines on the PDF
    y = 700  # Starting y position for the text content
    for line in lines:
        c.drawString(40, y, line)
        y -= 20  # Adjust line spacing as needed

    c.save()
    print(" :::::::::::::::: pdf generated ::::::::::::::")

# def text_to_pdf(text, pdf_path):
#     """this function will generate/create pdf file by extracted text from audio"""  # noqa
#     c = canvas.Canvas(pdf_path, pagesize=letter)

#     width, height = letter
#     lines = text.split('\n')
#     y = height - 40
#     for line in lines:
#         c.drawString(40, y, line)
#         y -= 20
#     c.save()
