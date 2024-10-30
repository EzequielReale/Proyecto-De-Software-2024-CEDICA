from datetime import datetime

from src.core import registro_pagos, people

def validar(monto, tipo_pago_id, fecha_pago, des, beneficiario_id):
    """Valido los parámetros según ciertos requerimientos"""
    if not monto or float(monto) <= 0:
        return False, "El monto debe ser mayor a 0", None, None

    if not tipo_pago_id:
        return False, "Debe seleccionar un tipo de pago", None, None
        
    if not fecha_pago:
        return False, "Debe ingresar una fecha de pago", None, None
    
    if fecha_pago > datetime.now().strftime('%Y-%m-%d'):
        return False, "La fecha de pago no puede ser futura", None, None
    
    if not des or len(des) > 255:
        return False, "La descripción es obligatoria y debe tener un máximo de 255 caracteres", None, None
    
    tipo_pago_obj = registro_pagos.get_tipo_pago(tipo_pago_id)
    if not tipo_pago_obj:
        return False, "El tipo de pago seleccionado no es válido", None, None
    
    beneficiario = None

    if beneficiario_id:
        beneficiario = people.get_member_by_field('id', beneficiario_id)
        if not beneficiario:
            return False, "El beneficiario seleccionado no es válido", None, None
    
    return True, "", beneficiario, tipo_pago_obj