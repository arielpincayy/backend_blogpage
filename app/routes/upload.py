from flask import Blueprint, request, jsonify, url_for
import os
from app.utils.helpers import slugify
from flask_jwt_extended import jwt_required
from app.schemas.upload_schema import UploadSchema
from marshmallow import ValidationError

upload_bp = Blueprint('upload', __name__)

IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
FOLDER = 'app/static/uploads/'

def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in IMAGE_EXTENSIONS

def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()

# Upload image route
@upload_bp.route('/image', methods=['POST'])
@jwt_required()
def upload_image():
    try:

        schema = UploadSchema()
        data = schema.load(request.form)

        blog_name = slugify(data['blog_name'])
        number = data['number']

        # Validate the file upload parameters
        if 'image' not in request.files:
            return jsonify({"error": "No file part"}), 400
    
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
    
        if not allowed_image(file.filename):
            return jsonify({"error": "File type not allowed"}), 400
        
        # Assign a filename based on its position
        extension = get_extension(file.filename)
        filename = number + '.' + extension
        FOLDER_IMAGES = os.path.join(FOLDER, 'images', blog_name)
        os.makedirs(FOLDER_IMAGES, exist_ok=True)
        save_path = os.path.join(FOLDER_IMAGES, filename)
        file.save(save_path)
    
        url = url_for('static', filename=f'uploads/images/{blog_name}/{filename}', _external=True)
        return jsonify({"message": "Image uploaded successfully", "url": url}), 201
    
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.messages}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while uploading the image", "details": str(e)}), 500

# Upload image route
@upload_bp.route('/pdf', methods=['POST'])
@jwt_required()
def upload_pdf():
    try:
        schema = UploadSchema()
        data = schema.load(request.form)
        blog_name = slugify(data['blog_name'])
        number = data['number']

        # Validate the file upload parameters
        if 'pdf' not in request.files:
            return jsonify({"error": "No file part"}), 400
    
        file = request.files['pdf']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
    
        if not get_extension(file.filename) == 'pdf':
            return jsonify({"error": "Only PDF files are allowed"}), 400

        # Assign a filename based on its position
        filename = number + '.pdf'
        FOLDER_PDFS = os.path.join(FOLDER, 'pdfs', blog_name)
        os.makedirs(FOLDER_PDFS, exist_ok=True)
        save_path = os.path.join(FOLDER_PDFS, filename)
        file.save(save_path)
    
        url = url_for('static', filename=f'uploads/pdfs/{blog_name}/{filename}', _external=True)
        return jsonify({"message": "PDF uploaded successfully", "url": url}), 201
    
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.messages}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while uploading the PDF", "details": str(e)}), 500
    
