import datetime
from typing import Text
from . import appbuilder, db
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Table
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import SessionTransaction
from sqlalchemy.sql.sqltypes import Numeric
from flask import session,request
from wtforms import Form, StringField
from wtforms.validators import DataRequired
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder.api import BaseApi, expose, rison ,safe
from . import appbuilder
import prison
schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        }
    }
}

print(prison.dumps(schema))

class ExampleApi(BaseApi):
    #route_base = '/newapi/v2/nice'
    resource_name = 'example'
    @expose('/greeting4')
    @rison(schema)
    def greeting4(self, **kwargs):
        return self.response(
        200,
        message=f"Hello {kwargs['rison']['name']}"
    )
    @expose('/error')
    @safe
    def error(self):
       raise Exception

appbuilder.add_api(ExampleApi)



class MyForm(DynamicForm):
    celular = StringField(('Celular'),
        description=('Ingresar numero de celular!'),
        validators = [DataRequired()], widget=BS3TextFieldWidget())
    mensaje = StringField(('Mensaje'),
        description=('Mensaje!'), widget=BS3TextFieldWidget())


   
cli = []


def today():
    return datetime.datetime.today().strftime('%d/%m/%Y')


class Saldos(Model):

    sid = Column(Integer, primary_key=True)
    fecha = Column(String, default=today, nullable=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    Clientes = relationship("Clientes")
    saldo = Column(Float)


class DetalleServicioTecnico(Model):

    dstid = Column(Integer, primary_key=True)
    detalle = Column(String)
    costoManoDeObra = Column(Float)
    repuesto_id = Column(Integer, ForeignKey("repuestos.id"), nullable=False)
    repuestos = relationship("Repuestos")
    servicioTecnico_id = Column(Integer, ForeignKey(
        "servicio_tecnico.stid"), nullable=False)
    servicio_tecnico = relationship("ServicioTecnico")


class Repuestos(Model):
    id = Column(Integer, primary_key=True)
    categoria = Column(String)
    descripcion = Column(String)
    precio = Column(Float)

    def __repr__(self):
        return f"('{self.descripcion}', '{self.precio}')"



class ServicioTecnico(Model):
    
    stid = Column(Integer, primary_key=True)
    fecha = Column(String, default=today, nullable=True)
    costo = Column(Float)
    formaPago = Column(Integer, ForeignKey(
        "forma_de_pago.fdpid"), nullable=False)
    forma_de_pago = relationship("formaDePago")
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    Clientes = relationship("Clientes")
    camion_id = Column(Integer, ForeignKey("camiones.cid"), nullable=False)
    camiones = relationship("Camiones")

    def __repr__(self):

        return f"('{self.costo}', '{self.cliente_id}', '{self.fecha}')"


class formaDePago(Model):

    fdpid = Column(Integer, primary_key=True)
    tipoDePago = Column(String(75), nullable=False)

    def __repr__(self):
        return f"('{self.tipoDePago}')"
        
class ClienteServicioTecnico(Model):
    cstid = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    Clientes = relationship("Clientes")
    servicioTecnico_id = Column(Integer, ForeignKey(
        "servicio_tecnico.stid"), nullable=False)
    servicio_tecnico = relationship("ServicioTecnico")
    fecha = Column(String, default=today, nullable=True)
    def __repr__(self):
        return f"('{self. servicioTecnico_id}')"

class ClienteCamiones(Model):
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    Clientes = relationship("Clientes")
    camion_id = Column(Integer, ForeignKey("camiones.cid"), nullable=False)
    camiones = relationship("Camiones")
    fecha = Column(String, default=today, nullable=True)
    def __repr__(self):
        return f"('{self.camion_id}')"

class Camiones(Model):

    cid = Column(Integer, primary_key=True)
    patente = Column(String(75), nullable=False)
    marca = Column(String(75), nullable=False)
    modelo = Column(String(75), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    clientes = relationship("Clientes")

    def __repr__(self):
        return f"('{self.marca}', '{self.modelo}')"


class Localidad(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


assoc_localidades_clientes = Table(
    "localidades_clientes",
    Model.metadata,
    Column("id", Integer, primary_key=True),
    Column("localidad_id", Integer, ForeignKey("localidad.id")),
    Column("cliente_id", Integer, ForeignKey("clientes.id")),
)


class Clientes(Model):

    id = Column(Integer, primary_key=True)
    nombre = Column(String(75), nullable=False)
    apellido = Column(String(75), nullable=False)
    telefono = Column(String(25), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    direccion = Column(String(120), unique=True, nullable=False)
    localidad = relationship(
        "Localidad", secondary=assoc_localidades_clientes, backref="cliente"
    )
   
    def __repr__(self):
    
        return f"('{self.nombre}', '{self.apellido}')"




