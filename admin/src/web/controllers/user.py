from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import flash
from flask import request
from flask import session

# Importación funciones de modelo User
from src.core.user_role_permission.operations.user_operations import get_user_by_email, list_users_advance, user_exists
from src.core.user_role_permission.operations.user_operations import user_new, delete_user, user_update, user_update_password
from src.core.user_role_permission.operations.user_operations import add_role_to_user, delete_role_from_user

# Importación funciones de modelo Role
from src.core.user_role_permission.operations.role_operations import list_roles, role_exists, roles_exists, get_role_by_name

# Importación formularios
from src.web.forms.user_register_form import RegistrationForm
from src.web.forms.user_update_form import UpdateForm
from src.web.forms.user_update_form import UpdatePassword

# Importación funciones de adicionales
from src.web.handlers.autenticacion import login_required
from src.web.handlers.autenticacion import check_permission,login_required
from src.web.controllers.auth import logout
from src.web.handlers.error import unauthorized


bp= Blueprint("user",__name__, url_prefix="/user")


@login_required
@bp.get("/")
def index():
    """Recibe los parametros de busqueda (email, estado, rol),
    filtra los registros, realiza la busqueda en la BD y retorna los resultados"""
    if  not check_permission(session,"user_index"):
         return unauthorized()
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

@login_required
@bp.get("/<string:email>")
def show(email: str)->str:
    """Recibe el email de un usuario y muestra su información"""
    if  not check_permission(session,"user_show"):
         return unauthorized()
    user = get_user_by_email(email)
    return render_template('user/show.html', user=user)


@login_required
@bp.route("/new" , methods=["GET", "POST"])
def create():
    """Formulario para crear un nuevo usuario"""
    if  not check_permission(session,"user_new"):
         return unauthorized()
    form = RegistrationForm()

    if form.validate_on_submit():
        
        alias = form.alias.data
        email = form.email.data
        password = form.password.data
        confirmed_password = form.confirm_password.data
        roles = form.role.data

        selected_roles = []


        if not roles:
            flash("Debe seleccionar al menos un rol", "danger")
            return redirect("/user/new")
        
        for role in roles: 
            if ( role_exists(role) is False):
                flash("Rol no válido", "danger")
                return redirect("/user/new")
            else: selected_roles.append(get_role_by_name(role))

        if user_exists(email):
            flash("El email ingresado ya está en uso.", "danger")
            return redirect("/user/new")

        new_user = user_new(alias=alias,
                            email=email, 
                            password=password, 
                            roles=selected_roles, 
                            isActive=True)

        if new_user:
            flash("Usuario creado exitosamente.", "success")
            return redirect("/user")
        
    
    return render_template('user/create.html', form=form)


@login_required
@bp.post("/delete/<string:email>")
def delete(email: str):
    """Recibe el email de un usuario y lo elimina de la BD"""
    if  not check_permission(session,"user_destroy"):
         return unauthorized()
    
    # Chequea si el usuario a eliminar existe
    if( user_exists(email)):

        # Chequea si el usuario se intenta eliminar a sí mismo
        
        if email == session.get("user"):  
            flash("No puedes eliminar tu propio usuario.", "danger")
            return redirect("/user")
        
        # Chequea si el usuario a eliminar es SystemAdmin
        if get_role_by_name('SystemAdmin') in get_user_by_email(email).roles:
            flash("No es posible eliminar usuarios con rol SystemAdmin", "danger")
            return redirect("/user")
        
        print('Se eliminara el usuario')
        delete_user(email)
        flash("Usuario eliminado exitosamente.", "success")
        return redirect("/user")
    
    else:
        flash("El usuario que desea eliminar no existe", "danger")
        return redirect("/user")
    

