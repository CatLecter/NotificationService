from letter_templates.interface import create_html


if __name__ == "__main__":

    html = create_html()
    with open("test.html", "w") as f:
        f.writelines(html)
