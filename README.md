animeta
=======

## 개발 환경 설정

### 의존성

* Python 3.3 이상
* libpq
* Node.js, Gulp, Bower (`npm install -g gulp bower`)

### 준비: virtualenv

    python3 -m venv env
    . env/bin/activate
    curl https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -o - | python
    easy_install pip

### Server

    pip install -e .
    mkdir instance
    $EDITOR instance/config.py
    python manage.py runserver

### Asset Build

    bower install
    npm install
    gulp
