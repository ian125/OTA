from flask import Flask, request, redirect, render_template, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

# 현재 디렉토리 기준으로 'upload' 폴더 경로 설정 작성


@app.route('/')
def upload_form():
    return render_template('upload.html')# HTML 파일 경로를 Flask 기본 경로에 맞게 설정

@app.route('/upload', methods=['POST'])
#파일 업로드 시 동작 작성


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

