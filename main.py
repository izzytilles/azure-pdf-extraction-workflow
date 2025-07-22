import utils
import psutil
import logging
from flask import Flask, request, jsonify, send_file
from io import BytesIO

app = Flask(__name__)



@app.route("/images", methods=["POST"])
def extract_images():
    try:
            # get file name from request
            if 'file' not in request.files:
                return "Please upload a file", 400

            uploaded_file = request.files['file']
            image_list = utils.extract_figures_from_pdf(uploaded_file)

            if not image_list:
                print("No images found")
                return "No content extracted from file.", 204  # no content
            

            return image_list, 200, {'Content-Type': 'text/plain'}

    except Exception as e:
            logging.error(f"Error processing file: {str(e)}")
            return f"Error: {str(e)}", 500
    
@app.route("/convert", methods=["POST"])
def convert_pdf():
    try:
        if 'file' not in request.files:
            return "Please upload a file", 400

        uploaded_file = request.files['file']
        images = utils.convert_pdf_to_image(uploaded_file)

        if not images:
            return "PDF could not be converted to an image, or PDF was not entered correctly.", 204 
        
        # convert image to BytesIO object 
        image_io = BytesIO()
        images[0].save(image_io, format='JPEG')
        image_io.seek(0)

        return send_file(
            image_io,
            mimetype='image/jpeg',
            as_attachment=True,
            download_name='converted_image.jpg'
        ), 200

    except Exception as e:
        logging.error(f"Error converting PDF to image: {str(e)}")
        return f"Error: {str(e)}", 500
    
if __name__ == "__main__":
    print("main")
    app.run(host="0.0.0.0", port=5001, debug=True)