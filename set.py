import os


def main(app_name):
    if app_name not in os.popen('ls').read().split("\n"):
        os.system(f"python manage.py startapp {app_name.strip()}")
        print(f"{app_name} --> created")

    static_templates(app_name) 
    
    project_name = os.popen('ls ..').read().split("\n")
    try:
        project_name.remove("venv")
    except:
        pass
    try:
        project_name.remove("")
    except:
        pass

    sett_ch(app_name, project_name[0])
    urls_ch(project_name[0], app_name)
    app_urls(app_name)
    app_views(app_name)
    
    
def static_templates(app_name):
    if "templates" not in os.popen(f'ls {app_name}').read().split("\n"):
        os.mkdir(f"{app_name}/templates")
        os.mkdir(f"{app_name}/templates/{app_name}")
    
        with open(f"{app_name}/templates/{app_name}/index.html", "w") as file:
            
            file.write("")
            file.write('{% load static %}\n\n' + '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta http-equiv="X-UA-Compatible" content="IE=edge">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n' + """    <link rel="stylesheet" href="{% static """ + f""" '{app_name}/css/style.css' %""" + '}">' + f'\n    <title> {app_name} - index </title>\n</head>\n<body>\n  <h1> Barev </h1>  \n</body>\n</html>')
        
        print(f"{app_name} --> Templates created")
        
        
    if "static" not in os.popen(f'ls {app_name}').read().split("\n"):
        os.mkdir(f"{app_name}/static")
        os.mkdir(f"{app_name}/static/{app_name}")

        os.mkdir(f"{app_name}/static/{app_name}/css")
        os.mkdir(f"{app_name}/static/{app_name}/js")
            
        with open(f"{app_name}/static/{app_name}/css/style.css", "w") as file:
            file.write("")
            file.write("/* Karoche css a */\n\n")
            file.write("""body{\n    background-color: #1f1f1f;\n    color: white;\n}""")
            
        print(f"{app_name} --> Static created")
    
def sett_ch(app_name, project_name):
    with open(f"{project_name}/settings.py", "r") as file:
        file = file.read()
        
    installed_apps = file[file.index("INSTALLED_APPS") : file.index("MIDDLEWARE")-2]
    skzb_installed_apps = installed_apps
    installed_apps = installed_apps.replace("INSTALLED_APPS = [", "").replace("]", "").strip().split(",\n")
    
    installed_apps = [i.strip().replace(",", "") for i in installed_apps]
    
    new_istalled_apps = "INSTALLED_APPS = [\n"
    for i in installed_apps:
        new_istalled_apps += f"    {i},\n"
    
    
    if f"'{app_name}'" not in installed_apps:
        new_istalled_apps += f"    '{app_name}',\n"
    
    new_istalled_apps += "]"
    file = file.replace(skzb_installed_apps, new_istalled_apps)
    
    
    file = file.replace("'DIRS': [],", """'DIRS': [
            BASE_DIR/"templates"
            ],""")


    if "MEDIA_URL = 'media/'" not in file and "STATIC_ROOT = BASE_DIR/'static'" not in file and "MEDIA_ROOT = BASE_DIR/'media'" not in file:  
        file = file.replace("STATIC_URL = 'static/'", "STATIC_URL = 'static/'\nSTATIC_ROOT = BASE_DIR/'static'\n\nMEDIA_URL = 'media/'\nMEDIA_ROOT = BASE_DIR/'media'")


    with open(f"{project_name}/settings.py", "w") as new_text:
        new_text.write(file)
        
    print(f"{app_name} --> {project_name}/settings.py Changed")
    

def urls_ch(project_name, app_name):
    with open(f"{project_name}/urls.py", "r") as file:
        file = file.read()
    
    urlpatterns = file[file.index("urlpatterns = "):file.index("]")+1:]
    
    if f'path("", include("{app_name}.urls"))' not in urlpatterns:
        urlpatterns = urlpatterns.replace("path('admin/', admin.site.urls),", f"""path('admin/', admin.site.urls),\n    path("", include("{app_name}.urls")),""")

    if " + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)" not in urlpatterns:
        urlpatterns += " + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)"

    with open(f"{project_name}/urls.py", "w") as new_file:
        new_file.write("from django.contrib import admin\nfrom django.urls import path, include\nfrom django.conf import settings\nfrom django.conf.urls.static import static\n\n")
        new_file.write(urlpatterns)
        new_file.write("")
    
    print(f"{app_name} --> {project_name}/urls.py Changed")
        
def app_urls(app_name):
    with open(f"{app_name}/urls.py", "w") as file:
        file.write("")
        file.write(f'from django.urls import path\nfrom . import views\n\nurlpatterns = [\n   path("", views.index, name = "index")\n]')
        print(f"{app_name} --> {app_name}/urls Created")
        

def app_views(app_name):
    with open(f"{app_name}/views.py", "r") as text:
        text = text.read()

    with open(f"{app_name}/views.py", "a") as file:
        if "def index(" not in text:
            file.write(f'\n\ndef index(request):\n    return render(request, "{app_name}/index.html")')
        
        print(f"{app_name} --> {app_name}/views.py Changed")


# ============================================================================================================================


def pattern_transfer(path):
    print()
    for i in path:
        repl_html(i)
            
def repl_html(path):
    try:
        with open(path, "r") as text:
            text = text.read()
    except:
        print(f"Fayly chi gtnvel --> {path}")
        return
    
    file = text.split("\n")
        
        
    for i in file:
        i = i.strip()
        if "<link" in i and 'rel="stylesheet"' in i and ".css" in i and "{% static" not in i:
            i = i[i.index("href"):].replace('href="', "").replace('href = "', "")
            i = i.replace('">', "")
            if "rel=" in i.strip():
                i = i[:i.index("rel")-2]

            text = text.replace(i, "{% static '" + i + "' %}")
       
        elif "<script" in i and ".js" in i and "{% static" not in i:
            i = i[i.index("src"):].replace('src="', "").replace('src = "', "")
            i = i[:i.index(".js")+3]
            text = text.replace(i, "{% static '" + i + "' %}")

    with open(path, "w") as file:
        file.write("")
        if "{% load static %}" not in text and "{%load static%}" not in text:
            file.write("{% load static %}\n\n")
        file.write(text)     
        print(f"Poxeci --> {path}")
    
    

if __name__ == "__main__":
    inp = ""
    
    while inp.strip() != "1" and inp.strip() != "0":
        print("0 - Change templates \n1 - Create an application\n")
        inp = input("--> ")
    
    print()
        
    if inp == "0":
        pattern_transfer(input("Html path: ").split(" "))
    else:
        main(input("Enter app name: "))
    
     




