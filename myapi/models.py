from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

# Create your models here.
class Hero(models.Model):
    name = models.CharField(max_length=60)
    alias = models.CharField(max_length=60)
    
    def __str__(self):
        return self.alias

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ['created']

class AssesmentItem(models.Model):
    question = models.TextField()
    assesment_category = models.CharField(max_length=100, choices = [('HW','Homework'),('CW','Classwork')])

    def __str__(self):        
        return self.question

class Answers(models.Model):
    question = models.ForeignKey(AssesmentItem,related_name="answers", on_delete=models.CASCADE)
    answer = models.CharField(max_length=50)
    correct_answer = models.BooleanField()
    feedback = models.CharField(max_length=50)

    def __str__(self):        
        return self.question.question