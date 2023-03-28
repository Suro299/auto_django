import os

def main(app_name):
    if app_name not in os.popen('ls').read().split("\n"):
        os.system(f"python manage.py startapp {app_name}")
    
    project_name = os.popen('ls ..').read().split("\n")
    project_name.remove("venv")
    project_name.remove("")
    
    sett_ch(app_name, project_name[0])
    urls_ch(project_name[0])
    
    
def sett_ch(app_name, project_name,):
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
    

def urls_ch(project_name):
    with open(f"{project_name}/urls.py", "r") as file:
        file = file.read()
    
    
    
    # urlpatterns = file[file.index("urlpatterns = "):file.index("]")+1:] + " + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)"
    urlpatterns = file[file.index("urlpatterns = "):file.index("]")+1:]
    
    if 'path("", include(" "))' not in urlpatterns:
        urlpatterns = urlpatterns.replace("path('admin/', admin.site.urls),", """path('admin/', admin.site.urls),\n    path("", include(" ")),""")

    if " + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)" not in urlpatterns:
        urlpatterns += " + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)"

    with open(f"{project_name}/urls.py", "w") as new_file:
        new_file.write("from django.contrib import admin\nfrom django.urls import path, include\nfrom django.conf import settings\nfrom django.conf.urls.static import static\n\n")
        new_file.write(urlpatterns)
        new_file.write("")
            
        
# from django.contrib import admin
        
    

    
main(input("Enter app name: ")) 


