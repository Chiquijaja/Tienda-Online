import sqlite3

DB_FILES = 'db/database.db'


# 创建数据库中的表 Crear tablas en la base de datos
def create_tables():
    print("Creating tables...")
    f_name = 'db/store-schema.sql'
    with open(f_name, 'r', encoding='utf') as f:
        sql = f.read()
        # 创建数据库连接 Crear una conexión a la base de datos
        conn = sqlite3.connect(DB_FILES)
        try:
            conn.executescript(sql)
            print('La inicialización de la base de datos se ha realizado con éxito')
        except Exception as e:
            print('La inicialización de la base de datos se ha realizado incorrecto')
            print(e)
        finally:
            conn.close()


# 数据库商品表插入数据 Insertar datos en la tabla de productos de la base de datos
def load_data():
    f_name = 'db/store-dataload.sql'
    with open(f_name, 'r', encoding='utf') as f:
        sql = f.read()
        # 创建数据库连接
        conn = sqlite3.connect(DB_FILES)
        try:
            conn.executescript(sql)
            print('La inicialización de la base de datos se ha realizado con éxito')
        except Exception as e:
            print('La inicialización de la base de datos se ha realizado incorrecto')
            print(e)
        finally:
            conn.close()