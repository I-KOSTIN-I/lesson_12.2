import json
# from pprint import pprint

from exceptions import DataLayerError, PictureWrongTypeError


class PostsHandler:
    def __init__(self, path):
        self.path = path

    def load_posts_from_json(self):
        """Загружает данные из JSON"""
        try:
            with open(self.path, 'r', encoding='utf=8') as file:
                posts = json.load(file)
            return posts

        except (FileNotFoundError, json.JSONDecodeError):
            raise DataLayerError('Что-то не так с файлом')

    def search_posts_for_substring(self, substring):
        """Ищет совпадения ввода пользователя в тексте постов"""
        substring_lower = substring.lower()
        posts_found = []

        posts = self.load_posts_from_json()
        for post in posts:
            if substring_lower in post['content'].lower():
                posts_found.append(post)

        return posts_found

    def add_post(self, post):
        """Добавляет данные загруденные данные"""
        posts = self.load_posts_from_json()
        posts.append(post)
        self.save_posts_to_json(posts)

    def save_posts_to_json(self, posts):
        """Записывает загруженную информацию в JSON"""
        try:
            with open(self.path, 'w', encoding='utf-8') as file:
                json.dump(posts, file)
        except FileNotFoundError:
            raise DataLayerError


def save_uploaded_picture(picture):
    """Проверяет и сохраняет загруженное изображение в папку uploads/images"""
    filename = picture.filename
    file_type = filename.split('.')[-1]

    if file_type not in ['jpg', 'jpeg', 'png', 'svg']:
        raise PictureWrongTypeError

    picture.save(f'./uploads/images/{filename}')

    return f'uploads/images/{filename}'

# posts_handler = PostsHandler('posts.json')
# posts_handler.add_post({'pic': 1, 'content': 2})
# posts = posts_handler.search_posts_for_substring('ржавые')
# pprint(posts)
