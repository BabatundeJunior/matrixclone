from django import forms
from .models import Trade

class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ['trade_date', 'pair', 'entry_price', 'exit_price', 'position_size', 'trade_type', 'notes']
        widgets = {
            'trade_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),

        }
