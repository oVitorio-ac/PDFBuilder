from flask import Flask, render_template, send_file, redirect, url_for,request
from pyloremgen.generator.lorem_pdf import PDFGenerator
from io import BytesIO



app = Flask(__name__)

pdf_buffer = None  # Variável global para o buffer do PDF

def generate_pdf(num_pages):
    """Gera o PDF com a quantidade especificada de páginas e retorna um buffer"""
    buffer = BytesIO()
    pdf_gen = PDFGenerator()
    pdf_gen.generate_pdf(buffer, num_pages=num_pages)  # Passa o número de páginas
    buffer.seek(0)
    return buffer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf_route():
    global pdf_buffer
    num_pages = int(request.form['num_pages'])
    pdf_buffer = generate_pdf(num_pages)
    return render_template('preview.html')

@app.route('/preview_pdf')
def preview_pdf():
    global pdf_buffer
    if pdf_buffer is None:
        return redirect(url_for('index'))
    pdf_buffer.seek(0)  # Reposiciona o ponteiro no início do buffer
    return send_file(pdf_buffer, mimetype='application/pdf')

@app.route('/download_pdf')
def download_pdf():
    global pdf_buffer
    if pdf_buffer is None:
        pdf_buffer = generate_pdf(1)  # Regenerar com uma página padrão se o buffer estiver fechado
    else:
        try:
            pdf_buffer.seek(0)  # Garante que o buffer esteja no início
        except ValueError:
            pdf_buffer = generate_pdf(1)  # Regenerar o PDF se o buffer estiver fechado

    return send_file(pdf_buffer, as_attachment=True, download_name='lorem_pdf.pdf')

@app.route('/cancel')
def cancel():
    global pdf_buffer
    pdf_buffer = None  # Limpa o buffer ao cancelar a operação
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)