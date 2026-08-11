from html import escape

from integrify.schemas import DryResponse


def json_to_html_form(json_data: DryResponse, with_submit: bool = False) -> str:
    """AzeriCard-ə göndərilməli datanı HTML formuna çevirən funksiya

    Bütün dəyərlər HTML atributuna yazılmadan əvvəl `html.escape(..., quote=True)` ilə
    escape olunur ki, tərkibində `"` və ya `<` olan dəyər atributdan çıxıb HTML/JS
    injection-a səbəb olmasın.

    Args:
        json_data: DryResponse payload
        with_submit: HTML form-da submit butonunu elavə etmə(mə)k
    """

    url = escape(str(json_data['url']), quote=True)
    verb = escape(str(json_data['verb']), quote=True)
    data = json_data['data']

    # Create HTML form based on keys and values of json_data. Every field is str, str.
    form = '\n'.join(
        f'<input type="hidden" name="{escape(str(key), quote=True)}" '
        f'value="{escape(str(value), quote=True)}">'
        for key, value in data.items()
    )

    submit = '<input type="submit" value="Submit">\n' if with_submit else ''
    return (
        f'<form name="azericard_form" action="{url}" method="{verb}">\n{form}\n{submit}</form>\n'
        '<script>document.azericard_form.submit();</script>'
    )
