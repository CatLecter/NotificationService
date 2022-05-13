from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader('./templates'))
template = env.get_template('test.html')
html = template.render(register_title='Петя')

with open('main.html', 'w') as f:
    f.writelines(html)