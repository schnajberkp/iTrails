from django import forms
from .models import Review, Trail, Trip

# Form for users to create a review for a trail

class ReviewForm(forms.ModelForm):
    # Users can rate a trail and leave a comment
    class Meta: #Inner class is linked to the Review model
        model = Review 
        fields = ["rating", "comment"] 
        widgets = { 
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "comment": forms.Textarea(attrs={"rows": 4}),
        }
# Form for users to plan a trip to a trail
class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ["trail", "date", "note"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }