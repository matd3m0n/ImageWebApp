from flask import Flask, render_template, request
import os
from os.path import basename
from ipdb import set_trace

from process_image import process_image

app = Flask(__name__)

# Get the absolute path to the 'static' folder
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app.config['UPLOAD_FOLDER'] = os.path.join(static_folder, 'uploads')  # Set the upload folder for storing images


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():

    if 'image' in request.files:
        sigma = int(request.form['sigmaInput'])
        theta = int(request.form['thetaInput'])
        kernel = list(map(int, request.form['kernelSizeInput'].split('x')))
        
        use_filter = request.form['yesNoOption'] == 'Yes'
        image = request.files['image']
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)  # Store the path of the uploaded image

        os.makedirs(os.path.dirname(image_path), exist_ok=True)  # Create the directory if it doesn't exist

        image.save(image_path)  # Save the uploaded image in the uploads folder

        # Process the image and save the processed image
        # Assuming you have a function called process_image() that takes the image path as input and returns the processed image path
        processed_image_path = process_image(image_path, theta,
                use_filter, sigma, kernel)

        return render_template('index.html',
                               image_path='uploads/' + basename(image_path),
                               processed_image_path='uploads/' + basename(processed_image_path))

    return "No image uploaded"


if __name__ == '__main__':
    app.run()

