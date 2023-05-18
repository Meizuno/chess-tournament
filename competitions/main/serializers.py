from rest_framework import serializers


class PlayerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    unique_id = serializers.CharField(max_length=8)
    photo = serializers.ImageField()
    username = serializers.CharField(required=False)
    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField()
    date_of_birth = serializers.DateField(required=False)
    country = serializers.CharField(required=False)
    rating = serializers.IntegerField()

    # def get_photo(self, obj):
    #     if obj.photo:
    #         request = self.context.get('request')
    #         return request.build_absolute_uri(obj.photo.url)
    #     return None

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class TournamentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    unique_id = serializers.CharField(max_length=8)
    name = serializers.CharField(max_length=30, required=False)
    place = serializers.CharField(max_length=30, required=False)
    description = serializers.CharField(required=True)
    capacity = serializers.IntegerField(required=False)
    date_of_start = serializers.DateTimeField()
    date_of_end = serializers.DateTimeField()
    opened = serializers.BooleanField()
    players = PlayerSerializer(many=True)
    organizers = PlayerSerializer(many=True)

