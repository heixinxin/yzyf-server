from rest_framework import serializers
from homeapi.models import ApplyJob, HomeJob


class ApplyJobSerializer(serializers.HyperlinkedModelSerializer):
    job = serializers.ReadOnlyField(source='job.id')
    # user = serializers.ReadOnlyField(source='owner.username')
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = ApplyJob
        fields = ('id', 'job', 'name', 'gender', 'age', 'card_id', 'number', 'status', 'create_time')
