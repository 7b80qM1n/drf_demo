from rest_framework import serializers
from . import models


# 课程分类
class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseCategory
        fields = ['id', 'name']


# 导师子序列化
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ['name', 'title', 'role_name', 'signature', 'image', 'brief']


# 全部课程
class CourseModelSerializer(serializers.ModelSerializer):
    # 子序列化
    teacher = TeacherSerializer()

    class Meta:
        model = models.Course
        fields = ['id', 'name', 'course_img', 'attachment_path', 'sections', 'price', 'brief', 'students',
                  'pub_sections', 'period', 'level_name', 'teacher', 'course_type_name', 'status_name', 'section_list']


# 课时子序列化
class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseSection
        fields = ['name', 'section_link', 'duration', 'free_trail', 'orders', 'section_type_name']


# 全部章节&课时
class CourseChapterSerializer(serializers.ModelSerializer):
    # 反向写related_name 章节下有多个课时many=True
    coursesections = SectionSerializer(many=True)

    class Meta:
        model = models.CourseChapter
        fields = ['name', 'summary', 'chapter', 'coursesections']
