from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    start_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Task
        fields = ['title', 'description', 'start_date', 'end_date', 'completed']  # Include the fields you want in the form
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter task description'}),
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"placeholder": "Enter task title"})