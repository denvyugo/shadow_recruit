"""models for mainapp"""
from random import shuffle
from django.db import models

QUIZ_LIMIT = 2  # quantity of questions in quiz


class Planet(models.Model):
    """class for Planet"""
    name = models.CharField(verbose_name="Planet's name", max_length=64)

    def __str__(self):
        return f"Planet '{self.name}'"


class Sith(models.Model):
    """class for Sith"""
    MAX_RECRUIT = 2

    planet = models.ForeignKey(Planet, on_delete=models.PROTECT)
    name = models.CharField(verbose_name='Name', max_length=64)

    def number_recruits(self):
        recruits = self.recruits.select_related()
        return len(recruits)

    def __str__(self):
        return f'Sith {self.name}'


class Recruit(models.Model):
    """class for Recruit"""
    planet = models.ForeignKey(Planet, on_delete=models.PROTECT)
    name = models.CharField(max_length=64)
    age = models.PositiveIntegerField()
    email = models.EmailField()
    master = models.ForeignKey(Sith, related_name="recruits",
                               on_delete=models.PROTECT, null=True, blank=True)

    def make_task(self):
        """
        create task for recruit
        :return recruit_task:
        """
        recruit_task = Task(recruit_id=self.id)
        recruit_task.save()
        questions = Question.get_random_id()
        print(questions)
        for question_id in questions:
            quiz = Quiz(task_id=recruit_task.id, question_id=question_id)
            quiz.save()
        return recruit_task

    def last_task_status(self):
        last_task_id = \
             Task.objects.filter(recruit_id=self.id).aggregate(models.Max('id'))
        task = Task.objects.get(id=last_task_id['id__max'])
        return task.task_done


class Question(models.Model):
    """class for question for task"""
    question = models.TextField(verbose_name='Text of question', blank=False, unique=True)

    def __str__(self):
        return self.question

    @staticmethod
    def get_random_id():
        """get random question from data base"""
        _items = Question.objects.all()
        print('QUESTIONS:', _items)
        _list_id = list(map(lambda x: x.id, _items))
        shuffle(_list_id)
        print(len(_list_id))
        if len(_list_id) < QUIZ_LIMIT:
            return _list_id
        return _list_id[:QUIZ_LIMIT]


class Answers(models.Model):
    """answers on questions for task"""
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    version = models.TextField(verbose_name='Version of answer', blank=False)
    is_right = models.BooleanField(verbose_name='Is this answer right')


class Task(models.Model):
    """class for the task for each recruit"""
    recruit = models.ForeignKey(Recruit, on_delete=models.PROTECT)
    task_date = models.DateField(auto_now_add=True)
    task_done = models.BooleanField(default=False)

    def check_done(self, versions):
        """
        check if all answers on questions in quiz are right
        :param versions: list of answers' ids
        :return:
        """
        is_done = False
        for answer_id in versions:
            answer = Answers.objects.filter(pk=answer_id).first()
            is_done = answer.is_right
            if not is_done: break
        self.task_done = is_done
        self.save()

    @staticmethod
    def get_last_tasks():
        """get the latest tasks from db group by free (w.o. master) recruit"""
        # tasks = Task.objects.raw('''
        #                 SELECT mainapp_task.id, mainapp_task.recruit_id,
        #                 mainapp_task.task_date, mainapp_task.task_done
        #                 FROM mainapp_task
        #                 INNER JOIN mainapp_recruit
        #                 ON mainapp_task.recruit_id = mainapp_recruit.id
        #                 WHERE mainapp_recruit.master_id Is Null
        #                 GROUP BY mainapp_task.recruit_id
        #                 HAVING Max(mainapp_task.id) = mainapp_task.id
        #                 ''')
        tasks = Task.objects.raw('''
                                SELECT mainapp_task.id, mainapp_task.recruit_id, 
                                mainapp_task.task_date, mainapp_task.task_done
                                FROM mainapp_task
                                ''')
        return tasks

    def __str__(self):
        return f'Task for {self.recruit.name}, status is {self.task_done}'


class Quiz(models.Model):
    """class for list of questions of task"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
