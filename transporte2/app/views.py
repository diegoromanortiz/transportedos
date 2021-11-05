from flask import render_template,request,redirect,url_for,session
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi
from sqlalchemy.orm.session import SessionTransaction
from app import app
from . import appbuilder, db
from app import app
from .models import  ServicioTecnico,Camiones,Clientes,Saldos,Localidad,Repuestos,DetalleServicioTecnico, formaDePago,ClienteCamiones,ClienteServicioTecnico,MyForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_appbuilder.fieldwidgets import Select2Widget
from flask_appbuilder.actions import action
import pyautogui as pg
import webbrowser as web
import time
#funciones
def camiones_query():
    return db.session.query(Camiones)

def servicio_tecnico_query():
    return db.session.query(ServicioTecnico)   

   

class ClienteServicioTecnicoView(ModelView):
    datamodel = SQLAInterface(ClienteServicioTecnico)
    list_columns = [ "servicioTecnico_id"]

    @action("muldelete", "Borrar todos los items", "Estas seguro de borrar?", "fa-rocket", single=False)
    def muldelete(self, items):
       self.datamodel.delete_all(items)
       self.update_redirect()
       return redirect(self.get_redirect())
    
    

class ClienteCamionesView(ModelView):
    datamodel = SQLAInterface(ClienteCamiones)
    list_columns = [ "camion_id"]

    @action("muldelete", "Borrar todos los items", "Estas seguro de borrar?", "fa-rocket", single=False)
    def muldelete(self, items):
       self.datamodel.delete_all(items)
       self.update_redirect()
       return redirect(self.get_redirect())
    

class formaDePagoView(ModelView):
    datamodel = SQLAInterface(formaDePago)
    list_columns = ["tipoDePago"]

    @action("muldelete", "Borrar todos los items", "Estas seguro de borrar?", "fa-rocket", single=False)
    def muldelete(self, items):
       self.datamodel.delete_all(items)
       self.update_redirect()
       return redirect(self.get_redirect())
    

class SaldosView(ModelView):
    datamodel = SQLAInterface(Saldos)
    list_columns = ["fecha","cliente_id","saldo"]

    @action("muldelete", "Borrar todos los items", "Estas seguro de borrar?", "fa-rocket", single=False)
    def muldelete(self, items):
       self.datamodel.delete_all(items)
       self.update_redirect()
       return redirect(self.get_redirect())
    

class DetalleServicioTecnicoView(ModelView):
    datamodel = SQLAInterface(DetalleServicioTecnico)
    list_columns = ["detalle", "costoManoDeObra", "repuesto_id","servicoTecnico_id"]

    @action("muldelete", "Borrar todos los items", "Estas seguro de borrar?", "fa-rocket", single=False)
    def muldelete(self, items):
       self.datamodel.delete_all(items)
       self.update_redirect()
       return redirect(self.get_redirect())
      

class ServicioTecnicoView(ModelView):
    datamodel = SQLAInterface(ServicioTecnico) 
    list_columns = ["fecha", "costo", "cliente_id","camion_id"]

    @action("muldelete", "Borrar todos los items", "Estas seguro de borrar?", "fa-rocket", single=False)
    def muldelete(self, items):
       self.datamodel.delete_all(items)
       self.update_redirect()
       return redirect(self.get_redirect())

class RepuestosView(ModelView):
    datamodel = SQLAInterface(Repuestos)
    list_columns = ["categoria","descripcion","precio"]

    @action("muldelete", "Borrar todos los items", "Estas seguro de borrar?", "fa-rocket", single=False)
    def muldelete(self, items):
       self.datamodel.delete_all(items)
       self.update_redirect()
       return redirect(self.get_redirect())
    
    


class CamionesView(ModelView):
    datamodel = SQLAInterface(Camiones)
    list_columns = ["patente","marca", "modelo", "cliente_id"]

    @action("muldelete", "Borrar todos los items", "Estas seguro de borrar?", "fa-rocket", single=False)
    def muldelete(self, items):
       self.datamodel.delete_all(items)
       self.update_redirect()
       return redirect(self.get_redirect())
       
    
