import jinja2
if __name__ == '__main__':
    jinjaEnv =jinja2.Environment(loader=jinja2.FileSystemLoader('tmp'))
    templete =jinjaEnv.get_template('Basic.py')
    print(templete.render({'home' :'ad' , 'ip':'0.0.0.0'}))
