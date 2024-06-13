from django import forms
from askme_app.models import User, Profile, Question, Tag, Answer
from django.core.exceptions import ValidationError
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import auth


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        user = auth.authenticate(request=self.request, **self.cleaned_data)
        if user is None:
            self.add_error(field=None, error="Wrong username or password!")


class SettingsForm(forms.Form):
    username = forms.CharField(disabled=True)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, label="Password confirmation")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New password if need", required=False)
    password_check = forms.CharField(widget=forms.PasswordInput, label="Repeat password", required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SettingsForm, self).__init__(*args, **kwargs)

    def clean_password_check(self):
        new_password = self.cleaned_data['new_password']
        password_for_checking = self.cleaned_data['password_check']
        if password_for_checking != new_password:
            raise ValidationError("Passwords don't match!")
        return password_for_checking
    avatar = forms.ImageField(required=False)

    def clean_password(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(request=self.request, username=username, password=password)
        if user is None:
            raise ValidationError("The old password is incorrect!")
        return password

    def update(self):
        data = self.cleaned_data

        username = data['username']
        new_password = data['new_password']
        avatar = data['avatar']

        data.pop('username')
        data.pop('password')
        data.pop('new_password')
        data.pop('password_check')
        data.pop('avatar')

        User.objects.filter(username=username).update(**data)

        user_tmp = User.objects.get(username=username)
        if not user_tmp:
            self.add_error(field=None, error="User updating error!")
            return None

        profile = Profile.manager.filter(user_id=user_tmp.id).update(avatar=avatar)
        if not profile:
            self.add_error(field=None, error="Profile updating error!")
            return None

        if new_password != '':
            user_tmp.set_password(new_password)
            user_tmp.save()

            test_auth_user = auth.authenticate(request=self.request, username=username, password=new_password)
            if test_auth_user is not None:
                auth_login(self.request, test_auth_user)
            else:
                self.add_error(field=None, error="User authenticating error!")

        return user_tmp


class SignUpForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(label="Repeat password", widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    def __init__(self, *args, user_id=0, **kwargs):
        self.user_id = user_id
        super(SignUpForm, self).__init__(*args, **kwargs)

    def clean_password_check(self):
        password = self.cleaned_data['password']
        password_for_checking = self.cleaned_data['password_check']
        if password_for_checking != password:
            raise ValidationError("Passwords don't match!")
        return password_for_checking

    def save(self):
        data = self.cleaned_data

        avatar = data['avatar']
        data.pop('avatar')
        data.pop('password_check')

        user = User.objects.create_user(**data)
        if not user:
            self.add_error("User saving error!")
            return None

        profile = Profile.manager.create(avatar=avatar, user_id=user.id)
        if not profile:
            self.add_error("Profile saving error!")
            return None

        return user

class AskForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, max_length=255)
    tags = forms.CharField(required=False, help_text="Enter up to three tags separated by a space")

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def __init__(self, *args, **kwargs):
        self.profile_id = kwargs.pop('profile_id', None)
        super(AskForm, self).__init__(*args, **kwargs)

    def clean_tags(self):
        input_tags = self.cleaned_data['tags']
        tags = input_tags.split()
        if len(tags) > 3:
            raise ValidationError("More than three tags have been entered!")
        for i in range(len(tags)):
            for j in tags[i]:
                if not j.isalpha() and not j.isdigit():
                    raise  ValidationError(f"The {i + 1} tag is incorrect")
        return input_tags

    def save(self):
        title, text, tags = self.cleaned_data['title'], self.cleaned_data['text'], self.cleaned_data['tags']
        new_question = Question(title=title, text=text, profile_id=self.profile_id)
        new_question.save()

        if not new_question:
            self.add_error(field=None, error="Question saving error!")
            return None

        for tag in tags.split():
            some_tag = Tag.manager.update_or_create(name=tag)[0]
            if not some_tag:
                self.add_error(field=None, error="Tag saving error!")
                return None

            new_question.tags.add(some_tag)

        return new_question


class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, max_length=255, label="Enter your answer here")

    def __init__(self, *args, **kwargs):
        self.question_id = kwargs.pop('question_id', None)
        self.profile_id = kwargs.pop('profile_id', None)
        super(AnswerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Answer
        fields = ['text']

    def save(self):
        text = self.cleaned_data['text']
        answer = Answer.manager.create(text=text, profile_id=self.profile_id, question_id=self.question_id)
        if not answer:
            self.add_error(field=None, error="User saving error!")
            return None
        return answer