class ClientesView(ModelView):
    datamodel = SQLAInterface(Clientes)
    list_columns = ["nombre", "apellido", "email"]

    @action("muldelete", "Borrar todos los items", "Estas seguro de borrar?", "fa-rocket", single=False)
    def muldelete(self, items):
       self.datamodel.delete_all(items)
       self.update_redirect()
       return redirect(self.get_redirect())

    
   
    edit_form_extra_fields = {
       "Camiones": QuerySelectField(
            "Camiones",
            query_factory=camiones_query,
            widget=Select2Widget(extra_classes="readonly"),
        )
    }
    
    edit_form_extra_fields = {
       "servicio_tecnico": QuerySelectField(
            "ServicioTecnico",
            query_factory=servicio_tecnico_query,
            widget=Select2Widget(extra_classes="readonly"),
        )
    }

    related_views = [ClienteCamionesView,ClienteServicioTecnicoView]
    
    show_template = "appbuilder/general/model/show_cascade.html" 
    

"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

"""
    Application wide 404 error handler
"""



@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )





class LocalidadView(ModelView):
    datamodel = SQLAInterface(Localidad)
    add_columns = ["name"]
    edit_columns = ["name"]
    show_columns = ["name"]
    list_columns = ["name"]



from flask import flash
from flask_appbuilder import SimpleFormView
from flask_babel import lazy_gettext as _


class MyFormView(SimpleFormView):
    form = MyForm
    form_title = 'This is my first form view'
    message = 'My form submitted'

    def form_get(self, form):
        form.celular.data = 'Celular'
        form.mensaje.data = 'Mensaje'

    def form_post(self, form):
        celulares = form.celular.data
        mensajes = form.mensaje.data
        first = True
        
        time.sleep(8)
        web.open_new_tab("https://web.whatsapp.com/send?phone="+str(celulares)+"&text="+str(mensajes))
        if first:
            time.sleep(8)
            first=False
        width,height = pg.size()
        pg.click(width/2,height/2)
        time.sleep(20)
        pg.press('enter')
        time.sleep(6)
        pg.hotkey('ctrl', 'w')
       
        return redirect(self.get_redirect())
        




db.create_all()

appbuilder.add_view(
   ClientesView, "Clientes", icon="fa-folder-open-o", category="Clientes"
)
appbuilder.add_view(
    SaldosView, "Saldos", icon="fa-folder-open-o", category= "Clientes"
)

#appbuilder.add_separator("Clientes")
appbuilder.add_view(
    CamionesView, "Camiones", icon="fa-folder-open-o", category="Camiones"
)
appbuilder.add_view(
    ServicioTecnicoView, "ServicioTecnico", icon="fa-folder-open-o", category= "ServicioTecnico"

)
appbuilder.add_view(
    DetalleServicioTecnicoView, "DetalleServicioTecnico", icon="fa-folder-open-o", category= "ServicioTecnico"

)
appbuilder.add_view(
     RepuestosView, " Repuestos", icon="fa-folder-open-o", category= "Camiones"

)

appbuilder.add_view(
    LocalidadView, "Localidad", icon="fa-folder-open-o", category="Clientes"
)
appbuilder.add_view(
    formaDePagoView, "FormaDePago", icon="fa-folder-open-o", category= "ServicioTecnico"
)

appbuilder.add_view_no_menu(ClienteCamionesView,"ClienteCamionesView")

appbuilder.add_view_no_menu(ClienteServicioTecnicoView,"ClienteServicioTecnicoView")



appbuilder.add_link("Calculos", icon="fa-folder-open-o", href='https://www.onlinerekenmachine.com/calculadora', category='ServicioTecnico')

appbuilder.add_view(MyFormView, "My form View", icon="fa-group", label=_('Enviar msj '),
                     category="My Forms", category_icon="fa-cogs")   
