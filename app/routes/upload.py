from flask import Blueprint, request, jsonify, url_for, send_from_directory, current_app
import os
from app.utils.helpers import slugify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.upload_schema import UploadSchema
from marshmallow import ValidationError
from PIL import Image

upload_bp = Blueprint('upload', __name__)

IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
MAXLENGTH_PDF = 10 * 1024 * 1024  # 10 MB
MAXLENGTH_IMAGE = 5 * 1024 * 1024  # 5 MB
MAXLENGTH_MDX = 10 * 1024 *1024 # 10 MB

def get_uploads_root():
    return os.path.join(current_app.root_path, 'static', 'uploads')

def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in IMAGE_EXTENSIONS

def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()

# Convert image to WebP format
def convert_image_to_webp(image_path, output_path):
    try:
        # Check if the image is already in WebP format
        if image_path.lower().endswith('.webp'):
            os.rename(image_path, output_path)
            return output_path
        
        # Convert the image to WebP format
        with Image.open(image_path) as img:
            img = img.convert('RGB') 
            img.save(output_path, 'webp', quality=80) #Quality 80 is a good balance between quality and file size
            return output_path
    except Exception as e:
        raise ValueError(f"Error converting image to WebP: {str(e)}")

# Upload image route
@upload_bp.route('/image', methods=['POST'])
@jwt_required()
def upload_image():
    try:
        schema = UploadSchema()
        data = schema.load(request.form)

        blog_name = slugify(data['blog_name'])
        number = data['number']
        
        userId = get_jwt_identity()

        # Validate the file upload parameters
        if 'image' not in request.files:
            return jsonify({"error": "No file part"}), 400
    
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
    
        if not allowed_image(file.filename):
            return jsonify({"error": "File type not allowed"}), 400
        
        if file.content_length > MAXLENGTH_IMAGE:
            return jsonify({"error": "File size exceeds the maximum limit of 10 MB"}), 400
        
        # Assign a filename based on its position
        extension = get_extension(file.filename)
        filename_temp = number + '.' + extension
        FOLDER = get_uploads_root()
        FOLDER_IMAGES = os.path.join(FOLDER, 'images', userId, blog_name)
        os.makedirs(FOLDER_IMAGES, exist_ok=True)
        save_path_temp = os.path.join(FOLDER_IMAGES, filename_temp)
        file.save(save_path_temp)

        # Convert the image to WebP format
        filename = number + '.webp'
        save_path = os.path.join(FOLDER_IMAGES, filename)
        convert_image_to_webp(save_path_temp, save_path)
        if not save_path_temp.endswith('.webp'):
            os.remove(save_path_temp)

        # Generate the URL for the uploaded image
        url = url_for('static', filename=f'uploads/images/{userId}/{blog_name}/{filename}', _external=True)
        return jsonify({"message": "Image uploaded successfully", "url": url}), 201
    
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.messages}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while uploading the image", "details": str(e)}), 500

# Upload pdf route
@upload_bp.route('/pdf', methods=['POST'])
@jwt_required()
def upload_pdf():
    try:
        schema = UploadSchema()
        data = schema.load(request.form)
        blog_name = slugify(data['blog_name'])
        number = data['number']
        
        userId = get_jwt_identity()

        # Validate the file upload parameters
        if 'pdf' not in request.files:
            return jsonify({"error": "No file part"}), 400
    
        file = request.files['pdf']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
    
        if not get_extension(file.filename) == 'pdf':
            return jsonify({"error": "Only PDF files are allowed"}), 400
        
        if file.content_length > MAXLENGTH_PDF:
            return jsonify({"error": "File size exceeds the maximum limit of 10 MB"}), 400

        # Assign a filename based on its position
        filename = number + '.pdf'
        FOLDER = get_uploads_root()
        FOLDER_PDFS = os.path.join(FOLDER, 'pdfs', userId, blog_name)
        os.makedirs(FOLDER_PDFS, exist_ok=True)
        save_path = os.path.join(FOLDER_PDFS, filename)
        file.save(save_path)
    
        # Generate the URL for the uploaded PDF
        url = url_for('static', filename=f'uploads/pdfs/{userId}/{blog_name}/{filename}', _external=True)
        return jsonify({"message": "PDF uploaded successfully", "url": url}), 201
    
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.messages}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while uploading the PDF", "details": str(e)}), 500
    

# Upload mdx route
@upload_bp.route('/mdx', methods=['POST'])
@jwt_required()
def upload_mdx():
    try:
        schema = UploadSchema(only=('blog_name',))
        data = schema.load(request.form)
        blog_name = slugify(data['blog_name'])

        userId = get_jwt_identity()

        # Validate the file upload parameters
        if 'mdx' not in request.files:
            return jsonify({"error": "No file part"}), 400
    
        file = request.files['mdx']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
    
        if not get_extension(file.filename) == 'mdx':
            return jsonify({"error": "Only MDX files are allowed"}), 400
        
        if file.content_length > MAXLENGTH_MDX:
            return jsonify({"error": "File size exceeds the maximum limit of 10 MB"}), 400

        # Assign a filename based on its position
        filename = blog_name + '.mdx'
        FOLDER = get_uploads_root()
        FOLDER_MDXS = os.path.join(FOLDER, 'mdxs', userId)
        os.makedirs(FOLDER_MDXS, exist_ok=True)
        save_path = os.path.join(FOLDER_MDXS, filename)
        file.save(save_path)
    
        # Generate the URL for the uploaded MDX
        url = url_for('static', filename=f'uploads/mdxs/{userId}/{filename}', _external=True)
        return jsonify({"message": "MDX uploaded successfully", "url": url}), 201
    
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.messages}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while uploading the MDX", "details": str(e)}), 500
    
@upload_bp.route('/static/uploads/mdx/<int:id>/<path:filename>')
def serve_mdx(id, filename):
    FOLDER = get_uploads_root()
    path_mdx = os.path.join(FOLDER, 'mdxs', str(id))
    return send_from_directory(path_mdx, filename)