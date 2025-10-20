from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
SUPER_ADMINS = [int(item.strip()) for item in env.str("SUPER_ADMINS", default="").split(',') if item.strip()]
MAN_GROUP = env.str("MAN_GROUP")
#IP = env.str("ip")
CHANNELS = [int(item.strip()) for item in env.str("CHANNELS", default="").split(',') if item.strip()]

PORT = env.int("PORT")
DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")
