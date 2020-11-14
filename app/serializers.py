from uuid import uuid4
from multiprocessing import Process

from rest_framework import serializers

from app.models import MediaFile
from app.utils.video_processing import convert_video, get_processing_progress


class ConverterSerializer(serializers.ModelSerializer):
    status = serializers.CharField(default=serializers.CreateOnlyDefault("UPLOAD_COMPLETE"), max_length=16)
    guid = serializers.UUIDField(default=serializers.CreateOnlyDefault(uuid4))
    progress = serializers.SerializerMethodField()

    class Meta:
        fields = "__all__"
        write_only_fields = ("input_file",)
        read_only_fields = ("guid", "status", "created_time", "updated_time", "output_file", "progress")
        model = MediaFile

    @staticmethod
    def get_progress(obj):
        return get_processing_progress(str(obj.guid))

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        guid, output_format = str(instance.guid), instance.output_format
        Process(target=convert_video, args=(guid, output_format)).start()
        return instance
