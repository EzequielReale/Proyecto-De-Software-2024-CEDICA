CREATE TABLE role_permissions (
    role_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    permission_id INTEGER NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Permisos para el rol 'Tecnica'
INSERT INTO role_permissions (role_id, permission_id) VALUES
((SELECT id FROM roles WHERE name='Tecnica'), (SELECT id FROM permissions WHERE name='encuestre_index')),
((SELECT id FROM roles WHERE name='Tecnica'), (SELECT id FROM permissions WHERE name='encuestre_show')),
((SELECT id FROM roles WHERE name='Tecnica'), (SELECT id FROM permissions WHERE name='jya_index')),
((SELECT id FROM roles WHERE name='Tecnica'), (SELECT id FROM permissions WHERE name='jya_show')),
((SELECT id FROM roles WHERE name='Tecnica'), (SELECT id FROM permissions WHERE name='jya_update')),
((SELECT id FROM roles WHERE name='Tecnica'), (SELECT id FROM permissions WHERE name='jya_new')),
((SELECT id FROM roles WHERE name='Tecnica'), (SELECT id FROM permissions WHERE name='jya_destroy'));

-- Permisos para el rol 'Encuestre'
INSERT INTO role_permissions (role_id, permission_id) VALUES
((SELECT id FROM roles WHERE name='Encuestre'), (SELECT id FROM permissions WHERE name='encuestre_index')),
((SELECT id FROM roles WHERE name='Encuestre'), (SELECT id FROM permissions WHERE name='encuestre_show')),
((SELECT id FROM roles WHERE name='Encuestre'), (SELECT id FROM permissions WHERE name='encuestre_update')),
((SELECT id FROM roles WHERE name='Encuestre'), (SELECT id FROM permissions WHERE name='encuestre_new')),
((SELECT id FROM roles WHERE name='Encuestre'), (SELECT id FROM permissions WHERE name='encuestre_destroy')),
((SELECT id FROM roles WHERE name='Encuestre'), (SELECT id FROM permissions WHERE name='jya_index')),
((SELECT id FROM roles WHERE name='Encuestre'), (SELECT id FROM permissions WHERE name='jya_show'));

-- Permisos para el rol 'Administracion'
INSERT INTO role_permissions (role_id, permission_id) VALUES
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='team_index')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='team_show')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='team_update')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='team_new')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='team_destroy')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='reg_pagos_index')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='reg_pagos_show')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='reg_pagos_update')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='reg_pagos_new')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='reg_pagos_destroy')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='encuestre_index')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='encuestre_show')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='jya_index')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='jya_show')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='jya_update')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='jya_new')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='jya_destroy'));
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='reg_cobros_index')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='reg_cobros_show')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='reg_cobros_update')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='reg_cobros_new')),
((SELECT id FROM roles WHERE name='Administracion'), (SELECT id FROM permissions WHERE name='reg_cobros_destroy')),

-- Permisos para el rol 'SystemAdmin'
INSERT INTO role_permissions (role_id, permission_id) VALUES
((SELECT id FROM roles WHERE name='SystemAdmin'), (SELECT id FROM permissions WHERE name='user_index')),
((SELECT id FROM roles WHERE name='SystemAdmin'), (SELECT id FROM permissions WHERE name='user_new')),
((SELECT id FROM roles WHERE name='SystemAdmin'), (SELECT id FROM permissions WHERE name='user_destroy')),
((SELECT id FROM roles WHERE name='SystemAdmin'), (SELECT id FROM permissions WHERE name='user_update')),
((SELECT id FROM roles WHERE name='SystemAdmin'), (SELECT id FROM permissions WHERE name='user_show')),
((SELECT id FROM roles WHERE name='SystemAdmin'), (SELECT id FROM permissions WHERE name='user_block')),
((SELECT id FROM roles WHERE name='SystemAdmin'), (SELECT id FROM permissions WHERE name='user_update_password')),
