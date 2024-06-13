from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count

class ProfileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(question_count=Count('questions')).order_by('-question_count')

    def top_of_profiles(self, n):
        return Profile.manager.annotate(Count('answers')).order_by('-answers__count')[:n]

    def existence_username(self, username):
        return User.objects.filter(username=username).exists()

    def get_user_by_id(self, user_id):
        return User.objects.get(pk=user_id)

    def get_profile_by_user_id(self, user_id):
        return Profile.manager.get(user_id=user_id)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="static/img", null=True, blank=True)
    manager = ProfileManager()

    def __str__(self):
        return f'Profile {self.user.username}'


class TagManager(models.Manager):
    def get_questions_by_tag(self, tag_name):
        tag = Tag.manager.get(name=tag_name)
        return tag.questions.all()

    def top_of_tags(self, n):
        return self.get_queryset().annotate(num_questions=Count('questions')).order_by('-num_questions')[:n]

    def get_tag_by_name(self, tag_name):
        return Tag.objects.get(name=tag_name)

class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    manager = TagManager()

    def __str__(self):
        return f"Tag {self.name}"

# ВОПРОСЫ
class QuestionLikeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()

    def like_this_question(self, user, question):
        # Проверяем, лайкал ли пользователь этот вопрос
        if self.filter(who_liked=user, question=question).exists():
            # Если да, то отменяем лайк
            self.filter(who_liked=user, question=question).delete()
        else:
            # Если нет, то ставим лайк
            self.create(who_liked=user, question=question)

class QuestionLike(models.Model):
    who_liked = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='question_likes')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='question_likes')

    manager = QuestionLikeManager()

    class Meta:
        unique_together = ['question', 'who_liked']

class QuestionManager(models.Manager):
    def get_new_questions(self):
        return Question.manager.all().order_by('pub_date')

    def get_top_questions(self):
        return self.get_queryset().annotate(num_likes=Count('question_likes')) \
                   .order_by('-num_likes') \
                   .prefetch_related('question_likes')

    def get_count_of_questions(self):
        return Question.manager.all().count()

    def get_question_by_id(self, id):
        return Question.manager.get(pk=id)


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=50)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='questions')

    manager = QuestionManager()

    def __str__(self):
        return f"Question {self.title}"

    def get_likes_count(self):
        return self.question_likes.count()

    def get_answers_count(self):
        return self.answers.count()

    def get_tags(self):
        return self.tags.all()

    def get_answers(self):
        return self.answers.all()


# ОТВЕТЫ
class AnswerLikeManager(models.Manager):
    def like_this_answer(self, user, answer):
        # Проверяем, лайкал ли пользователь этот ответ
        if self.filter(who_liked=user, answer=answer).exists():
            # Если да, то отменяем лайк
            self.filter(who_liked=user, answer=answer).delete()
        else:
            # Если нет, то ставим лайк
            self.create(who_liked=user, answer=answer)

class AnswerLike(models.Model):
    who_liked = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='answer_likes')
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='answer_likes')

    manager = AnswerLikeManager()

    class Meta:
        unique_together = ['answer', 'who_liked']

class AnswerManager(models.Manager):
    pass


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    marked_as_correct = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now=True)

    manager = AnswerManager()

    def __str__(self):
        return f"Answer {self.text}"

    def get_likes_count(self):
        return self.answer_likes.count()

    def get_correctness(self):
        return self.marked_as_correct

