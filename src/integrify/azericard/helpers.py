from integrify.schemas import DryResponse


def json_to_html_form(json_data: DryResponse) -> str:
    """AzeriCard-ə göndərilməli datanı HTML formuna çevirən funksiya"""

    url = json_data['url']
    verb = json_data['verb']
    data: dict = json_data['data']

    # Create HTML form based on keys and values of json_data. Every field is str, str.
    form = '\n'.join(
        f'<input type="hidden" name="{key}" value="{value}">' for key, value in data.items()
    )

    return f'<form action="{url}" method="{verb}">\n{form}\n</form>'
