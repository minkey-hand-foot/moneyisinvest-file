from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
import os, uuid

UPLOAD_FOLDER = '../'

app = Flask(__name__)
api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class FileUpload(Resource):
    def post(self):
        if 'file' not in request.files:
            return {
                "success": False,
                "msg": "요청 값에서 파일을 찾을 수 없습니다."
                }, 400
        
        file = request.files['file']
        
        if file.filename == '':
            return {
                "success": False,
                "msg": "파일이 업로드되지 않았습니다."
                }, 400
        
        if file:
            ext = os.path.splitext(file.filename)[1]
            filename = secure_filename(f"{uuid.uuid4()}{ext}")
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return {
                "success": True,
                "msg": f"{filename}"
                }, 200

from flask import send_file

class FileReader(Resource):
    def get(self, filename):
        try:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            return send_file(file_path, mimetype='image/jpeg')
        except FileNotFoundError:
            return {
                "success": False,
                "msg": "파일을 찾을 수 없습니다."
                }, 404

class StockFileReader(Resource):
    def get(self, filename):
        try:
            stock_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'stock')
            file_path = os.path.join(stock_folder, filename)
            
            return send_file(file_path, mimetype='image/jpeg')
        except FileNotFoundError:
            return {
                "success": False,
                "msg": "파일을 찾을 수 없습니다."
                }, 404
        except Exception as e:
            return {
                "success": False,
                "msg": f"오류 발생: {str(e)}"
                }, 500



api.add_resource(FileUpload, '/upload')
api.add_resource(FileReader, '/img/<string:filename>')
api.add_resource(StockFileReader, '/stock/<string:filename>')

if __name__ == '__main__':
    app.run(debug=True)