
# 🌟 Prueba Técnica: Sistema de Gestión de Reservas y RBAC

Este proyecto implementa un sistema backend modular para la gestión de reservas de canchas deportivas, haciendo un fuerte énfasis en la arquitectura de Roles y Permisos (RBAC), siguiendo los lineamientos de una prueba técnica para un rol de Backend Python Profesional.

La aplicación utiliza un enfoque moderno basado en FastAPI y SQLAlchemy sobre una base de datos PostgreSQL.

## Pasos para iniciar el sistema

* Crear entorno
``` bash
  python -m venv .venv
```
* instalar dependencias
``` bash
  pip install -r requirements.txt
```
* iniciar proyecto
``` bash
  uvicorn main:app --reload
```
Una vez iniciado el proyecto y estar corriendo la BD, debemos utilizar las siguientes sentencias para que asi el proyecto funcione correctamente. 
#### para crear los roles principales: 
```sql
  INSERT INTO roles (name, description) VALUES
('admin', 'Administrador del sistema con control total y permisos de gestión.'),
('user', 'Usuario estándar con permisos básicos para reservar canchas.');
```
#### para crear los permisos principales:
```sql
 INSERT INTO permissions (name) VALUES
('reservations:view_all'),
('roles:assign'),
('permissions:assign'),
('permissions:view'),
('permissions:create'),
('roles:delete'),
('roles:view'),
('roles:create'),
('fields:delete'),
('fields:update'),
('fields:create'),
('dashboard:view');
```


## 🌟 Stack Tecnologico

**framewoork:** FastAPI	Creación rápida de APIs asíncronas de alto rendimiento.

**Base de datos:** PostgreSQL Base de datos relacional robusta.

**ORM:** PSQLAlchemy Mapeo Objeto-Relacional para interactuar con la base de datos.

**Validación:** Pydantic Validación estricta de esquemas de datos (peticiones y respuestas).

**Seguridad:** Python hashlib/JWT Hashing de contraseñas y seguridad login.

## Features

- Login
- Reserva de canchas (crud)
- Roles (crud)
- permisos (crud)

## Arquitectura y Modelado de Datos

La base del sistema de seguridad se establece en la relación entre los roles y los permisos.

El sistema utiliza una relación Muchos a Muchos (N:M) explícita entre roles y permissions a través de la tabla de unión role_permissions. Esto permite que un mismo permiso (ej: "dashboard:view") pueda ser asignado a múltiples roles (admin, sub_gerente), cumpliendo con los requisitos de escalabilidad.

| clase/tabla | descripción | relaciones clave |
|----------|----------|----------|
|User (users)   | Información del usuario. | N:1 con Role (vía role_id). 1:N con Reservation.  |
| Role (roles)  | Define roles del sistema (admin, user).  | 1:N con User. 1:N con RolePermission (N:M a Permission).   |
| Permission (permissions)   | Catálogo de acciones del sistema (fields:create, roles:view). | 1:N con RolePermission (N:M a Role).  |
| RolePermission (role_permissions)   | Tabla de Unión N:M.  | FKs a Role y Permission.  |
|Reservation (reservations)   | Registro de reservas.  | N:1 con User y Field.  |


## ⚙️ Conclusión
El proyecto demuestra una implementación sólida de modelos de datos relacionales, servicios transaccionales y la lógica de permisos necesaria para la prueba técnica. El uso de la estructura N:M para roles y permisos asegura la flexibilidad y escalabilidad del módulo de seguridad.