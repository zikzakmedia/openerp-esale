#
# FileManager http://labs.corefive.com/Projects/FileManager/ Connector
# 
#
# Django Connector By Paul von Hoesslin
#
from django.http import HttpResponse, Http404
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.core.servers.basehttp import FileWrapper
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from settings import PATH as PROJECT_DIR

import os, urllib, time
import traceback
import sys

encode_json = simplejson.JSONEncoder().encode

try:
    from PIL import Image
except ImportError:
    raise EnvironmentError('Must have the PIL (Python Imaging Library).')

path_exists = os.path.exists
normalize_path = os.path.normpath
absolute_path = os.path.abspath 
split_path = os.path.split
split_ext = os.path.splitext

base_dir = '/static/uploads/'

def dirlist(request):
    r=['<ul class="jqueryFileTree" style="display: none;">']
    d = request.POST.get('dir', base_dir)    
    try:
        r=['<ul class="jqueryFileTree" style="display: none;">']
        for f in os.listdir(PROJECT_DIR + d):
            ff=os.path.join((PROJECT_DIR + d),f)

            if os.path.isdir(ff):
                if f != ".svn" and f != ".DS_Store":
                    r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (d+f,f))
            else:
                if f != ".svn" and f != ".DS_Store": 
                    e=os.path.splitext(f)[1][1:] # get .ext and remove dot
                    r.append('<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (e,(d+f),f))

        r.append('</ul>')
    except Exception,e:
        type, value, tb = sys.exc_info()
        print >> sys.stderr,  type.__name__, ":", value
        print >> sys.stderr, '\n'.join(traceback.format_tb(tb))
        r.append('Could not load directory: %s %s' % (d, traceback.format_tb(tb)))
    r.append('</ul>')

    request.session["upload_path"] = d

    return HttpResponse(''.join(r))

def getInfo(request, request_path):
    path = PROJECT_DIR + request_path
    preview = request_path
    imagetypes = ['.gif','.jpg','.jpeg','.png',]
    if os.path.isdir(path):
        thefile = {
            'Path' : request_path + "/",
            'Filename' : split_path(path)[-1],
            'File Type' : split_path(path)[1],
            'Preview' : 'images/fileicons/_Open.png',
            'Properties' : {
                    'Date Created' : '',
                    'Date Modified' : '',
                    'Width' : '',
                    'Height' : '',
                    'Size' : ''
                },
            'Return' : request_path,
            'Error' : '',
            'Code' : 0,
            }        
        thefile['File Type'] = 'Directory'
    else:
        ext = split_ext(path)
        preview = 'images/fileicons/'+ ext[1][1:] + '.png'
        thefile = {
            'Path' : request_path,
            'Filename' : split_path(path)[-1],
            'File Type' : split_path(path)[1][1:],
            'Preview' : preview,
            'Properties' : {
                    'Date Created' : '',
                    'Date Modified' : '',
                    'Width' : '',
                    'Height' : '',
                    'Size' : ''
                },
            'Return' : request_path,
            'Error' : '',
            'Code' : 0,
            }        
        if ext[1] in imagetypes:
            try:
                img = Image.open(open(path,"r"))
                xsize, ysize = img.size
                thefile['Properties']['Width'] = xsize
                thefile['Properties']['Height'] = ysize
                thefile['Preview'] = "../../.." + request_path
            except:
                preview = 'images/fileicons/'+ ext[1][1:] + '.png'
                thefile['Preview'] = preview

        thefile['File Type'] = os.path.splitext(path)[1][1:]

        thefile['Properties']['Date Created'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(path))) 
        thefile['Properties']['Date Modified'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(path)))  
        thefile['Properties']['Size'] = os.path.getsize(path)
    return encode_json(thefile)

