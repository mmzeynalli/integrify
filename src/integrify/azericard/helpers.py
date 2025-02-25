from integrify.schemas import DryResponse


def json_to_html_form(json_data: DryResponse, with_submit: bool = True) -> str:
    """AzeriCard-ə göndərilməli datanı HTML formuna çevirən funksiya

    Args:
        json_data: DryResponse payload
        with_submit: HTML form-da submit butonunu elavə etmə(mə)k
    """

    url = json_data['url']
    verb = json_data['verb']
    data = json_data['data']

    # Create HTML form based on keys and values of json_data. Every field is str, str.
    form = '\n'.join(
        f'<input type="hidden" name="{key}" value="{value}">' for key, value in data.items()
    )

    return (
        f'<form action="{url}" method="{verb}">\n{form}\n'
        f'{'<input type="submit" value="Submit">\n' if with_submit else ''}</form>'
    )
