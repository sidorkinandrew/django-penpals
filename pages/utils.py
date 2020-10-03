LANGUAGE_CHOICES = (
    (1, 'English'),
    (2, 'Spanish'),
    (3, 'German'),
    (4, 'Swedish'),
    (5, 'Chinese'),
    (6, 'Italian'),
    (7, 'Polish'),
)

def from_value_to_label(field):
    if field is not None:
        list_of_labels = [label for value, label in LANGUAGE_CHOICES if str(value) in field]
        return ", ".join(list_of_labels)  # list_of_labels  #ast.literal_eval(field)  # [int(i) for i in field.replace('[','').replace(']','').replace(',','').replace("'",'').split(" ")] # list_of_labels #
    return field

def from_label_to_value(field):
    if field is not None:
        list_of_values = [value for value, label in LANGUAGE_CHOICES if label in field]
        return list_of_values  # list_of_labels  #ast.literal_eval(field)  # [int(i) for i in field.replace('[','').replace(']','').replace(',','').replace("'",'').split(" ")] # list_of_labels #
    return field
