#获取二维码
import requests
import random
import base64
import json
import os
from io import BytesIO
import cv2
import numpy as np
import time
import threading
import datedays
import datetime
from Crypto.Cipher import AES

#验证码1分钟有效 登录30分钟


def get_qr():
    url=' http://org.xjtu.edu.cn/openplatform/g/qrcode/getQRCode?width=215&height=215&_='+str(int(round(time.time() * 1000)))
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22041216C Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.79 Mobile Safari/537.36 toon/2122313098 toonType/150 toonVersion/6.3.0 toongine/1.0.12 toongineBuild/12 platform/android language/zh skin/white fontIndex/0',
        'cookie':'cur_appId_=n0C/SQT28fY=; state=xjdCas'
        }
    res_qr = session.get(url,headers=headers)
    #cookie_dict = requests.utils.dict_from_cookiejar(session.cookies)
    #print(cookie_dict)
    #session.cookies = requests.utils.cookiejar_from_dict(cookie_dict)
    json_res=json.loads(res_qr.text)
    base64_str=json_res['data']['baseCode']
    to_ken=json_res['data']['token']
    return base64_str,to_ken

def post_zh_dl(user,pwd):
    url='http://org.xjtu.edu.cn/openplatform/g/admin/login'
    data={
        "username":user,
        "loginType":1,
        "pwd":pwd,
        "jcaptchaCode":""
        }
    headers={
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22041216C Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.79 Mobile Safari/537.36 toon/2122313098 toonType/150 toonVersion/6.3.0 toongine/1.0.12 toongineBuild/12 platform/android language/zh skin/white fontIndex/0',
        'Content-Type': 'application/json;charset=UTF-8',
        'cookie':'cur_appId_=n0C/SQT28fY=; state=xjdCas'
        }
    res_pl=session.post(url,json=data,headers=headers)
    json_pl=json.loads(res_pl.text)
    memberId=json_pl['data']['orgInfo']['memberId']
    tokenKey=json_pl['data']['tokenKey']
    print('memberId:'+str(memberId))
    return memberId,tokenKey

def get_status(token):
    url='https://org.xjtu.edu.cn/openplatform/g/qrcode/getQrCodeStatus?uuid='+token+'&_='+str(int(round(time.time() * 1000)))
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22041216C Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.79 Mobile Safari/537.36 toon/2122313098 toonType/150 toonVersion/6.3.0 toongine/1.0.12 toongineBuild/12 platform/android language/zh skin/white fontIndex/0',
        'cookie':'cur_appId_=n0C/SQT28fY=; state=xjdCas'
        }
    res_st = session.get(url,headers=headers)
    json_st=json.loads(res_st.text)
    return json_st['data']['qrcodeStatus']


def base64_to_image(base64_code):
    # base64解码
    img_data = base64.b64decode(base64_code)
    # 转换为np数组
    img_array = np.frombuffer(img_data, np.uint8)
    # 转换成opencv可用格式
    img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
    return img

def post_login():
    url='http://org.xjtu.edu.cn/openplatform/g/admin/login'
    data={
        "username":token,
        "loginType":3
        }
    headers={
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22041216C Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.79 Mobile Safari/537.36 toon/2122313098 toonType/150 toonVersion/6.3.0 toongine/1.0.12 toongineBuild/12 platform/android language/zh skin/white fontIndex/0',
        'Content-Type': 'application/json;charset=UTF-8',
        'cookie':'cur_appId_=n0C/SQT28fY=; state=xjdCas'
        }
    res_pl=session.post(url,json=data,headers=headers)
    json_pl=json.loads(res_pl.text)
    memberId=json_pl['data']['orgInfo']['memberId']
    tokenKey=json_pl['data']['tokenKey']
    #requests.utils.add_dict_to_cookiejar(session.cookies, {'open_Platform_User': tokenKey})
    #requests.utils.add_dict_to_cookiejar(session.cookies, {'memberId': str(memberId)})
    print('memberId:'+str(memberId))
    return memberId,tokenKey

