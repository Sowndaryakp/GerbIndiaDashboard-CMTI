import pdfkit

# Define input and output file paths
input_html_file = 'input.html'
output_pdf_file = 'output.pdf'

# Path to wkhtmltopdf executable (replace this with the actual path on your system)
wkhtmltopdf_path = '/path/to/wkhtmltopdf'

# Options for pdfkit (optional)
options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
}

# Convert HTML to PDF
pdfkit.from_file(input_html_file, output_pdf_file, options=options)
