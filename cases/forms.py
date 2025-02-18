from django import forms

from utils.enum import DocumentType
from .models import Case, Document

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field,HTML
from .models import Case, Document


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = [
            "title",
            "client",
            "case_type",
            "status",
            "description",
            "assigned_lawyer",
            "assigned_users",
        ]

        widgets = {
            "case_type": forms.CheckboxSelectMultiple(),
            "assigned_users": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assigned_users"].label = "Support Users"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("title", css_class="col-md-6"),
                Column("client", css_class="col-md-6"),
            ),
            Row(
                Column("case_type", css_class="col-md-6"),
                Column("status", css_class="col-md-6"),
            ),
            Row(
                Column("assigned_lawyer", css_class="col-md-6"),
                Column("assigned_users", css_class="col-md-6"),
            ),
            "description",
            Submit("submit", "Save Case", css_class="btn btn-primary"),
        )

class DocumentForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    title = forms.CharField(required=False)
    document_type = forms.ChoiceField(
        choices=DocumentType.choices, required=False, widget=forms.Select
    )
    file = forms.FileField(required=False, widget=forms.FileInput)
    description = forms.CharField(
        widget=forms.Textarea(attrs={"cols": 3, "rows": 3}), required=False
    )

    class Meta:
        model = Document
        fields = ['id', "title", "document_type", "file", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['id'].initial = self.instance.pk
            
        if self.instance and self.instance.pk and self.instance.file:
            self.fields["file"].help_text = (
                f'<small><a href="{self.instance.file.url}" target="_blank">{self.instance.file.name}</a></small>'
            )

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('id'),
            Row(
                Column("title", css_class="col-md-3"),
                Column("document_type", css_class="col-md-3"),
                Column("file", css_class="col-md-6"),
                Column("description", css_class="col-md-12"),
            ),
            HTML("{% if form.instance.pk %}{{ form.DELETE }}{% endif %}")
        )

    def clean(self):
        cleaned_data = super().clean()
        # Allow documents with only file or title/description populated (don't require all fields)
        if not cleaned_data.get('id') and not cleaned_data.get('DELETE', False):
            if not any(cleaned_data.get(field) for field in ['title', 'document_type', 'file', 'description']):
                raise forms.ValidationError("At least one field must be filled for new documents.")
        return cleaned_data

# class DocumentForm(forms.ModelForm):
#     id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
#     title = forms.CharField(required=False)
#     document_type = forms.ChoiceField(
#         choices=DocumentType.choices, required=False, widget=forms.Select
#     )
#     file = forms.FileField(required=False, widget=forms.FileInput)
#     description = forms.CharField(
#         widget=forms.Textarea(attrs={"cols": 3, "rows": 3}), required=False
#     )

#     class Meta:
#         model = Document
#         fields = ['id', "title", "document_type", "file", "description"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance and self.instance.pk:
#             self.fields['id'].initial = self.instance.pk
            
#         if self.instance and self.instance.pk and self.instance.file:
#             self.fields["file"].help_text = (
#                 f'<small><a href="{self.instance.file.url}" target="_blank">{self.instance.file.name}</a></small>'
#             )

#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Field('id'),
#             Row(
#                 Column("title", css_class="col-md-3"),
#                 Column("document_type", css_class="col-md-3"),
#                 Column("file", css_class="col-md-6"),
#                 Column("description", css_class="col-md-12"),
#             ),
#             HTML("{% if form.instance.pk %}{{ form.DELETE }}{% endif %}")
#         )
#     def clean(self):
#         cleaned_data = super().clean()
#         if not cleaned_data.get('id') and not cleaned_data.get('DELETE', False):
#             if not any(cleaned_data.get(field) for field in ['title', 'document_type', 'file', 'description']):
#                 raise forms.ValidationError("At least one field must be filled for new documents.")
#         return cleaned_data