def getUserIdentity(memberId):
    url='http://org.xjtu.edu.cn/openplatform/g/admin/getUserIdentity?memberId='+str(memberId)+'&_='+str(int(round(time.time() * 1000)))
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22041216C Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.79 Mobile Safari/537.36 toon/2122313098 toonType/150 toonVersion/6.3.0 toongine/1.0.12 toongineBuild/12 platform/android language/zh skin/white fontIndex/0',
        'cookie':'cur_appId_=n0C/SQT28fY=; state=xjdCas',
        'Content-Type': 'application/json;charset=utf-8'
        }
    res_guid = session.get(url,headers=headers)
    json_guid=json.loads(res_guid.text)
    #print(json_guid['data'])
    personNo=json_guid['data'][0]['personNo']
    print('personNo:'+str(personNo))
    return personNo
    
def getRedirectUrl(personNo):
    url='http://org.xjtu.edu.cn/openplatform/oauth/auth/getRedirectUrl?userType=1&personNo='+str(personNo)+'&_='+str(int(round(time.time() * 1000)))
    print(url)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27',
        'cookie':'cur_appId_=n0C/SQT28fY=; state=xjdCas;open_Platform_User='+tokenKey
        }
    res_gru = session.get(url,headers=headers)
    json_gru=json.loads(res_gru.text)
    #print(session.cookies)
    #print(res_gru.text)
    getRedirectUrl=json_gru['data']
    print("getRedirectUrl:"+getRedirectUrl)
    return getRedirectUrl.split('redirectUrl=')[0]+'redirectUrl=http://202.117.17.144/index.html'

def get_html(url):
    print(url)
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22041216C Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.79 Mobile Safari/537.36 toon/2122313098 toonType/150 toonVersion/6.3.0 toongine/1.0.12 toongineBuild/12 platform/android language/zh skin/white fontIndex/0',
        'cookie':'cur_appId_=n0C/SQT28fY=; state=xjdCas;open_Platform_User='+tokenKey
        }
    res_html = session.get(url,headers=headers)
    return True

def get_okarea():
    url='http://202.117.17.144/product/findOkArea.html?s_date='+str(ttt)+'&serviceid='+sport_id
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Content-Type':'text/plain;charset=UTF-8',
        'Referer': 'http://202.117.17.144:8080/web/product/show.html?id='+sport_id,
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22041216C Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.79 Mobile Safari/537.36 toon/2122313098 toonType/150 toonVersion/6.3.0 toongine/1.0.12 toongineBuild/12 platform/android language/zh skin/white fontIndex/0'
        }   
    return session.get(url,headers=headers).text

def list_print(ls,ncd):
    #这里分析场地有几个+1 设为ncd

    #这里分析场地时间段有几个 nsj
    k=1
    for i in ls:
        #判断 计数到第几个了，开始换行.
        if k%ncd==0:
            #换行
            print(i)
            k=k+1
        else:
            print(i,end="----")
            k=k+1

            
def xie_liebiao(res_okarea):
    list_a=list()
    global json_d
    json_d=json.loads(res_okarea)
    #存数据
    #创建列表
    for i in range(len(json_d['object'])):
        name=json_d['object'][i]['name']
        sname=json_d['object'][i]['sname']
        status=json_d['object'][i]['status']
        time_no=json_d['object'][i]['stock']['time_no']
        #为1时 可以选 为2时 已被选 0为预定
        stock=json_d['object'][i]['stock']['all_count']
        #写入时间段
        if i%stock==0:
            list_a.append(json_d['object'][i]['stock']['time_no'])
        if status==1:
            list_a.append("✅"+"【"+str(i)+"】"+sname)
        else:
            list_a.append("--"+"【"+str(i)+"】"+sname)
    list_print(list_a,stock+1) 

