from django.db import models
from utils.models import BaseModel


class CourseCategory(BaseModel):
    """分类"""
    name = models.CharField(verbose_name="分类名称", max_length=64, unique=True)

    class Meta:
        db_table = "luffy_course_category"
        verbose_name = "分类"
        verbose_name_plural = "分类"

    def __str__(self):
        return self.name


class Course(BaseModel):
    """课程"""
    course_type = (
        (0, '付费'),
        (1, 'VIP专享'),
        (2, '学位课程')
    )
    level_choices = (
        (0, '初级'),
        (1, '中级'),
        (2, '高级'),
    )
    status_choices = (
        (0, '上线'),
        (1, '下线'),
        (2, '预上线'),
    )
    name = models.CharField(verbose_name="课程名称", max_length=128)
    course_img = models.ImageField(verbose_name="封面图片", upload_to="course", max_length=255, blank=True, null=True)
    course_type = models.SmallIntegerField(verbose_name="付费类型", choices=course_type, default=0)
    # 使用这个字段的原因
    brief = models.TextField(verbose_name="详情介绍", max_length=2048, null=True, blank=True)
    level = models.SmallIntegerField(verbose_name="难度等级", choices=level_choices, default=0)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)
    period = models.IntegerField(verbose_name="建议学习周期(day)", default=7)
    attachment_path = models.CharField(verbose_name="课件路径", max_length=128, blank=True,
                                       null=True)
    status = models.SmallIntegerField(verbose_name="课程状态", choices=status_choices, default=0)
    price = models.DecimalField(verbose_name="课程原价", max_digits=6, decimal_places=2, default=0)

    students = models.IntegerField(verbose_name="学习人数", default=0)
    sections = models.IntegerField(verbose_name="总课时数量", default=0)
    pub_sections = models.IntegerField(verbose_name="课时更新数量", default=0)

    teacher = models.ForeignKey(verbose_name="授课老师", to="Teacher", on_delete=models.DO_NOTHING, null=True, blank=True,
                                db_constraint=False)
    course_category = models.ForeignKey(verbose_name="课程分类", to="CourseCategory", on_delete=models.SET_NULL,
                                        db_constraint=False, null=True, blank=True)

    keyword = models.TextField(verbose_name="搜索关键词", help_text='搜索关键词', max_length=2048, null=True, blank=True)

    class Meta:
        db_table = "luffy_course"
        verbose_name = "课程"
        verbose_name_plural = "课程"

    def __str__(self):
        return self.name

    @property
    def level_name(self):
        return self.get_level_display()

    @property
    def course_type_name(self):
        return self.get_course_type_display()

    @property
    def status_name(self):
        return self.get_status_display()

    @property
    def section_list(self):
        section_l = []
        # 课程获取所有章节
        course_chapter_list = self.coursechapters.all()
        for course_chapter in course_chapter_list:
            # 章节获取所有课时
            course_section_list = course_chapter.coursesections.all()
            for course_section in course_section_list:
                section_l.append({
                    'name': course_section.name,
                    'section_link': course_section.section_link,
                    'duration': course_section.duration,
                    'free_trail': course_section.free_trail,
                })
        return section_l[:4]


class Teacher(BaseModel):
    """导师"""
    role_choices = (
        (0, '讲师'),
        (1, '导师'),
        (2, '班主任'),
    )
    name = models.CharField(verbose_name="导师名", max_length=32)
    role = models.SmallIntegerField(verbose_name="导师身份", choices=role_choices, default=0, )
    title = models.CharField(verbose_name="职位、职称", max_length=64)
    signature = models.CharField(verbose_name="导师签名", help_text="导师签名", max_length=255, blank=True, null=True)
    image = models.ImageField(verbose_name="导师封面", upload_to="teacher", null=True)
    brief = models.TextField(verbose_name="导师描述", max_length=1024)

    class Meta:
        db_table = "luffy_teacher"
        verbose_name = "导师"
        verbose_name_plural = "导师"

    def __str__(self):
        return self.name

    @property
    def role_name(self):
        return self.get_role_display()


class CourseChapter(BaseModel):
    """章节"""
    chapter = models.SmallIntegerField(verbose_name="第几章", default=1)
    name = models.CharField(verbose_name="章节标题", max_length=128)
    summary = models.TextField(verbose_name="章节介绍", blank=True, null=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)

    course = models.ForeignKey(verbose_name="课程名称", to="Course", related_name='coursechapters',
                               on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = "luffy_course_chapter"
        verbose_name = "章节"
        verbose_name_plural = "章节"

    def __str__(self):
        return f'{self.course}:(第{self.chapter}章){self.name}'


class CourseSection(BaseModel):
    """课时"""
    section_type_choices = (
        (0, '文档'),
        (1, '练习'),
        (2, '视频')
    )
    name = models.CharField(max_length=128, verbose_name="课时标题")
    orders = models.PositiveSmallIntegerField(verbose_name="课时排序")
    section_type = models.SmallIntegerField(verbose_name="课时种类", default=2, choices=section_type_choices)
    section_link = models.CharField(verbose_name="课时链接", max_length=255, blank=True, null=True,
                                    help_text="若是video，填vid,若是文档，填link")
    duration = models.CharField(verbose_name="视频时长", blank=True, null=True, max_length=32)  # 仅在前端展示使用
    pub_date = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    free_trail = models.BooleanField(verbose_name="是否可试看", default=False)

    chapter = models.ForeignKey(verbose_name="课程章节", to="CourseChapter", related_name='coursesections',
                                on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = "luffy_course_section"
        verbose_name = "课时"
        verbose_name_plural = "课时"

    def __str__(self):
        return f'{self.chapter}-{self.name}'

    def section_type_name(self):
        return self.get_section_type_display()
