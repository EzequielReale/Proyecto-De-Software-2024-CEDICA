from src.core import board, auth,registro_pagos


def run():
    """Llena la base de datos con issues de prueba"""
    issue1 = board.create_issue(
        email="giu@gmail.com"
    )
    issue2= board.create_issue(
        email="yo@gmail.com"
    )
    role = auth.role_new(
        name="Administracion"
    )
    user1 = auth.user_new(
        email="giuliana@gmail.com",
        password="123",
        role = role,
        alias= "chu"
    )
    tipo1= registro_pagos.tipo_new(
        tipo="Honorarios"
    )
    tipo2= registro_pagos.tipo_new(
        tipo="Proveedor"
    ) 
    tipo3= registro_pagos.tipo_new(
        tipo="Varios"
    )
    pago = registro_pagos.pago_create(
        monto = 2000,
        beneficiario = user1,
        tipo_pago = tipo1
    )

