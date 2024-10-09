from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import flash
from flask import request
from src.core.user_role_permission.operations.user_operations import *
from src.core.user_role_permission.operations.role_operations import *
from src.web.controllers.user_controller.user_forms.user_register_form import RegistrationForm
from src.web.controllers.user_controller.user_forms.user_update_form import UpdateForm
from src.web.handlers.autenticacion import login_required


bp= Blueprint("user",__name__, url_prefix="/user")


@login_required
@bp.get("/")
def index():
    """Recibe los parametros de busqueda (email, estado, rol),
    filtra los registros, realiza la busqueda en la BD y retorna los resultados"""
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Obtener los filtros de búsqueda y ordenación
    filters = {
        'email': request.args.get('email'),
        'isActive': request.args.get('status'),
        'roles': request.args.get('role_id')
    }
    sort_by = request.args.get('sort_by', 'email')
    sort_direction = request.args.get('sort_direction', 'asc')

    users, total_pages = list_users_advance(filters, page, per_page, sort_by, sort_direction)

    return render_template('/user/index.html', 
                           page=page,
                           total_pages=total_pages,
                           roles = list_roles(),
                           sort_by=sort_by,
                           sort_direction=sort_direction,
                           filters=filters,
                           users=users)

@bp.get("/<string:email>")
def show(email: str)->str:
    """Recibe el email de un usuario y muestra su información"""
    user = get_user_by_email(email)
    return render_template('user/show.html', user=user)


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
    