def get_yzm():
    url='http://202.117.17.144/gen'
    headers = {
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'X-Requested-With': 'synjones.commerce.xjtu',
        'Connection': 'keep-alive',
        'Referer': 'http://202.117.17.144:8080/web/product/show.html?id='+sport_id,
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22041216C Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.79 Mobile Safari/537.36 toon/2122313098 toonType/150 toonVersion/6.3.0 toongine/1.0.12 toongineBuild/12 platform/android language/zh skin/white fontIndex/0'
        }
    res = session.get(url,headers=headers)
    parsed_json = json.loads(res.text)
    yzmid= parsed_json["id"]
    captcha_data = parsed_json["captcha"]
    return yzmid,captcha_data["backgroundImage"].replace("data:image/jpeg;base64,","")

def get_mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        #print("Clicked at ({}, {})".format(int((x-15)*260/590), int(y*159/360)))
        global zb
        zb=int((x-15)*260/590)
        cv2.destroyAllWindows()
        #print("Clicked at ({}, {})".format(x, y))
    if event == cv2.EVENT_RBUTTONDOWN:
        cv2.destroyAllWindows()

def do_guiji(okx):
    trackList=[]
    startX=0
    startY=0
    pageX=0
    pageY=0
    time.sleep(0.3)
    clist={
        "x":pageX-startX,
        "y":pageY-startY,
        "type":"down",
        "t":0
        }
    trackList.append(clist)
    k=random.randint(50,80)
    for i in range(0,k):
        pageX=random.uniform(-0.5,0.5)+pageX+okx/k
        pageY=pageY+random.uniform(-0.5,0.5)
        clist={
            "x":int(pageX-startX),
            "y":int(pageY-startY),
            "type":"move",
            "t":int((datetime.datetime.utcnow().timestamp()-startTime.timestamp())*1000)
            }
        trackList.append(clist)
        time.sleep(0.03)
    global endtime
    endtime=datetime.datetime.utcnow()
    time.sleep(0.03)
    clist={
        "x":okx-startX,
        "y":int(pageY-startY),
        "type":"up",
        "t":int((endtime.timestamp()-startTime.timestamp())*1000)
        }
    trackList.append(clist)
    return trackList


def post_order(stockid,id,yzm,yzmid):
    url='http://202.117.17.144/order/book.html'
    param='{"activityPrice":0,"activityStr":null,"address":"'+sport_id+'","dates":null,"extend":{},"flag":"0","isBulkBooking":null,"isbookall":"0","isfreeman":"0","istimes":"0","mercacc":null,"merccode":null,"order":null,"orderfrom":null,"remark":null,"serviceid":null,"shoppingcart":"0","sno":null,"stock":{"'+stockid+'":"1"},"stockdetail":{"'+stockid+'":"'+id+'"},"stockdetailids":"'+id+'","stockid":null,"subscriber":"0","time_detailnames":null,"userBean":null,"venueReason":null}'
    data='param='+param+'&yzm='+str(yzm)+'synjones'+yzmid+'synjoneshttp://202.117.17.144:8071&'+'json=true'
    print(data)
    headers={
        'Accept': 'application/json, text/javascript, */*;q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://202.117.17.144/product/show.html?id='+sport_id,
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22041216C Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.79 Mobile Safari/537.36 toon/2122313098 toonType/150 toonVersion/6.3.0 toongine/1.0.12 toongineBuild/12 platform/android language/zh skin/white fontIndex/0',
        }
    rep_order = session.post(url=url,data=data, headers=headers)
    print(rep_order.text)

def post_first(stockid,id):
    url='http://202.117.17.144/order/show.html?id='+sport_id
    param='{"stock":{"'+stockid+'":"1"},"address":"'+sport_id+'","stockdetailids":"'+id+'","extend":{}}'
    data='param='+param
    print(data)
    headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://202.117.17.144:8080/web/product/show.html?id='+sport_id,
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22041216C Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.79 Mobile Safari/537.36 toon/2122313098 toonType/150 toonVersion/6.3.0 toongine/1.0.12 toongineBuild/12 platform/android language/zh skin/white fontIndex/0',
        }
    rep_order = session.post(url=url,data=data, headers=headers)
    #print(rep_order.text)


def pad(s):
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

