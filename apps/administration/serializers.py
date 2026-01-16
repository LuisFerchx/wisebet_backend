from rest_framework import serializers
from .models import Agency

class AgencySerializer(serializers.ModelSerializer):
    id_display = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    house = serializers.CharField(source='betting_house')
    status = serializers.SerializerMethodField()
    rake_percentage_display = serializers.SerializerMethodField()
    movements_current_month = serializers.SerializerMethodField()
    ggr_current_month = serializers.SerializerMethodField()
    estimated_commission = serializers.SerializerMethodField()
    active_profiles_count = serializers.SerializerMethodField()
    missing_profiles_count = serializers.SerializerMethodField()
    alerts = serializers.SerializerMethodField()

    class Meta:
        model = Agency
        fields = [
            'id',
            'id_display',
            'owner',
            'house',
            'status',
            'rake_percentage',
            'rake_percentage_display',
            'movements_current_month',
            'ggr_current_month',
            'estimated_commission',
            'active_profiles_count',
            'missing_profiles_count',
            'alerts',
        ]

    def get_id_display(self, obj):
        return f"AG-{obj.id:03d}"

    def get_owner(self, obj):
        if obj.responsible and obj.responsible.user:
            return f"{obj.responsible.user.first_name} {obj.responsible.user.last_name}".strip() or obj.responsible.user.username
        return "Sin Asignar"

    def get_status(self, obj):
        return "ACTIVO" if obj.is_active else "BLOQUEADO"

    def get_rake_percentage_display(self, obj):
        return f"{int(obj.rake_percentage)}%"

    def get_movements_current_month(self, obj):
        # Sum of current_weekly_ops of all profiles for this agency
        return sum(profile.current_weekly_ops for profile in obj.profiles.all())

    def get_ggr_current_month(self, obj):
        # Placeholder as no transaction model exists
        return 0

    def get_estimated_commission(self, obj):
        # Placeholder
        return 0

    def get_active_profiles_count(self, obj):
        return obj.profiles.filter(is_active=True).count()

    def get_missing_profiles_count(self, obj):
        active_count = self.get_active_profiles_count(obj)
        return max(0, obj.min_recommended_profiles - active_count)

    def get_alerts(self, obj):
        alerts = []
        if self.get_missing_profiles_count(obj) > 0:
            alerts.append("FALTAN PERFILES")
        
        # Example condition for "CASA PERDIENDO"
        if self.get_ggr_current_month(obj) < 0:
            alerts.append("CASA PERDIENDO")
            
        return alerts
