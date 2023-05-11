from flask import Flask, render_template, request
import os
from os.path import basename
from ipdb import set_trace

from process_image import process_image

app = Flask(__name__)

# Get the absolute path to the 'static' folder
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'static')
# Set the upload folder for storing images
app.config['UPLOAD_FOLDER'] = os.path.join(static_folder, 'uploads')  

@app.route('/')
def index() -> str:
    '''Render the index.html template.'''
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload() -> str:
    '''Handle the image upload and process the image.'''
    if 'image' in request.files:
        # fetch relevant info from html 
        sigma = int(request.form['sigmaInput'])
        theta = int(request.form['thetaInput'])
        kernel = list(map(int, request.form['kernelSizeInput'].split('x')))
        use_filter = request.form['yesNoOption'] == 'Yes'
        image = request.files['image']
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)

        os.makedirs(os.path.dirname(image_path), exist_ok=True)  
        image.save(image_path)  

        # Process the image and save the processed image
        processed_image_path = process_image(image_path, theta,
                use_filter, sigma, kernel)

        return render_template('index.html',
                   image_path='uploads/' + basename(image_path),
                   processed_image_path='uploads/' + basename(processed_image_path))

    return "No image uploaded"


if __name__ == '__main__':
    app.run()