def encrypt(message, key):
    # 对原文进行填充
    message = pad(message)
    
    # 创建AES对象并进行加密
    aes = AES.new(key.encode(), AES.MODE_ECB)
    message = aes.encrypt(message.encode())
  
    # 返回Base64编码后的密文
    return base64.b64encode(message).decode()

def decrypt(ciphertext, key):
    # 对密文进行解码
    ciphertext = base64.b64decode(ciphertext)
  
    # 创建AES对象并进行解密
    aes = AES.new(key.encode(), AES.MODE_ECB)
    message = aes.decrypt(ciphertext).decode()
  
    # 去除填充部分并返回明文
    return message[:-ord(message[len(message)-1:])]


#整体思路;
    #1.先进行扫码登陆。 获取相应位置的排序列表；-----这里提前选择位置；（自己输入吧）
    #2.等待时间处理，提前五秒或者十秒对验证码进行处理。记录轨迹
    #3.时间到达8点40整，循环获取列表数据；然后提交相应数据。
    

    
    
#全局变量初始化  
sport_id='101'
ttt=datedays.gettomorrow(2)
xzsuccess=False #是否选择
denglu=False #判断登录
shijian_1=False  #判断验证码
shijian_2=False  #判断提交
zb=None #判断坐标
xz=''
tokenKey=''
session=requests.session()
#建立可连续cookie的浏览器



print('使用说明') 
print('-------》1.会询问是否在线选，如果在先线选，则是达到8.40才进行访问座位序号；否则需要进行本地选择，但可能出现每日的放场次不同，导致提交出现问题') 
print('-------》2.需要进行登录，后续的操作才会进行。但是这里好像有问题，如果提前太早的话，易出错。这里已经修改，还未测试。解决方法，使用APP进一下抢场地界面')
print('-------》3.使用二维码登录，APP扫码。验证码采用点击方式，即出现验证码则点击缺口最左边即可')
get_html("http://org.xjtu.edu.cn/openplatform/oauth/authorize?appId=1099&redirectUri=http://ohello.xjtu.edu.cn/berserker-auth/auth/casLogin&responseType=code&scope=user_info&state=thirdPartyUrl=http://202.117.17.144/loginCas/isLogin.html,redirectUrl=http://yudingweb/order/show.html?id=101")
online_xz=int(input("是否在线选场地,1-yes;0-no :"))

