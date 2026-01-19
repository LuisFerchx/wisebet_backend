from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    LoginResponseSerializer,
)
from drf_spectacular.utils import extend_schema

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration
    """

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @extend_schema(
        responses={201: LoginResponseSerializer},
        description="Register a new user and return tokens",
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "User registered successfully",
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    API endpoint for user login
    """

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @extend_schema(
        responses={200: LoginResponseSerializer},
        description="Login with username/email and password",
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        identifier = serializer.validated_data["identifier"]
        password = serializer.validated_data["password"]

        # Try to determine if identifier is email or username
        user = None

        # Check if it's an email format
        if "@" in identifier:
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        else:
            # Try as username
            user = authenticate(username=identifier, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": UserSerializer(user).data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "message": "Login successful",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    """
    API endpoint for user logout
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to retrieve and update user profile
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """
    API endpoint for changing user password
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        # Check old password
        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"error": "Old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Set new password
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"message": "Password changed successfully"}, status=status.HTTP_200_OK
        )


class UserNavigationView(APIView):
    """
    API endpoint to get user navigation based on role permissions
    Returns menus and their children that the user has access to
    """

    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={200: "UserNavigationResponseSerializer"},
        description="Get navigation menus based on user's role permissions",
    )
    def get(self, request):
        user = request.user

        # Check if user has a role assigned
        if not user.rol:
            return Response(
                {
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "nombre_completo": user.nombre_completo,
                        "rol": None,
                    },
                    "navigation": [],
                },
                status=status.HTTP_200_OK,
            )

        # Import models here to avoid circular imports
        from .models import Menu, RoleMenuAccess, Section
        from .serializers import UserSerializer, MenuSerializer

        # Get all menu accesses for this role
        role_menu_accesses = (
            RoleMenuAccess.objects.filter(
                role=user.rol, is_active=True, menu__is_active=True
            )
            .select_related("menu")
            .distinct()
        )

        # Get unique menu IDs that the user has access to
        accessible_menu_ids = set(access.menu.id for access in role_menu_accesses)

        # Get all parent menus (menus without parent) that user has access to
        parent_menus = Menu.objects.filter(
            id__in=accessible_menu_ids, parent__isnull=True, is_active=True
        ).order_by("order", "name")

        # Serialize the navigation
        navigation_data = []
        for menu in parent_menus:
            menu_data = {
                "id": menu.id,
                "name": menu.name,
                "code": menu.code,
                "icon": menu.icon,
                "route": menu.route,
                "order": menu.order,
                "children": [],
                "sections": [],
            }

            # Get sections for this menu
            sections = menu.sections.filter(is_active=True).order_by("order", "name")
            for section in sections:
                menu_data["sections"].append(
                    {
                        "id": section.id,
                        "name": section.name,
                        "code": section.code,
                        "icon": section.icon,
                        "route": section.route,
                        "order": section.order,
                    }
                )

            # Get children menus that user has access to
            children = menu.children.filter(
                id__in=accessible_menu_ids, is_active=True
            ).order_by("order", "name")

            for child in children:
                child_data = {
                    "id": child.id,
                    "name": child.name,
                    "code": child.code,
                    "icon": child.icon,
                    "route": child.route,
                    "order": child.order,
                    "children": [],
                    "sections": [],
                }

                # Get sections for this child menu
                child_sections = child.sections.filter(is_active=True).order_by(
                    "order", "name"
                )
                for section in child_sections:
                    child_data["sections"].append(
                        {
                            "id": section.id,
                            "name": section.name,
                            "code": section.code,
                            "icon": section.icon,
                            "route": section.route,
                            "order": section.order,
                        }
                    )

                menu_data["children"].append(child_data)

            navigation_data.append(menu_data)

        return Response(
            {"user": UserSerializer(user).data, "navigation": navigation_data},
            status=status.HTTP_200_OK,
        )
