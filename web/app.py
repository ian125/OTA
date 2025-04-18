from flask import Flask, request, redirect, render_template, url_for, flash
import os

app = Flask(__name__)
# 세션관리용 키
app.secret_key = 'secret_key'

# 현재 디렉토리 기준으로 'upload' 폴더 경로 설정 작성
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upload')
# 폴더가 없는 경우 폴더를 생성해서 프로그램이 돌아갈 수 있도록 함 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def upload_form():
    return render_template('upload.html')# HTML 파일 경로를 Flask 기본 경로에 맞게 설정

@app.route('/upload', methods=['POST'])
#파일 업로드 시 동작 작성
def upload_file():
    if 'file' not in request.files:
        flash('파일을 선택하세요')
        return redirect(url_for('upload_form'))
    file = request.files['file']
    username = request.form['username']
    password = request.form['password']
    print(f'File : {file.filename}, Username : {username}, Password : {password}')

    if file.filename == '':
        flash('파일이 존재하지 않습니다.')
        return redirect(url_for('upload_form'))
    if file :
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        flash(f"FILE '{file.filename}'이 성공적으로 업로드 되었습니다.")
        return redirect(url_for('upload_form'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) #외부 장치 접근 허용

