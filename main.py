import utils
import psutil
import logging
from flask import Flask, request

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

if __name__ == "__main__":
    print("main")
    app.run(host="0.0.0.0", port=5001, debug=True)