if online_xz==0:
    j_date=datetime.date(2023,5,2)
    tianshu=(ttt-j_date).days
    print(' 101号羽毛球场地 仅供场地编号获取 并未涉及场地情况获取 ')
    print('09:01-10:00------( 0)场地1------( 1)场地2------( 2)场地3<----一般不选择--->')
    print('10:01-11:00------( 3)场地1------( 4)场地2------( 5)场地3<----一般不选择--->')
    print('11:01-12:00------( 6)场地1------( 7)场地2------( 8)场地3<----一般不选择--->')
    print('08:01-09:00------( 9)场地1------(10)场地2------(11)场地3<----一般不选择--->')
    print('14:31-15:30------(12)场地1------(13)场地2------(14)场地3')
    print('15:31-16:30------(15)场地1------(16)场地2------(17)场地3')
    print('16:31-17:30------(18)场地1------(19)场地2------(20)场地3')
    print('17:31-18:30------(21)场地1------(22)场地2------(23)场地3')
    print('18:31-19:30------(24)场地1------(25)场地2------(26)场地3')
    print('19:31-20:30------(27)场地1------(28)场地2------(29)场地3')
    print('20:31-21:30------(30)场地1------(31)场地2------(32)场地3')
    while True:
        xz=input("输入场地序号")
        if xz=='':
            break
        else:
            stockid=str(232496+int(xz)//3+11*tianshu)
            id=str(2452828+33*tianshu+int(xz))
            xzsuccess=True
            print('stockid:'+stockid+','+'id:'+id)
            break


cx=int(input("是否登录,1-yes;0-no :"))

if cx==1:
    key = '0725@pwdorgopenp'
    text_zh="3122103203"
    #pwd_text=mm.get()
    pwd_text="081077"
    pwd = encrypt(pwd_text, key)
    memberId,tokenKey=post_zh_dl(text_zh,pwd)
    #memberId,tokenKey=post_login()
    personNo=getUserIdentity(memberId)
    getredirectUrl=getRedirectUrl(personNo)
    denglu=get_html(getredirectUrl)



#获取列表,不需要判断是否登录;但这里需要处理时间
#try:
 #   res_okarea=get_okarea()
#except Exception as e:
 #   print("函数okarea:",e)
  #  #已经获得了场地信息，打印出来
#if res_okarea != None:
 #   xie_liebiao(res_okarea)
  #  stockid=str(json_d['object'][xz]['stockid'])
   # id=str(json_d['object'][xz]['id'])
    #print(stockid+","+id)


#post_first(stockid,id)


#如果登录,判断时间
if denglu==True:
    print(denglu)
    while True:
        current_time = time.strftime("%H:%M:%S", time.localtime())
        if current_time >= "08:39:45" and current_time <= "08:40:10":
            print('xcz-1:'+current_time)
            shijian_1=True
            break
        else :
            print('xcz-2:'+current_time)
            #shijian_1=True
            #break
        time.sleep(1)

#如果登录,判断时间(8:39.45-8.40.10),验证码处理
if denglu==True and shijian_1==True:
    yzmid,background_image=get_yzm()
    background_image_data = base64.b64decode(background_image)
    background_image_data = np.frombuffer(background_image_data, dtype=np.uint8)
    background_image = cv2.imdecode(background_image_data, flags=cv2.IMREAD_COLOR)
    cv2.imwrite("1.jpg",background_image)
    img = cv2.imread('1.jpg')
    #img=cv2.resize(img,(260,159))
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', get_mouse_click)
    cv2.waitKey(0)
    while 2>1:
        if zb!=None:
            break
    #这里是验证码坐标获取
    #global startTime 默认全局
    startTime=datetime.datetime.utcnow()
    tlist=do_guiji(zb)
    #print(str(startTime)[:-3])
    data={
        "bgImageWidth":260,
        "bgImageHeight":0,
        "sliderImageWidth":0,
        "sliderImageHeight":159,
        "startSlidingTime":str(startTime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])+"Z",
        "entSlidingTime":str(endtime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])+"Z",
        "trackList":tlist
        }


if denglu==True and online_xz==1:
#在线选的话，时间弄快点
    while True:
        current_time = time.strftime("%H:%M:%S", time.localtime())
        if current_time >= "08:40:00" and current_time <= "08:40:10":
            shijian_2=True
            break
        else :
            print('zxshijian_2:'+current_time)
            #shijian_2=True
            #break
        time.sleep(1)

if denglu==True and online_xz==0:
#离线选的话，时间慢点
    while True:
        current_time = time.strftime("%H:%M:%S", time.localtime())
        if current_time >= "08:40:03" and current_time <= "08:40:10":
            shijian_2=True
            break
        else :
            print('lxshijian_2:'+current_time)
            #shijian_2=True
            #break
        time.sleep(1)



if denglu==True:
   if online_xz==1 or xz=='':
        print("2")
        try:
            res_okarea=get_okarea()
        except Exception as e:
            print("函数okarea:",e)
    #已经获得了场地信息，打印出来
        xie_liebiao(res_okarea)
    #输出数组形式
    # 1 1 1
    # 1 1 1
        while True:
            xz=input("输入场地序号")
            if xz =='':
                print("输入场地序号--->")
            else:
                stockid=str(json_d['object'][int(xz)]['stockid'])
                id=str(json_d['object'][int(xz)]['id'])
                xzsuccess=True
                print('online_stockid:'+stockid+','+'online_id:'+id)
                break

if denglu==True:
    if shijian_2==True and xzsuccess==True:
        print("3")
        try:
            order=post_order(stockid,id,str(data).replace("'","\"").replace(" ",""),yzmid)
        except Exception as e:
            print("post_order:",e)



