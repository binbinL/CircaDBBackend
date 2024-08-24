TORTOISE_ORM = {
    'connections': {
        'default': {
            #
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': '127.0.0.1',
                'port': '3306',
                'user': 'root',
                'password': 'root',
                'database': 'circadian',
                'minsize': 1,
                'maxsize': 5,
                'charset': 'utf8mb4',
                'echo': True
            }
        },
    },
    'apps': {
        'models': {
            # 看models的位置
            'models': ['models', 'aerich.models'],
            # If no default_connection specified, defaults to 'default'
            'default_connection': 'default',
        }
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}
