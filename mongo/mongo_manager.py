from bson import ObjectId
from pymongo import MongoClient


class MongoManager:

    def __init__(self, collection_name, online: bool = False):
        """
        Crea la instancia conectada a la collecion en cuestion.
        sqlite: tfg
        :param collection_name: nombre de la conexion
        """
        username = 'seguridad'
        password = 'password_1'
        self.collection = MongoClient('mongodb://%s:%s@localhost:27017' % (username, password), authSource='practica2Seguridad')['practica2Seguridad'][collection_name]

    @staticmethod
    def bson_encoder(s):
        """
        Transforma el ObjectId de BSON a String, haciendo el objeto serializable
        :param s: String
        :return: String
        """
        if type(s) == ObjectId:
            return str(s)
        return s.__str__


class MongoException(Exception):
    pass


'''
    Conexiones
'''

usuarios = MongoManager('usuario', False).collection