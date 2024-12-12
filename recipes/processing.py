# Responsible for managing the current/new image based on radio button
def process_image_dict(data, cleaned_data):

    if 'maintain-image' not in data:
        return cleaned_data

    match(data['maintain-image']):
        case 'Delete Image':
            pass
        case 'Keep Image':
            cleaned_data.pop('image')

    return cleaned_data