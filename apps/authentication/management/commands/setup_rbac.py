from django.core.management.base import BaseCommand
from apps.authentication.models import Role, Menu, RoleMenuAccess
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Configura datos iniciales de RBAC (Roles, Menús y Permisos)"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Iniciando configuración de RBAC..."))

        # ==================== CREAR ROLES ====================
        self.stdout.write("\n📋 Creando roles...")

        admin_role, created = Role.objects.get_or_create(
            code="ADMIN",
            defaults={
                "name": "Administrador",
                "description": "Acceso completo al sistema",
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS("  ✓ Rol 'Administrador' creado"))
        else:
            self.stdout.write("  - Rol 'Administrador' ya existe")

        operador_role, created = Role.objects.get_or_create(
            code="OPERADOR",
            defaults={
                "name": "Operador",
                "description": "Acceso a operaciones básicas",
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS("  ✓ Rol 'Operador' creado"))
        else:
            self.stdout.write("  - Rol 'Operador' ya existe")

        # ==================== CREAR MENÚS PADRE ====================
        self.stdout.write("\n📁 Creando menús principales...")

        dashboard_menu, created = Menu.objects.get_or_create(
            code="dashboard",
            defaults={
                "name": "Dashboard",
                "icon": "dashboard",
                "route": "/dashboard",
                "parent": None,
                "order": 1,
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS("  ✓ Menú 'Dashboard' creado"))
        else:
            self.stdout.write("  - Menú 'Dashboard' ya existe")

        admin_menu, created = Menu.objects.get_or_create(
            code="administration",
            defaults={
                "name": "Administración",
                "icon": "settings",
                "route": None,
                "parent": None,
                "order": 2,
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS("  ✓ Menú 'Administración' creado"))
        else:
            self.stdout.write("  - Menú 'Administración' ya existe")

        operations_menu, created = Menu.objects.get_or_create(
            code="operations",
            defaults={
                "name": "Operaciones",
                "icon": "work",
                "route": None,
                "parent": None,
                "order": 3,
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS("  ✓ Menú 'Operaciones' creado"))
        else:
            self.stdout.write("  - Menú 'Operaciones' ya existe")

        # ==================== CREAR SUBMENÚS (CHILDREN) ====================
        self.stdout.write("\n📂 Creando submenús...")

        # Children de Administración
        users_menu, created = Menu.objects.get_or_create(
            code="users",
            defaults={
                "name": "Usuarios",
                "icon": "people",
                "route": "/admin/users",
                "parent": admin_menu,
                "order": 1,
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS("  ✓ Submenú 'Usuarios' creado en Administración")
            )
        else:
            self.stdout.write("  - Submenú 'Usuarios' ya existe")

        roles_menu, created = Menu.objects.get_or_create(
            code="roles",
            defaults={
                "name": "Roles",
                "icon": "security",
                "route": "/admin/roles",
                "parent": admin_menu,
                "order": 2,
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS("  ✓ Submenú 'Roles' creado en Administración")
            )
        else:
            self.stdout.write("  - Submenú 'Roles' ya existe")

        agencies_menu, created = Menu.objects.get_or_create(
            code="agencies",
            defaults={
                "name": "Agencias",
                "icon": "business",
                "route": "/admin/agencies",
                "parent": admin_menu,
                "order": 3,
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS("  ✓ Submenú 'Agencias' creado en Administración")
            )
        else:
            self.stdout.write("  - Submenú 'Agencias' ya existe")

        # Children de Operaciones
        bets_menu, created = Menu.objects.get_or_create(
            code="bets",
            defaults={
                "name": "Apuestas",
                "icon": "casino",
                "route": "/operations/bets",
                "parent": operations_menu,
                "order": 1,
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS("  ✓ Submenú 'Apuestas' creado en Operaciones")
            )
        else:
            self.stdout.write("  - Submenú 'Apuestas' ya existe")

        reports_menu, created = Menu.objects.get_or_create(
            code="reports",
            defaults={
                "name": "Reportes",
                "icon": "assessment",
                "route": "/operations/reports",
                "parent": operations_menu,
                "order": 2,
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS("  ✓ Submenú 'Reportes' creado en Operaciones")
            )
        else:
            self.stdout.write("  - Submenú 'Reportes' ya existe")

        # ==================== ASIGNAR PERMISOS ====================
        self.stdout.write("\n🔐 Asignando permisos...")

        # Permisos para ADMIN (acceso completo)
        self.stdout.write("  Configurando permisos para 'Administrador'...")
        admin_menus = [
            dashboard_menu,
            admin_menu,
            users_menu,
            roles_menu,
            agencies_menu,
            operations_menu,
            bets_menu,
            reports_menu,
        ]

        admin_count = 0
        for menu in admin_menus:
            _, created = RoleMenuAccess.objects.get_or_create(
                role=admin_role, menu=menu, defaults={"is_active": True}
            )
            if created:
                admin_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"  ✓ {admin_count} permisos nuevos para Administrador")
        )

        # Permisos para OPERADOR (acceso limitado)
        self.stdout.write("  Configurando permisos para 'Operador'...")
        operador_menus = [dashboard_menu, operations_menu, bets_menu]

        operador_count = 0
        for menu in operador_menus:
            _, created = RoleMenuAccess.objects.get_or_create(
                role=operador_role, menu=menu, defaults={"is_active": True}
            )
            if created:
                operador_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"  ✓ {operador_count} permisos nuevos para Operador")
        )

        # ==================== RESUMEN ====================
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("✅ Configuración RBAC completada"))
        self.stdout.write("=" * 60)
        self.stdout.write(f"\n📊 Resumen:")
        self.stdout.write(f"  • Roles creados: {Role.objects.count()}")
        self.stdout.write(f"  • Menús creados: {Menu.objects.count()}")
        self.stdout.write(f"  • Permisos asignados: {RoleMenuAccess.objects.count()}")
        self.stdout.write(
            f"\n💡 Tip: Asigna un rol a tus usuarios con: user.rol = Role.objects.get(code='ADMIN')"
        )
        self.stdout.write(f"💡 Tip: Prueba la API en: GET /api/auth/navigation/\n")
