from django import forms
from datetime import date

class CandidateForm(forms.Form):
    first_name = forms.CharField(label="Ім'я", min_length=2, max_length=30)
    last_name = forms.CharField(label="Прізвище", min_length=2, max_length=30)
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Телефон", min_length=13, max_length=13)
    birth_date = forms.DateField(label="Дата народження", widget=forms.DateInput(attrs={"type": "date"}))
    position = forms.ChoiceField(label="Позиція", choices=[
        ("frontend", "Frontend"),
        ("backend", "Backend"),
        ("fullstack", "Fullstack"),
        ("design", "Design"),
    ])
    experience = forms.ChoiceField(label="Досвід роботи", choices=[
        ("none", "Немає досвіду"),
        ("less1", "Менше 1 року"),
        ("1to3", "1–3 роки"),
        ("3plus", "Більше 3 років"),
    ], widget=forms.RadioSelect)
    skills = forms.MultipleChoiceField(label="Технології", choices=[
        ("React", "React"),
        ("TypeScript", "TypeScript"),
        ("Node.js", "Node.js"),
        ("Git", "Git"),
        ("Docker", "Docker"),
    ], widget=forms.CheckboxSelectMultiple)
    salary_expected = forms.IntegerField(label="Бажана зарплата", required=False, min_value=5000, max_value=200000)
    start_date = forms.DateField(label="Готовий розпочати з", required=False, widget=forms.DateInput(attrs={"type": "date"}))
    portfolio_url = forms.URLField(label="Портфоліо або GitHub", required=False)
    cover_letter = forms.CharField(label="Супровідний лист", widget=forms.Textarea, required=False)
    agree_to_terms = forms.BooleanField(label="Я погоджуюсь з умовами")

    def clean_birth_date(self):
        birth_date = self.cleaned_data["birth_date"]
        age = date.today().year - birth_date.year
        if age < 16 or age > 60:
            raise forms.ValidationError("Кандидат повинен бути від 16 до 60 років.")
        return birth_date

    def clean_skills(self):
        skills = self.cleaned_data["skills"]
        if len(skills) < 2 or len(skills) > 4:
            raise forms.ValidationError("Оберіть від 1 до 4 технологій.")
        return skills

    def clean_start_date(self):
        start_date = self.cleaned_data.get("start_date")
        if start_date and start_date < date.today():
            raise forms.ValidationError("Дата не може бути в минулому.")
        return start_date

    def clean_cover_letter(self):
        letter = self.cleaned_data.get("cover_letter", "")
        if letter and len(letter) < 50:
            raise forms.ValidationError("Супровідний лист має містити мінімум 50 символів.")
        return letter