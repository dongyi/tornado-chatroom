#coding=utf-8
from django.views.decorators.csrf import csrf_exempt
from settings import SINA_APP_KEY, SINA_APP_SECRET
from weibopy.auth import OAuthHandler, BasicAuthHandler
from weibopy.api import API
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
import md5

def rp2rating(rp):
    if rp in range(0, 20):
        return u"你爸爸是李刚也没用了"
    if rp in range(21, 40):
        return u"你太二了"
    if rp in range(41, 60):
        return u"一般一般"
    if rp in range(61, 80):
        return u"人品尚可，继续保持"
    if rp in range(81, 100):
        return u"你有很高的niubility"
    

@csrf_exempt
def test_rp(request):
    if request.method == 'POST':
        success = ""
        access_token = request.session['oauth_access_token']
        auth = OAuthHandler(SINA_APP_KEY, SINA_APP_SECRET)
        auth.set_access_token(access_token.key, access_token.secret)
        api = API(auth)
        try:
            username = api.me().screen_name
            number = int(md5.md5(username.encode('utf-8')).hexdigest(), 16)
            rp = number % 100
            rating = rp2rating(rp)
            api.update_status(u"%s, 你的人品是 %d, %s" %(username, rp, rating))
            success = u"成功发布"
        except:
            raise
            success = u"失败"
        return HttpResponseRedirect('/status')
    return HttpResponseRedirect('/status')

@csrf_exempt
def post_to_wb(request):
    if request.method == 'POST':
        success = ""
        access_token = request.session['oauth_access_token']
        auth = OAuthHandler(SINA_APP_KEY, SINA_APP_SECRET)
        auth.set_access_token(access_token.key, access_token.secret)
        api = API(auth)
        try:
            content = request.POST.get("content")
            api.update_status(content)
            success = "成功发布"
        except:
            raise
            success = "失败"
        return HttpResponseRedirect('/status')
    return HttpResponseRedirect('/status')


def showstatus(request):
    logined = False
    if request.session.get('oauth_access_token'):
        logined = True
        access_token = request.session['oauth_access_token']
    else:
        return render_to_response('wb/status.html', locals())
    access_token = request.session['oauth_access_token'] 
    auth = OAuthHandler(SINA_APP_KEY, SINA_APP_SECRET)
    auth.set_access_token(access_token.key, access_token.secret)
    api = API(auth)
    try: 
        gender = "male" if api.me().gender == "m" else "female"
        id = api.me().id
        screen_name = api.me().screen_name
        description = api.me().description
        location = api.me().location
        profile_image_url = api.me().profile_image_url
    except :
        return render_to_response('wb/status.html', locals())
    return render_to_response('wb/status.html', locals())
