from django.forms import ModelForm, NumberInput
from techtrends_fn.models import Ratings, Review

class RatingForm(ModelForm):
    class Meta:
        model=Ratings
        fields=['score']
        widgets = {
            'score': NumberInput(attrs={
                'min':'1',
                'max':'5',
                'step':'0.1'
            })
         }
    

class ReviewForm(ModelForm):
    class Meta:
        model=Review
        fields=['content']