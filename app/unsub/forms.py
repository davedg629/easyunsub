from flask_wtf import Form
from wtforms import SelectMultipleField, SubmitField
from wtforms import widgets
from wtforms.validators import DataRequired


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class UnsubForm(Form):
    subreddits = MultiCheckboxField(
        'Check the the subreddits to unsubscribe from',
        validators=[DataRequired()]
    )
    submit = SubmitField('Unsubscribe')


class UnsubConfirmForm(Form):
    submit = SubmitField('Unsubscribe Now')
