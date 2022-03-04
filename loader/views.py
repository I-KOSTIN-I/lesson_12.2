import logging

from flask import Blueprint, render_template, request

from exceptions import DataLayerError, PictureWrongTypeError
from functions import PostsHandler, save_uploaded_picture

load_blueprint = Blueprint('load_blueprint', __name__, template_folder='templates')
logging.basicConfig(filename="basic.log", level=logging.INFO)


@load_blueprint.route('/post')
def load_page():
    return render_template('post_form.html')


@load_blueprint.route('/post', methods=['POST'])
def create_user_post():
    picture = request.files.get('picture', None)
    content = request.form.get('content', None)
    posts_handler = PostsHandler('posts.json')

    if not picture or not content:
        return 'Данные не загружены'

    try:
        picture_path = save_uploaded_picture(picture)
    except PictureWrongTypeError:
        logging.info('Неверный тип файла')
        return 'Неверный тип файла'
    except FileNotFoundError:
        return 'Не удалось сохранить файл, путь не найден'

    picture_url = '/' + picture_path
    post_object = {'pic': picture_url, 'content': content}

    try:
        posts_handler.add_post(post_object)
    except DataLayerError:
        return 'Пост не добавлен, ошибка записи'

    return render_template('post_uploaded.html', picture_url=picture_url, content=content)
