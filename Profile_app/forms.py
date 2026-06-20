from django import forms
from Profile_app.models import Profile

PROGRAM_CHOICES = [
    ('B.A. Theology and Mission', 'Theology and Mission (Faculty of Theology and Mission)'),
    ('B.Sc. Business Administration (Human Resource Management)', 'Management (Faculty of Business Administration)'),
    ('B.Sc. Business Administration (Logistics and Supply Chain Management)', 'Economics, Marketing and Services (Faculty of Business Administration)'),
    ('B.Sc. Construction Technology and Engineering Management', 'Built Environment (Faculty of Engineering Science and Computing)'),
    ('B.Sc. Information Technology', 'Accounting and Finance (Faculty of Engineering Science and Computing)'),
    ('B.Sc. Midwifery', 'Nursing and Midwifery (Faculty of Health and Allied Sciences)'),
    ('B.Sc. Nursing', 'Nursing and Midwifery (Faculty of Health and Allied Sciences)'),
    ('B.Sc. Physician Assistant Studies', 'Physician Assistantship – Medical (Faculty of Health and Allied Sciences)'),
    ('B.Sc. Quantity Surveying and Building Economics', 'Built Environment (Faculty of Engineering Science and Computing)'),
    ('Bachelor of Commerce (Accounting with Computing)', 'Accounting and Finance (Faculty of Business Administration)'),
    ('Bachelor of Laws (LL.B)', 'Law (Faculty of Law)'),
    ('BSc Health Information Management', 'Nursing and Midwifery (Faculty of Health and Allied Sciences)'),
    ('BSc Industrial Software Engineering', 'Information Technology (Faculty of Engineering Science and Computing)'),
]

class PhoneForm(forms.ModelForm):
    program = forms.ChoiceField(choices=PROGRAM_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['phone', 'faculty']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number',
                'required': 'required'
            }),
            'faculty': forms.Select(choices=PROGRAM_CHOICES, attrs={'class': 'form-control'})
        }
