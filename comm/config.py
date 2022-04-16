import configparser

config = configparser.ConfigParser()
config.read('comm/config.ini')

G_API_KEY = config['DEFAULT']['G_API_KEY']
G_SECRET_KEY = config['DEFAULT']['G_SECRET_KEY']
# print(G_API_KEY)