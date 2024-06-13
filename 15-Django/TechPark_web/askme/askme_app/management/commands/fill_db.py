from askme_app.models import Tag, Profile, Question, Answer, QuestionLike, AnswerLike
from django.core.management.base import BaseCommand
from itertools import islice
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Заполняем бд'

    STEP = 10
    RATIO = 100


    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='?', type=int, default=self.RATIO, help='Количество')


    def fill_questions_likes(self, ratio):
        profiles = Profile.manager.all()
        questions = Question.manager.all()

        batch_size = 100
        objs = []

        iter = 0
        for i in profiles:
            for j in questions:
                question_like = QuestionLike()
                question_like.who_liked = i
                question_like.question = j
                objs.append(question_like)
            iter += 1
            objs = (y for y in objs)
            QuestionLike.manager.bulk_create(objs)
            iter = 0
            objs = []


    def fill_answers_likes(self, ratio):
        profiles = Profile.manager.all()
        answers = Answer.manager.all()

        batch_size = 100
        objs = []

        iter = 0
        for i in profiles:
            for j in answers:
                answer_like = AnswerLike()
                answer_like.who_liked = i
                answer_like.answer = j
                objs.append(answer_like)
            iter += 1
            objs = (y for y in objs)
            AnswerLike.manager.bulk_create(objs)
            iter = 0
            objs = []


    def fill_profiles(self, ratio):
        users = User.objects.all()
        batch_size = self.STEP
        objs = (Profile(user=users[i], avatar="img_avatar.png") for i in range(ratio))
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Profile.manager.bulk_create(batch, batch_size)


    def fill_users(self, ratio):
        batch_size = self.STEP
        objs = (User(username='SomeNickname%s' % i, email='SomeEmail%s@gmail.com' % i, password='SomePassword%s' % i) for i in range(ratio))
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            User.objects.bulk_create(batch, batch_size)


    def fill_tags(self, ratio):
        batch_size = self.STEP
        objs = (Tag(name='Tag %s' % i) for i in range(ratio))
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Tag.manager.bulk_create(batch, batch_size)


    def create_question(self, curr_idx, ratio, some_profile):
        quest = Question()
        quest.title = 'Question #%s' % curr_idx
        quest.text = 'Text of the question #%s' % curr_idx
        quest.author = some_profile
        return quest


    def fill_questions(self, ratio):
        profiles = Profile.manager.all()
        batch_size = self.STEP
        objs = (self.create_question(i, ratio, profiles[i % ((ratio - 1) // 10 + 1)]) for i in range(ratio))
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Question.manager.bulk_create(batch, batch_size)


    def add_tags_to_questions(self):
        try:
            questions = Question.manager.all()
            three_tags = Tag.manager.all()[4:7]
            batch_size = self.STEP
            objs = []
            for question in questions:
                for some_tag in three_tags:
                    question.tags.add(some_tag)
                objs.append(question)

            while True:
                batch = list(islice(objs, batch_size))
                if not batch:
                    break
                Question.manager.bulk_update(batch, batch_size)
        except Exception as e:
            print(e)
            pass


    def fill_answers(self, ratio):
        profiles = Profile.manager.all()
        questions = Question.manager.all()
        batch_size = 100
        objs = []
        i = 0
        for profile in profiles:
            for question in questions:
                answer = Answer(text='Some text of the answer #%s' % i, marked_as_correct=bool(i))
                i += 1
                answer.author = profile
                answer.question = question
                objs.append(answer)

        objs = (y for y in objs)
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Answer.manager.bulk_create(batch, batch_size)

    #
    # def fill_answers(self, ratio):
    #     profiles = Profile.manager.all().select_related()
    #     questions = Question.manager.all().select_related()
    #     batch_size = 10000
    #
    #     objs = (Answer(text='Some text of the answer #%s' % i, marked_as_correct=bool(i),
    #                    author=profile, question=question)
    #             for i, profile in enumerate(profiles)
    #             for question in questions)
    #
    #     with transaction.atomic():
    #         while True:
    #             batch = list(islice(objs, batch_size))
    #             if not batch:
    #                 break
    #             try:
    #                 Answer.manager.bulk_create(batch, batch_size)
    #             except Exception as e:
    #                 print(f"Error: {e}")


    def update_tags_name(self):
        TAGS = Tag.manager.all()
        i = 0
        for tag in TAGS:
            tag.name = f"Tag{i}"
            i += 1
            tag.save()

    def handle(self, *args, **options):
        ratio = options['ratio']
        # print(f"ratio = {ratio}")
        # Tag.manager.all().delete()
        # print("TAGS WILL FILL")
        # self.fill_tags(ratio + 1)
        # print("TAGS FILLED")

        # User.objects.all().delete()
        # print("USERS WILL FILL")
        # self.fill_users(ratio + 1)
        # print("USERS FILLED")

        # Profile.manager.all().delete()
        # print("PROFILES WILL FILL")
        # self.fill_profiles(ratio + 1)
        # print("PROFILES FILLED")

        # Question.manager.all().delete()
        # print("QUESTIONS WILL FILL")
        # self.fill_questions(ratio * 10 + 1)
        # print("QUESTIONS FILLED")
        # print("QUESTIONS WILL UPDATE")
        # self.add_tags_to_questions()
        # print("QUESTIONS UPDATED")

        # Answer.manager.all().delete()
        # print("ANSWERS WILL FILL")
        # self.fill_answers(ratio * 100 + 1)
        # print("ANSWERS FILLED")
        #
        # QuestionLike.manager.all().delete()
        # print("VoteQuestion WILL FILL")
        # self.fill_questions_likes(ratio * 100 + 1)
        # print("VoteQuestion FILLED")

        # AnswerLike.manager.all().delete()
        # print("VoteQuestion WILL FILL")
        # self.fill_answers_likes(ratio * 100 + 1)
        # print("VoteQuestion FILLED")
        # print(Tag.manager.top_of_tags(10))

