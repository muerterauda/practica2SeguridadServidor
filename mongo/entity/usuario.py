from datetime import datetime

from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, diccionario):
        self.__id_mongo = diccionario.get('_id')
        if self.__id_mongo:
            self.__id_mongo = str(self.__id_mongo)
        self.id = diccionario.get('id')
        self.name = diccionario.get('name')
        self.avatar = diccionario.get('avatar')
        self.__archivos = self.__generar_dict_archivos(diccionario.get('archivos'))

    def user_to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "avatar": self.avatar, 'archivos': self.__generar_list_archivos(self.__archivos)}

    @property
    def id_mongo(self):
        return self.__id_mongo

    @property
    def id_mongo_str(self):
        return str(self.__id_mongo)

    @property
    def nombre_email(self):
        return self.id.split('@')[0]

    def eliminar_archivo(self, nombre):
        self.__archivos.pop(nombre, None)

    def get_clave_encriptado(self, nombre):
        return self.__archivos.get(nombre)

    def comprobar_archivo(self, nombre):
        return nombre in self.__archivos

    def guardar_archivo(self, nombre):
        self.__archivos[nombre] = {'fecha_subida': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}

    def get_list_archivos(self):
        returned = []
        if self.__archivos is not None:
            for x, y in self.__archivos.items():
                returned.append((x, y['fecha_subida']))
        return returned

    @staticmethod
    def __generar_dict_archivos(diccionario: list):
        returned = {}
        if diccionario is not None:
            for x in diccionario:
                returned[x[0]] = {'fecha_subida': x[1]}
        return returned

    @staticmethod
    def __generar_list_archivos(diccionario: dict):
        returned = []
        if diccionario is not None:
            for x, y in diccionario.items():
                returned.append((x, y['fecha_subida']))
        return returned

    def __str__(self):
        return self.id + ", " + self.name