@login_required
@bp.route("/update/<string:email>", methods=['GET', 'POST'])
def update(email: str):
    """Formulario para editar un usuario"""
    if  not check_permission(session,"user_update"):
         return unauthorized()
    
    user = get_user_by_email(email)
    form = UpdateForm()

    # Cargar los roles del usuario en el formulario
    form.roles_to_delete.choices = list(user.roles)

    # Cargar todos los roles disponibles en el formulario excepto los que el usuario ya tiene y el rol SystemAdmin
    form.roles_to_add.choices = list(set(list_roles()) - set(user.roles) - set([get_role_by_name('SystemAdmin')]))

    if form.validate_on_submit():

        alias = form.alias.data
        email = form.email.data
        roles_to_delete = form.roles_to_delete.data
        roles_to_add = form.roles_to_add.data

        # Convierto los roles del usuario a una lista de strings
        user_roles = [role.name for role in user.roles]

        # Diccionario donde se guardan los campos sobre los que se realizarán cambios en el usuario
        fields_to_change = {}
        

        # Verifica si ingreso algun dato nuevo para realizar cambios
        if not alias and not email and not roles_to_delete and not roles_to_add:
            flash("No se ha realizado ningún cambio.", "warning")
            return redirect("/user")

        if alias:
            fields_to_change['alias'] = alias


        # Valida que el email no exista
        if email:
            if user_exists(email):
                flash("El email ingresado ya está en uso.", "danger")
                return redirect("/user")
            
            # Chequea si el usuario al que se intenta cambiar la contraseña es el mismo que esta logueado
            if user.email == session.get("user"):  
                flash("No es posible cambiar su propio email", "danger")
                return redirect("/user")
            
            fields_to_change['email'] = email
        
        
        if len(roles_to_add) > 0:       
            # Valida que los roles a agregar existan
            if roles_exists(roles_to_add):

                # Hace las validaciones con respecto al agregado de roles

                validation = validate_roles(roles_to_add, user_roles, action='add')
                if validation['result'] is False:
                    flash(f"{validation['message']}", "danger")
                    return redirect("/user")
                else: 
                    fields_to_change['roles_to_add'] = roles_to_add 

            else:
                flash(f"Alguno de los roles a agregar no era válido", "danger")
                return redirect("/user")

        
        if len(roles_to_delete) > 0:

            # Valida que los roles a eliminar existan
            if roles_exists(roles_to_delete):

                # Hace las validaciones con respecto al agregado de roles

                validation = validate_roles(roles_to_delete, user_roles, action='delete')
                if validation['result'] is False:
                    flash(f"{validation['message']}", "danger")
                    return redirect("/user")
                else: 
                    fields_to_change['roles_to_delete'] = roles_to_delete

            else:
                flash(f"Alguno de los roles a eliminar no era válido", "danger")
                return redirect("/user")
        

        # Actualiza los campos del usuario luego de todas las validaciones
        for field, value in fields_to_change.items():

            if field == 'email' or field == 'alias':
                user_update(user.id, **{field: value})
            elif field == 'roles_to_add':
                for role in value:
                    add_role_to_user(user.id, role)
            elif field == 'roles_to_delete':
                for role in value:
                    delete_role_from_user(user.id, role)
        
        flash("Usuario actualizado exitosamente.", "success")
        return redirect("/user")
                
    return render_template('user/update.html', user=user, form=form)


def validate_roles(roles, user_roles, action):
    """
    Valida los roles a agregar o eliminar en función de la acción especificada.
    
    :param roles: Lista de roles a validar.
    :param user_roles: Roles actuales del usuario.
    :param action: Acción a realizar ('add' o 'delete').
    :return: Diccionario con el resultado de la validación y un mensaje.
    """

    validation = {'result': True, 'message': ''}
   
    for role in roles:
        if action == 'delete':
            if role not in user_roles:
                validation['result'] = False
                validation['message'] = f"El rol {role} no existe en el usuario"
                break
            if role == 'SystemAdmin':
                validation['result'] = False
                validation['message'] = f"No es posible quitar el rol SystemAdmin a otro SystemAdmin"
                break
        
        elif action == 'add':
            if role in user_roles:
                validation['result'] = False
                validation['message'] = f"El usuario ya tiene el rol {role}"
                break
            if role == 'SystemAdmin':
                validation['result'] = False
                validation['message'] = "No es posible asignar el rol SystemAdmin a un usuario"
                break

    return validation



@login_required
@bp.route("/update/password/<string:email>", methods=['GET', 'POST'])
def update_password(email: str):
    """Formulario para actualizar contraseña de un usuario"""
    if  not check_permission(session,"user_update_password"):
         return unauthorized()

    user = get_user_by_email(email)
    form = UpdatePassword()

    if form.validate_on_submit():

        password = form.password.data
        confirm_password = form.confirm_password.data

        user_update_password(email, password)

        flash("Contraseña actualizada exitosamente.", "success")
        return redirect("/user")
                
    return render_template('user/update.html', user=user, form=form)


@login_required
@bp.route("/update/status/<string:email>", methods=['POST'])
def block_user(email: str):
    """Formulario para bloquear o desbloquear un usuario"""
    if  not check_permission(session,"user_block"):
         return unauthorized()
    
    user = get_user_by_email(email)
    
    action = request.form.get('action')
    
    if action == 'block':
        if user.isActive:
            # Verificar que el usuario no sea SystemAdmin
            if get_role_by_name('SystemAdmin') in user.roles:
                flash("No es posible bloquear usuarios con rol SystemAdmin ", "danger")
                return redirect("/user")

            user_update(user.id, isActive=False)
            flash("Usuario bloqueado exitosamente.", "success")

        else:
            flash("El usuario ya se encontraba bloqueado.", "warning")
    
    elif action == 'unblock':
        if not user.isActive:
            
            user_update(user.id, isActive=True)
            flash("Usuario desbloqueado exitosamente.", "success")

        else:
            flash("No es posible desbloquear a un usuario que ya está activo.", "warning")
    
    return redirect("/user")

    

    

    


