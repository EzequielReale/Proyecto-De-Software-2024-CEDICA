from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import flash
from flask import request
from src.core.user_role_permission.operations.user_operations import *
from src.core.user_role_permission.operations.role_operations import *
from src.web.controllers.user_controller.user_validator import RegistrationForm
from src.web.controllers.user_controller.user_validator import UpdateForm
from src.web.controllers.user_controller.user_validator import SearchForm


bp= Blueprint("user",__name__, url_prefix="/user")


@bp.get("/")
def index():
    """Listado de usuarios"""
    users = list_users()
    return render_template("user/index.html" , users=users)


@bp.route("/new" , methods=["GET", "POST"])
def create():
    """Formulario para crear un nuevo usuario"""
    form = RegistrationForm()

    if form.validate_on_submit():
        
        alias = form.alias.data
        email = form.email.data
        password = form.password.data
        confirmed_password = form.confirm_password.data
        role = form.role.data

        role_exists = get_role_by_name(role)
        if not role_exists:
            flash("Rol no válido", "danger")
            return redirect("/user/new")

        if user_exists(email):
            flash("Usuario ya existe", "danger")
            return redirect("/user/new")

        new_user = user_new(alias=alias, email=email, password=password, 
                            role=role_exists, isActive=True)

        if new_user:
            flash("Usuario creado exitosamente.", "success")
            return redirect("/user")
    
    return render_template('user/create.html', form=form)



@bp.post("/delete/<string:email>")
def delete(email: str):
    """Eliminar un usuario"""
    if( user_exists(email)):
        delete_user(email)
        flash("Usuario eliminado exitosamente.", "success")
        return redirect("/user")
    else:
        flash("El usuario que desea eliminar no existe", "danger")
        return redirect("/user")
    

# Sin terminar
@bp.route("/update/<string:email>", methods=['GET', 'POST'])
def update(email: str):
    """Formulario para editar un usuario"""
    user = get_user_by_email(email)
    form = UpdateForm()

    if form.validate_on_submit():

        form_data = {field.name: field.data for field in form}
        print(form_data)  

        
        flash("Usuario actualizado exitosamente.", "success")
        return redirect("/user")
                
    
    return render_template('user/update.html', user=user, form=form)
    

def update_email(user_email,new_email):
    if( user_exists(new_email)):
        flash("El email al que desea cambiar ya está en uso.", "danger")
        return redirect("/user/update")
    else:
        user_update(user_email, email=new_email)



@bp.route('/search', methods=['GET'])
def search():
    """Recibe los parametros de busqueda (email, estado, rol),
    filtra los registros, realiza la busqueda en la BD y retorna los resultados"""
    form = SearchForm(request.args, meta={'csrf': False})  # Desactivar CSRF para formularios GET
    search_executed = False
    users = []

    if request.args and form.validate():
        query = User.query
        search_executed = True
        
        if form.email.data:
            query = query.filter(User.email.like(f"%{form.email.data}%"))
        if form.status.data and form.status.data != 'Todos':
            query = query.filter(User.isActive == form.status.data)
        
        #if form.role.data:
         #   role_exists = get_role_by_name(form.role.data)
         #  query = query.filter(User.role.like(f"%{form.role.data}%"))
        
        users = query.all()

    return render_template('/user/search.html', form=form, search_executed=search_executed, users=users)


