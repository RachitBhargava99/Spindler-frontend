import os


class Config:
    SECRET_KEY = '0917b13a9091915d54b6336f45909539cce452b3661b21f386418a257883b30a'
    PROJECT_ID = os.environ.get('PROJECT_ID')
    DATA_BACKEND = os.environ.get('DATA_BACKEND')
    CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
    CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')
    CLOUDSQL_DATABASE = os.environ.get('CLOUDSQL_DATABASE')
    CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://{user}:{password}@localhost/{database}?unix_socket=/cloudsql/{connection_name}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD, database=CLOUDSQL_DATABASE,
        connection_name=CLOUDSQL_CONNECTION_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENDPOINT_ROUTE = 'http://spindler.thinger.appspot.com'
    MOST_SEARCH_URL = '/search/most'
    SEARCH_URL = '/search'
    NORMAL_REGISTER_URL = '/register'
    LOGIN_URL = '/login'
    SEARCH_HISTORY_URL = '/search/history'
    NEW_STREAM_URL = '/result/stream/add'
    ALL_STREAM_URL = '/result/stream/all'
    REMOVE_STREAM_URL = '/result/stream/remove'
    ADD_FAV_URL = '/result/fav'
    SHOW_FAV_URL = '/result/fav/show_all'
    REMOVE_FAV_URL = '/result/unfav'