def handle_uploaded_file(request, f):
    upload_path = request.session.get("upload_path", '/static/uploads/')
    destination = open((PROJECT_DIR + upload_path + f.name.lower()), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    result = {
        'Name' : f.name,
        'Path' : upload_path,
        'Code' : "0",
        'Error' : ""
    }
    return result

@login_required
@csrf_exempt
def handler(request):
    if request.method == "POST":
        try:
            result = handle_uploaded_file(request, request.FILES["newfile"])
            return HttpResponse('<textarea>' + encode_json(result) + '</textarea>')
        except:
            type, value, tb = sys.exc_info()
            print >> sys.stderr,  type.__name__, ":", value
            print >> sys.stderr, '\n'.join(traceback.format_tb(tb))
    else:
        if not 'mode' in request.GET:
            raise Http404('Use navigation menus access this view')

        if request.GET["mode"] == "getinfo":
            return HttpResponse(getInfo(request, request.GET["path"]))

        if request.GET["mode"] == "getfolder":
            result = []
            d=urllib.unquote(PROJECT_DIR + request.GET["path"])
            request.session["upload_path"] = request.GET["path"]
            result += " { "
            for i, filename in enumerate(os.listdir(d)):
                if filename != ".svn" and filename != ".DS_Store":
                    result += '"' + request.GET["path"] + filename + '" : '
                    result += getInfo(request,request.GET["path"] + filename)
                    if i < (len(os.listdir(d)) - 1):
                        result += " , "
            result += " } "
            return HttpResponse(result)

        if request.GET["mode"] == "rename":
            old = PROJECT_DIR + request.GET["old"] 
            path = split_path(old)[0]

            oldname = split_path(old)[-1]

            if os.path.isdir(old+"/"):
                old += '/'

            newname = request.GET["new"]
            newpath = path + '/' + newname

            try:
                print "old:" + split_path(old)[0].replace(PROJECT_DIR, "")
                print "newpath:" + split_path(newpath)[0].replace(PROJECT_DIR, "")
                os.rename(old, newpath)
                error_message = newname
                success_code = "0"
            except:
                type, value, tb = sys.exc_info()
                print >> sys.stderr,  type.__name__, ":", value
                print >> sys.stderr, '\n'.join(traceback.format_tb(tb))
                success_code = "500"
                error_message = _('There was an error renaming the file.')

            if os.path.isdir(newpath+"/"):
                newpath += '/'
            
            result = {
                'Old Path' : split_path(old)[0].replace(PROJECT_DIR, "") + "/",
                'Old Name' : oldname,
                'New Path' : split_path(newpath)[0].replace(PROJECT_DIR, "") + "/",
                'New Name' : newname,
                'Error' : error_message,
                'Code' : success_code
            }
        
            return HttpResponse(encode_json(result))

        if request.GET["mode"] == "delete":
            fullpath = PROJECT_DIR + request.GET["path"]
            if os.path.isdir(fullpath+"/"):
                if not fullpath[-1]=='/':
                    fullpath += '/'

            try:
                directory = split_path(fullpath)[0]
                name = split_path(fullpath)[-1]
                os.remove(fullpath)
                error_message = _('%(name)s was deleted successfully.') % {'name':name}
                success_code = "0"
            except:
                error_message = _('There was an error deleting the file. <br/> The operation was either not permitted or it may have already been deleted.')
                success_code = "500"
            
            result = {
                'Path' : fullpath.replace(PROJECT_DIR, ""),
                'Name' : name,
                'Error' : error_message,
                'Code' : success_code
            }

            return HttpResponse(encode_json(result))

        if request.GET["mode"] == "addfolder":
            path = PROJECT_DIR + request.GET["path"]
            newName = request.GET["name"].replace(" ", "_")

            newPath = path + newName + "/"
        
            if path_exists(path):
                try:
                    os.mkdir(newPath)
                    success_code = "0"
                    error_message = _('Successfully created folder.')
                except:
                    error_message = _('There was an error creating the directory.')
                    success_code = "500"
            else:
                success_code = "500"
                error_message = _('There is no Root Directory.')

            result = {
                'Path' : request.GET["path"],
                'Parent' : request.GET["path"],
                'Name' : newName,
                'New Path' : newPath,
                'Error' : error_message,
                'Code' : success_code
            }
            return HttpResponse(encode_json(result))
    
        if request.GET["mode"] == "download":
            abspath = PROJECT_DIR + request.GET["path"]
            wrapper = FileWrapper(file(abspath))
            response = HttpResponse(wrapper)
            response['Content-Length'] = os.path.getsize(abspath)
            response['Content-Disposition'] = 'attachment; filename=%s' % split_path(abspath)[-1]
            return response

    return HttpResponse("failed")
