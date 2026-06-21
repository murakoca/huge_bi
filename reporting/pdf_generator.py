import pdfkit
from jinja2 import Environment, FileSystemLoader
import os

class PDFReportGenerator:
    def __init__(self, template_dir='reporting/templates'):
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def generate(self, data, output_path='report.pdf'):
        template = self.env.get_template('report.html')
        html = template.render(data=data)
        pdfkit.from_string(html, output_path)
        return output_path