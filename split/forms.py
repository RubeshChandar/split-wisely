from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        # fields = "__all__"
        exclude = ['group', 'created_by']
        widgets = {
            'paid_by': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        super().__init__(*args, **kwargs)
        self.fields["paid_by"].queryset = group.members.all()
        self.fields["paid_by"].label_from_instance = lambda user: str(
            user.username).capitalize()

        if group:
            self.initial['group'] = str(group)
            self.instance.group = group

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount <= 0:
            raise forms.ValidationError("Only positive number is allowed")

        return amount

    def save(self, commit=True, group=None, user=None):
        instance = super().save(commit=False)

        if not all([group, user]):
            raise ValueError("Group and User is found to be None")

        instance.group = group
        instance.created_by = user

        if commit:
            instance.save()

        return instance
