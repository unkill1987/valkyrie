import smtplib
import urllib.request
import requests
from email.message import EmailMessage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import hashlib
from fpdf import FPDF, HTMLMixin
import pyotp
import os
import time
from pandas.io import json
from app.models import Contract_LCR, Member, Contract_CI, Contract_SR, Contract_BL, Contract_DO, Contract_LC, Process, \
    Notice
from valweb import settings
from django.utils import timezone
from cryptography.fernet import Fernet


def user_manual(request):
    filepath = os.path.join(settings.BASE_DIR, 'app/static/app/manual/user_manual.pdf')
    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
        return response


def checkcontract(request):
    try:
        result_dict = {}
        cid = str(request.POST['cid'])
        url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
        res = requests.post(url)
        history = res.json()
        if len(history) == 0:
            result_dict['result'] = "not exist"
        else:
            result_dict['result'] = "exist"
        return JsonResponse(result_dict)
    except:
        pass


def email(request):
    if request.method == 'GET':
        user_role = request.session['user_role']
        if user_role == '1':
            return render(request, 'app/mypage1.html', {})
        elif user_role == '2':
            return render(request, 'app/mypage2.html', {})
        elif user_role == '3':
            return render(request, 'app/mypage3.html', {})
        elif user_role == '4':
            return render(request, 'app/mypage4.html', {})
        else:
            return redirect('index')

    else:
        result_dict = {}
        smtp_gmail = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_gmail.ehlo()
        # 연결을 암호화
        smtp_gmail.starttls()
        smtp_gmail.login('saidtherapy23@gmail.com', 'erff8653!')
        msg = EmailMessage()

        try:
            user_id = request.session['user_id']
            email = request.POST['email']

            msg['Subject'] = "%s님의 문의글입니다" % user_id
            # 내용 입력
            msg.set_content("%s" % email)
            # 보내는 사람
            msg['From'] = 'Valkyrie Trade System'
            # 관리자 메일
            msg['To'] = 'therapy23@naver.com'
            smtp_gmail.send_message(msg)
            result_dict['result'] = 'Success'
            return JsonResponse(result_dict)
        except Exception as e:
            print(e)
            result_dict['result'] = 'Fail'
            return JsonResponse(result_dict)


def mytrade(request):
    if request.method == 'GET':
        user_role = request.session['user_role']
        if user_role == '1':
            return render(request, 'app/mypage1.html', {})
        elif user_role == '2':
            return render(request, 'app/mypage2.html', {})
        elif user_role == '3':
            return render(request, 'app/mypage3.html', {})
        elif user_role == '4':
            return render(request, 'app/mypage4.html', {})
        else:
            return redirect('index')
    else:
        result_dict = {}
        try:

            mytrade = request.POST['mytrade']
            trade = Process.objects.filter(id=mytrade).values('CI_hash', 'LCR_hash', 'LC_hash', 'SR_hash', 'BL_hash',
                                                              'DO_hash')
            return JsonResponse({'trade': list(trade)})
        except Exception as e:
            result_dict['result'] = "Invalid Contract"
            return JsonResponse(result_dict)


def addressmodify(request):
    if request.method == 'GET':
        user_role = request.session['user_role']
        if user_role == '1':
            return render(request, 'app/mypage1.html', {})
        elif user_role == '2':
            return render(request, 'app/mypage2.html', {})
        elif user_role == '3':
            return render(request, 'app/mypage3.html', {})
        elif user_role == '4':
            return render(request, 'app/mypage4.html', {})
        else:
            return redirect('index')
    else:
        result_dict = {}
        try:
            user_id = request.session['user_id']
            postcode = request.POST['postcode']
            address = request.POST['address']
            details = request.POST['details']
            extra = request.POST['extra_info']
            member = Member.objects.get(user_id=user_id)
            user_address = '(' + postcode + ')' + address + extra + ' ' + details
            member.address = user_address
            member.save()
            result_dict['result'] = 'success'
            return JsonResponse(result_dict)
        except Exception as e:
            print(e)
            result_dict['result'] = 'fail'
            return JsonResponse(result_dict)


def pwmodify(request):
    if request.method == 'GET':
        user_role = request.session['user_role']
        if user_role == '1':
            return render(request, 'app/mypage1.html', {})
        elif user_role == '2':
            return render(request, 'app/mypage2.html', {})
        elif user_role == '3':
            return render(request, 'app/mypage3.html', {})
        elif user_role == '4':
            return render(request, 'app/mypage4.html', {})
        else:
            return redirect('index')
    else:
        result_dict = {}
        user_id = request.session['user_id']
        user_pw = request.POST['user_pw']
        user_npw = request.POST['user_npw']
        user_cpw = request.POST['user_cpw']
        member = Member.objects.get(user_id=user_id)

        password = hashlib.sha256(user_pw.encode('utf-8')).hexdigest()
        new_password = hashlib.sha256(user_npw.encode('utf-8')).hexdigest()
        if member.user_pw == password and user_npw == user_cpw:
            member.user_pw = new_password
            member.save()
            result_dict['result'] = 'success'
            return JsonResponse(result_dict)

        else:
            result_dict['result'] = 'fail'
            return JsonResponse(result_dict)


def makeotp(request):
    if request.method == 'GET':
        user_role = request.session['user_role']
        if user_role == '1':
            return render(request, 'app/mypage1.html', {})
        elif user_role == '2':
            return render(request, 'app/mypage2.html', {})
        elif user_role == '3':
            return render(request, 'app/mypage3.html', {})
        elif user_role == '4':
            return render(request, 'app/mypage4.html', {})
        else:
            return redirect('index')
    else:
        user_id = request.session['user_id']
        otpkey = pyotp.random_base32()
        key = b'PvyhpBY3ACtXhj_wm9ueKhFSYyKAz4ntMc3p6sKYvuI='
        cipher_suite = Fernet(key)
        ciphered_text = cipher_suite.encrypt(b"%s" % bytes(otpkey.encode('utf-8')))
        with open('otpkey/%s.bin' % user_id, 'wb') as file_object:
            file_object.write(ciphered_text)
        otpsave = Member.objects.get(user_id=user_id)
        result_dict = {}

        if Member.objects.filter(user_id=user_id).values('otpkey')[0]['otpkey'] == '':
            otpsave.otpkey = "Issued"
            otpsave.save()
            data = pyotp.totp.TOTP(otpkey).provisioning_uri(user_id, issuer_name="Valkyrie App")
            output = {"otpkey": otpkey, 'data': data}
            return JsonResponse(output)
        else:
            result_dict['result'] = 'Already Issued'
            return JsonResponse(result_dict)


def mypage1(request):
    try:
        user_id = request.session['user_id']
        try:
            mytrade = Process.objects.filter(user1=user_id).order_by('-id')
            user_info = Member.objects.get(user_id=user_id)
            return render(request, 'app/mypage1.html', {'mytrade': mytrade, 'user_info': user_info})
        except:
            return render(request, 'app/mypage1.html', {})
    except:
        return redirect('index')


def mypage2(request):
    try:
        user_id = request.session['user_id']
        try:
            mytrade = Process.objects.filter(user2=user_id).order_by('-id')
            user_info = Member.objects.get(user_id=user_id)
            return render(request, 'app/mypage2.html', {'mytrade': mytrade, 'user_info': user_info})
        except:
            return render(request, 'app/mypage2.html', {})
    except:
        return redirect('index')


def mypage3(request):
    try:
        user_id = request.session['user_id']
        try:
            mytrade = Process.objects.filter(user3=user_id).order_by('-id')
            user_info = Member.objects.get(user_id=user_id)
            return render(request, 'app/mypage3.html', {'mytrade': mytrade, 'user_info': user_info})
        except:
            return render(request, 'app/mypage3.html', {})
    except:
        return redirect('index')


def mypage4(request):
    try:
        user_id = request.session['user_id']
        try:
            mytrade = Process.objects.filter(user4=user_id).order_by('-id')
            user_info = Member.objects.get(user_id=user_id)
            return render(request, 'app/mypage4.html', {'mytrade': mytrade, 'user_info': user_info})
        except:
            return render(request, 'app/mypage4.html', {})
    except:
        return redirect('index')


def about(request):
    return render(request, 'app/about.html', {})


def search1(request):
    try:
        cid = str(request.POST['cid'])
        url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
        res = requests.post(url)
        history = res.json()

        if len(history) == 0:
            return redirect('index')
        else:
            history.reverse()
            return render(request, 'app/search1.html', {'cid': cid, 'history': history, })
    except Exception as e:
        print(e)
        pass
    try:
        cid = str(request.POST['mytrade'])
        url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
        res = requests.post(url)
        history = res.json()

        if len(history) == 0:
            return render(request, 'app/mypage1.html', {})
        else:
            history.reverse()
            return render(request, 'app/search1.html', {'cid': cid, 'history': history, })
    except Exception as e:
        print(e)
        return redirect('index')


def search2(request):
    try:
        cid = str(request.POST['cid'])
        url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
        res = requests.post(url)
        history = res.json()

        if len(history) == 0:
            return redirect('index')
        else:
            history.reverse()
            return render(request, 'app/search2.html', {'cid': cid, 'history': history, })
    except Exception as e:
        print(e)
        pass
    try:
        cid = str(request.POST['mytrade'])
        url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
        res = requests.post(url)
        history = res.json()

        if len(history) == 0:
            return render(request, 'app/mypage2.html', {})
        else:
            history.reverse()
            return render(request, 'app/search2.html', {'cid': cid, 'history': history, })
    except Exception as e:
        print(e)
        return redirect('index')


def search3(request):
    try:
        cid = str(request.POST['cid'])
        url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
        res = requests.post(url)
        history = res.json()

        if len(history) == 0:
            return redirect('index')
        else:
            history.reverse()
            return render(request, 'app/search3.html', {'cid': cid, 'history': history, })
    except Exception as e:
        print(e)
        pass
    try:
        cid = str(request.POST['mytrade'])
        url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
        res = requests.post(url)
        history = res.json()

        if len(history) == 0:
            return render(request, 'app/mypage3.html', {})
        else:
            history.reverse()
            return render(request, 'app/search3.html', {'cid': cid, 'history': history, })
    except Exception as e:
        print(e)
        return redirect('index')


def search4(request):
    try:
        cid = str(request.POST['cid'])
        url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
        res = requests.post(url)
        history = res.json()

        if len(history) == 0:
            return redirect('index')
        else:
            history.reverse()
            return render(request, 'app/search4.html', {'cid': cid, 'history': history, })
    except Exception as e:
        print(e)
        pass
    try:
        cid = str(request.POST['mytrade'])
        url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
        res = requests.post(url)
        history = res.json()

        if len(history) == 0:
            return render(request, 'app/mypage4.html', {})
        else:
            history.reverse()
            return render(request, 'app/search4.html', {'cid': cid, 'history': history, })
    except Exception as e:
        print(e)
        return redirect('index')


def share1(request):
    try:
        otp = request.POST['otp']
        check_id = request.POST['check_id']
        share_user = request.POST['share_user']
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_LCR.objects.filter(owner=member)
        getid = contract.filter(id=check_id)
        hash = getid.values('sha256')[0]['sha256']
        contract_id = str(getid.values('contract_id')[0]['contract_id'])
        user_id = getid.values('owner')[0]['owner']

        urlhistory = ("http://222.239.231.247:8001/keyHistory/%s" % contract_id)
        urlto = requests.post(urlhistory)
        history = urlto.json()
        result_dict = {}

        key = b'PvyhpBY3ACtXhj_wm9ueKhFSYyKAz4ntMc3p6sKYvuI='
        cipher_suite = Fernet(key)
        with open('otpkey/%s.bin' % user_id, 'rb') as file_object:
            for line in file_object:
                encryptedpwd = line
        uncipher_text = cipher_suite.decrypt(encryptedpwd)
        otpkey = bytes(uncipher_text).decode("utf-8")

        totp = pyotp.TOTP(otpkey)
        nowotp = totp.now()
        try:
            if otp == nowotp and Member.objects.get(user_id=share_user):
                if history[0]['Value']['ci']['To'][11:] == user_id:
                    url = (
                            'http://222.239.231.247:8001/add_LCR/' + contract_id + '- importer: ' + user_id + '- bank: ' + share_user + '- letter of credit request: ' + hash)
                    response = requests.post(url)
                    res = response.text

                    if res == "Fail":
                        result_dict['result'] = 'Fail'

                    else:

                        process = Process.objects.get(id=contract_id)
                        process.user1 = user_id
                        process.LCR_hash = hash
                        process.user3 = share_user
                        process.save()

                        share = Contract_LCR.objects.get(id=check_id)
                        share.share3 = share_user
                        share.save()
                        result_dict['result'] = 'Success'
                    return JsonResponse(result_dict)
                else:
                    result_dict['result'] = "You don't have  the authority"
                    return JsonResponse(result_dict)
            else:
                result_dict['result'] = "Check OTP"
                return JsonResponse(result_dict)
        except:
            result_dict['result'] = 'Not found user'
            return JsonResponse(result_dict)
    except Exception as e:
        print(e)
        return redirect('ing')


def share2(request):
    try:
        otp = request.POST['otp']
        check_id = request.POST['check_id']
        share_user = request.POST['share_user']
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_CI.objects.filter(owner=member)
        getid = contract.filter(id=check_id)
        hash = getid.values('sha256')[0]['sha256']
        contract_id = str(getid.values('id')[0]['id'])
        user_id = getid.values('owner')[0]['owner']
        result_dict = {}

        key = b'PvyhpBY3ACtXhj_wm9ueKhFSYyKAz4ntMc3p6sKYvuI='
        cipher_suite = Fernet(key)
        with open('otpkey/%s.bin' % user_id, 'rb') as file_object:
            for line in file_object:
                encryptedpwd = line
        uncipher_text = cipher_suite.decrypt(encryptedpwd)
        otpkey = bytes(uncipher_text).decode("utf-8")
        totp = pyotp.TOTP(otpkey)
        nowotp = totp.now()
        try:
            if otp == nowotp and Member.objects.get(user_id=share_user):
                url = 'http://222.239.231.247:8001/add_CI/' + contract_id + '- Exporter: ' + user_id + '- importer: ' + share_user + '- commercial invoice: ' + hash
                response = requests.post(url)
                res = response.text

                if res == "The contract already exists":
                    result_dict['result'] = 'Fail'
                else:
                    process = Process.objects.get(CI_hash=hash)
                    process.user1 = share_user
                    process.save()

                    share = Contract_CI.objects.get(id=check_id)
                    share.share1 = share_user
                    share.save()
                    result_dict['result'] = 'Success'
                return JsonResponse(result_dict)
            else:
                result_dict['result'] = "Check OTP"
                return JsonResponse(result_dict)
        except Exception as e:
            print(e)
            result_dict['result'] = 'Not found user'
            return JsonResponse(result_dict)

    except Exception as e:
        print(e)
        return redirect('ing2')


def share2_1(request):
    try:
        otp = request.POST['otp']
        check_id = request.POST['check_id']
        share_user = request.POST['share_user']
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_SR.objects.filter(owner=member)
        getid = contract.filter(id=check_id)
        hash = getid.values('sha256')[0]['sha256']
        contract_id = str(getid.values('contract_id')[0]['contract_id'])
        user_id = getid.values('owner')[0]['owner']

        urlhistory = ("http://222.239.231.247:8001/keyHistory/%s" % contract_id)
        urlto = requests.post(urlhistory)
        history = urlto.json()
        result_dict = {}

        key = b'PvyhpBY3ACtXhj_wm9ueKhFSYyKAz4ntMc3p6sKYvuI='
        cipher_suite = Fernet(key)
        with open('otpkey/%s.bin' % user_id, 'rb') as file_object:
            for line in file_object:
                encryptedpwd = line
        uncipher_text = cipher_suite.decrypt(encryptedpwd)
        otpkey = bytes(uncipher_text).decode("utf-8")
        totp = pyotp.TOTP(otpkey)
        nowotp = totp.now()
        try:
            if otp == nowotp and Member.objects.get(user_id=share_user):
                if history[2]['Value']['lc']['To'][11:] == user_id:
                    url = 'http://222.239.231.247:8001/add_SR/' + contract_id + '- exporter: ' + user_id + '- shipper: ' + share_user + '- shipping request: ' + hash
                    response = requests.post(url)
                    res = response.text

                    if res == "Fail":
                        result_dict['result'] = 'Fail'
                    else:

                        share = Contract_SR.objects.get(id=check_id)
                        share.share4 = share_user
                        share.save()

                        process = Process.objects.get(id=contract_id)
                        process.SR_hash = hash
                        process.user4 = share_user
                        process.save()
                        result_dict['result'] = 'Success'
                    return JsonResponse(result_dict)
                else:
                    result_dict['result'] = "You don't have  the authority"
                    return JsonResponse(result_dict)
            else:
                result_dict['result'] = "Check OTP"
                return JsonResponse(result_dict)
        except:
            result_dict['result'] = 'Not found user'
            return JsonResponse(result_dict)

    except Exception as e:
        print(e)
        return redirect('ing2_1')


def share3(request):
    try:
        otp = request.POST['otp']
        check_id = request.POST['check_id']
        share_user = request.POST['share_user']
        share_user2 = request.POST['share_user2']
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_LC.objects.filter(owner=member)
        getid = contract.filter(id=check_id)
        hash = getid.values('sha256')[0]['sha256']
        contract_id = str(getid.values('contract_id')[0]['contract_id'])
        user_id = getid.values('owner')[0]['owner']

        urlhistory = ("http://222.239.231.247:8001/keyHistory/%s" % contract_id)
        urlto = requests.post(urlhistory)
        history = urlto.json()
        result_dict = {}

        key = b'PvyhpBY3ACtXhj_wm9ueKhFSYyKAz4ntMc3p6sKYvuI='
        cipher_suite = Fernet(key)
        with open('otpkey/%s.bin' % user_id, 'rb') as file_object:
            for line in file_object:
                encryptedpwd = line
        uncipher_text = cipher_suite.decrypt(encryptedpwd)
        otpkey = bytes(uncipher_text).decode("utf-8")
        totp = pyotp.TOTP(otpkey)
        nowotp = totp.now()
        try:
            if otp == nowotp and Member.objects.get(user_id=share_user) and Member.objects.get(user_id=share_user2):
                if history[1]['Value']['lcr']['To'][7:] == user_id:
                    url = 'http://222.239.231.247:8001/add_LC/' + contract_id + '- bank: ' + user_id + '- exporter: ' + share_user2 + '- letter of credit: ' + hash
                    response = requests.post(url)
                    res = response.text
                    result_dict = {}

                    if res == "Fail":
                        result_dict['result'] = 'Fail'
                    else:

                        process = Process.objects.get(id=contract_id)
                        process.LC_hash = hash
                        process.save()

                        share = Contract_LC.objects.get(id=check_id)
                        share.share1 = share_user
                        share.share2 = share_user2
                        share.save()
                        result_dict['result'] = 'Success'
                    return JsonResponse(result_dict)
                else:
                    result_dict['result'] = "You don't have  the authority"
                    return JsonResponse(result_dict)
            else:
                result_dict['result'] = "Check OTP"
                return JsonResponse(result_dict)
        except:
            result_dict['result'] = 'Not found user'
            return JsonResponse(result_dict)
    except Exception as e:
        print(e)
        return redirect('ing3')


def share4_1(request):
    try:
        otp = request.POST['otp']
        check_id = request.POST['check_id']
        share_user = request.POST['share_user']
        share_user2 = request.POST['share_user2']
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_BL.objects.filter(owner=member)
        getid = contract.filter(id=check_id)
        hash = getid.values('sha256')[0]['sha256']
        contract_id = str(getid.values('contract_id')[0]['contract_id'])
        user_id = getid.values('owner')[0]['owner']

        urlhistory = ("http://222.239.231.247:8001/keyHistory/%s" % contract_id)
        urlto = requests.post(urlhistory)
        history = urlto.json()
        result_dict = {}

        key = b'PvyhpBY3ACtXhj_wm9ueKhFSYyKAz4ntMc3p6sKYvuI='
        cipher_suite = Fernet(key)
        with open('otpkey/%s.bin' % user_id, 'rb') as file_object:
            for line in file_object:
                encryptedpwd = line
        uncipher_text = cipher_suite.decrypt(encryptedpwd)
        otpkey = bytes(uncipher_text).decode("utf-8")
        totp = pyotp.TOTP(otpkey)
        nowotp = totp.now()
        try:
            if otp == nowotp and Member.objects.get(user_id=share_user) and Member.objects.get(user_id=share_user2):
                if history[3]['Value']['sr']['To'][10:] == user_id:
                    url = 'http://222.239.231.247:8001/add_BL/' + contract_id + '- shipper: ' + user_id + '- importer: ' + share_user + '- bill of landing: ' + hash
                    response = requests.post(url)
                    res = response.text

                    if res == "Fail":
                        result_dict['result'] = 'Fail'
                    else:

                        process = Process.objects.get(id=contract_id)
                        process.BL_hash = hash
                        process.save()

                        share = Contract_BL.objects.get(id=check_id)
                        share.share1 = share_user
                        share.share2 = share_user2
                        share.save()

                        result_dict['result'] = 'Success'
                    return JsonResponse(result_dict)
                else:
                    result_dict['result'] = "You don't have  the authority"
                    return JsonResponse(result_dict)
            else:
                result_dict['result'] = "Check OTP"
                return JsonResponse(result_dict)
        except:
            result_dict['result'] = 'Not found user'
            return JsonResponse(result_dict)
    except:
        return redirect('ing4_1')


def share4_2(request):
    try:
        otp = request.POST['otp']
        check_id = request.POST['check_id']
        share_user = request.POST['share_user']
        share_user2 = request.POST['share_user2']
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_DO.objects.filter(owner=member)
        getid = contract.filter(id=check_id)
        hash = getid.values('sha256')[0]['sha256']
        contract_id = str(getid.values('contract_id')[0]['contract_id'])
        user_id = getid.values('owner')[0]['owner']

        urlhistory = ("http://222.239.231.247:8001/keyHistory/%s" % contract_id)
        urlto = requests.post(urlhistory)
        history = urlto.json()
        result_dict = {}

        key = b'PvyhpBY3ACtXhj_wm9ueKhFSYyKAz4ntMc3p6sKYvuI='
        cipher_suite = Fernet(key)
        with open('otpkey/%s.bin' % user_id, 'rb') as file_object:
            for line in file_object:
                encryptedpwd = line
        uncipher_text = cipher_suite.decrypt(encryptedpwd)
        otpkey = bytes(uncipher_text).decode("utf-8")
        totp = pyotp.TOTP(otpkey)
        nowotp = totp.now()
        try:
            if otp == nowotp and Member.objects.get(user_id=share_user) and Member.objects.get(user_id=share_user2):
                if history[4]['Value']['bl']['from'][10:] == user_id:
                    url = 'http://222.239.231.247:8001/add_DO/' + contract_id + '- shipper: ' + user_id + '- importer: ' + share_user + '- delivery order: ' + hash
                    response = requests.post(url)
                    res = response.text
                    result_dict = {}

                    if res == "Fail":
                        result_dict['result'] = 'Fail'
                    else:

                        process = Process.objects.get(id=contract_id)
                        process.DO_hash = hash
                        process.save()

                        share = Contract_DO.objects.get(id=check_id)
                        share.share1 = share_user
                        share.share3 = share_user2
                        share.save()

                        result_dict['result'] = 'Success'
                    return JsonResponse(result_dict)
                else:
                    result_dict['result'] = "You don't have  the authority"
                    return JsonResponse(result_dict)
            else:
                result_dict['result'] = "Check OTP"
                return JsonResponse(result_dict)
        except:
            result_dict['result'] = 'Not found user'
            return JsonResponse(result_dict)
    except Exception as e:
        print(e)
        return redirect('ing4_2')


def remove(request):
    check_id = request.GET['check_id']
    check_ids = check_id.split(',')

    try:
        for check_id in check_ids:
            Contract_LCR.objects.get(id=check_id).delete()
        return redirect('ing')
    except Exception as e:
        print(e)
        return redirect('ing')


def remove2(request):
    check_id = request.GET['check_id']
    check_ids = check_id.split(',')

    try:
        for check_id in check_ids:
            Contract_CI.objects.get(id=check_id).delete()
        return redirect('ing2')
    except Exception as e:
        print(e)
        return redirect('ing2')


def remove2_1(request):
    check_id = request.GET['check_id']
    check_ids = check_id.split(',')

    try:
        for check_id in check_ids:
            Contract_SR.objects.get(id=check_id).delete()
        return redirect('ing2_1')
    except Exception as e:
        print(e)
        return redirect('ing2_1')


def remove3(request):
    check_id = request.GET['check_id']
    check_ids = check_id.split(',')

    try:
        for check_id in check_ids:
            Contract_LC.objects.get(id=check_id).delete()
        return redirect('ing3')
    except Exception as e:
        print(e)
        return redirect('ing3')


def remove4_1(request):
    check_id = request.GET['check_id']
    check_ids = check_id.split(',')

    try:
        for check_id in check_ids:
            Contract_BL.objects.get(id=check_id).delete()
        return redirect('ing4_1')
    except Exception as e:
        print(e)
        return redirect('ing4_1')


def remove4_2(request):
    check_id = request.GET['check_id']
    check_ids = check_id.split(',')

    try:
        for check_id in check_ids:
            Contract_DO.objects.get(id=check_id).delete()
        return redirect('ing4_2')
    except Exception as e:
        print(e)
        return redirect('ing4_2')


def ciremove(request):
    # deletes all objects from Car database table
    # Contract.objects.get('id').delete()
    check_id = request.GET['check_id']
    check_ids = check_id.split(',')

    for id in check_ids:
        try:
            share = Contract_CI.objects.get(id=id)
            share.share1 = ' '
            share.save()
        except:
            pass
    return redirect('cireceived')


def blremove1(request):
    # deletes all objects from Car database table
    # Contract.objects.get('id').delete()
    check_id = request.GET['check_id']
    check_ids = check_id.split(',')

    for id in check_ids:
        try:
            share = Contract_BL.objects.get(id=id)
            share.share1 = ' '
            share.save()
        except:
            pass
    return redirect('blreceived1')


def lcremove1(request):
    # deletes all objects from Car database table
    # Contract.objects.get('id').delete()
    check_id = request.GET['check_id']
    check_ids = check_id.split(',')

    for id in check_ids:
        try:
            share = Contract_LC.objects.get(id=id)
            share.share1 = ' '
            share.save()
        except:
            pass
    return redirect('lcreceived1')


def blremove2(request):
    # deletes all objects from Car database table
    # Contract.objects.get('id').delete()
    check_id = request.GET['check_id']
    check_ids = check_id.split(',')

    for id in check_ids:
        try:
            share = Contract_BL.objects.get(id=id)
            share.share2 = ' '
            share.save()
        except:
            pass
    return redirect('blreceived2')


def lcremove2(request):
    # deletes all objects from Car database table
    # Contract.objects.get('id').delete()
    check_id = request.GET['check_id']
    check_ids = check_id.split(',')

    for id in check_ids:
        try:
            share = Contract_LC.objects.get(id=id)
            share.share2 = ' '
            share.save()
        except:
            pass
    return redirect('lcreceived2')


def doremove(request):
    # deletes all objects from Car database table
    # Contract.objects.get('id').delete()
    check_id = request.GET['check_id']
    check_ids = check_id.split(',')

    for id in check_ids:
        try:
            share = Contract_DO.objects.get(id=id)
            share.share1 = ' '
            share.save()
        except:
            pass
    return redirect('doreceived')


def doremove2(request):
    # deletes all objects from Car database table
    # Contract.objects.get('id').delete()
    check_id = request.GET['check_id']
    check_ids = check_id.split(',')

    for id in check_ids:
        try:
            share = Contract_DO.objects.get(id=id)
            share.share3 = ' '
            share.save()
        except:
            pass
    return redirect('doreceived2')


def lcrremove(request):
    # deletes all objects from Car database table
    # Contract.objects.get('id').delete()
    check_id = request.GET['check_id']
    check_ids = check_id.split(',')

    for id in check_ids:
        try:
            share = Contract_LCR.objects.get(id=id)
            share.share3 = ' '
            share.save()
        except:
            pass
    return redirect('lcrreceived')


def srremove(request):
    # deletes all objects from Car database table
    # Contract.objects.get('id').delete()
    check_id = request.GET['check_id']
    check_ids = check_id.split(',')

    for id in check_ids:
        try:
            share = Contract_SR.objects.get(id=id)
            share.share4 = ' '
            share.save()
        except:
            pass
    return redirect('cireceived')


def submit(request):
    try:
        user_id = request.session['user_id']
        contractname = request.POST['contractname']
        contract_id = request.POST['contract_id']
        a = request.POST['a']
        b = request.POST['b']
        c = request.POST['c']
        d = request.POST['d']
        e = request.POST['e']
        f = request.POST['f']
        g = request.POST['g']
        h = request.POST['h']
        i = request.POST['i']
        j = request.POST['j']
        k = request.POST['k']
        l = request.POST['l']
        m = request.POST['m']
        n = request.POST['n']
        o = request.POST['o']
        time_format = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))

        try:
            pdf = FPDF(unit='in', format='A4')
            pdf.add_page()
            pdf.set_font('Arial', '', 10.0)
            epw = pdf.w - 2 * pdf.l_margin
            records = [['No.', 'title', 'content'],
                       [1, 'Advising bank:', a],
                       [2, 'Credit No.:', b],
                       [3, 'Beneficiary:', c],
                       [4, 'Applicant:', d],
                       [5, 'L/C Amount and Tolerance:', e],
                       [6, 'Type:', f],
                       [7, 'Partial shipment:', g],
                       [8, 'Transshipment:', h],
                       [9, 'Trnasport mode:', i],
                       [10, 'Loading(shipment from):', j],
                       [11, 'Discharging(shipment to):', k],
                       [12, 'Latest shipment date:', l],
                       [13, 'All banking charges:', m],
                       [14, 'Confirmation:', n],
                       [15, 'T/T reimbursement:', o],
                       ]

            pdf.set_font('Arial', 'B', 14.0)
            pdf.cell(epw, 0.0, 'Contract ID:' + contract_id + '/' + time_format, align='C')
            pdf.ln(0.25)
            pdf.set_font('Arial', '', 12.0)
            pdf.cell(epw, 0.0, contractname + ' From:' + user_id, align='C')
            pdf.set_font('Arial', '', 10.0)
            pdf.ln(0.5)

            th = pdf.font_size
            for row in records:
                pdf.cell(0.5, 2 * th, str(row[0]), border=1, align='C')
                pdf.cell(3.5, 2 * th, str(row[1]), border=1)
                pdf.cell(3.5, 2 * th, str(row[2]), border=1)
                pdf.ln(2 * th)

            pdf.output('document/LCR_' + time_format + '.pdf', 'F')
            file = open('document/LCR_' + time_format + '.pdf', 'rb')
            data = file.read()

            hash = hashlib.sha256(data).hexdigest()
            file.close()

            # 데이터 저장
            contract = Contract_LCR(contractname=contractname, contract_id=contract_id, sha256=hash,
                                    filename='document/LCR_' + time_format + '.pdf')

            # 로그인한 사용자 정보를 Contract에 같이 저장
            user_id = request.session['user_id']
            member = Member.objects.get(user_id=user_id)
            contract.owner = member
            contract.save()
            return redirect('ing')
        except Exception as e:
            print(e)
            return redirect('forms')
    except:
        return redirect('forms')


def submit2(request):
    try:
        user_id = request.session['user_id']
        invoicename = request.POST['invoicename']

        a = request.POST['a']
        b = request.POST['b']
        c = request.POST['c']
        d = request.POST['d']
        e = request.POST['e']
        f = request.POST['f']
        g = request.POST['g']
        h = request.POST['h']
        i = request.POST['i']
        j = request.POST['j']
        k = request.POST['k']
        l = request.POST['l']
        m = request.POST['m']
        n = request.POST['n']
        o = request.POST['o']
        p = request.POST['p']
        q = request.POST['q']

        time_format = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
        try:
            pdf = FPDF(unit='in', format='A4')
            pdf.add_page()

            pdf.set_font('Arial', '', 10.0)
            epw = pdf.w - 2 * pdf.l_margin
            records = [['No.', 'title', 'content'],
                       [1, 'Shipper/Seller:', a],
                       [2, 'Consignee:', b],
                       [3, 'Departure Date:', c],
                       [4, 'Vessel/Flight:', d],
                       [5, 'To:', e],
                       [6, 'From:', f],
                       [7, 'Invoice No.and Date:', g],
                       [8, 'L/C No.and Date:', h],
                       [9, 'Buyer(if other than consignee):', i],
                       [10, 'Other reference:', j],
                       [11, 'Terms of delivery and payment:', k],
                       [12, 'Shipping Mark:', l],
                       [13, 'No.and kind of packages:', m],
                       [14, 'Goods description:', n],
                       [15, 'Quantity:', o],
                       [16, 'Unit price:', p],
                       [17, 'Amount:', q],
                       ]
            tag = invoicename + '/' + time_format

            pdf.set_font('Arial', 'B', 14.0)
            pdf.cell(epw, 0.0, u'%s' % tag, align='C')
            pdf.ln(0.25)
            pdf.set_font('Arial', '', 12.0)
            pdf.cell(epw, 0.0, 'CI From:' + user_id, align='C')
            pdf.set_font('Arial', '', 10.0)
            pdf.ln(0.5)

            th = pdf.font_size
            for row in records:
                pdf.cell(0.5, 2 * th, str(row[0]), border=1, align='C')
                pdf.cell(3.5, 2 * th, str(row[1]), border=1)
                pdf.cell(3.5, 2 * th, str(row[2]), border=1)
                pdf.ln(2 * th)

            pdf.output('document/CI_' + time_format + '.pdf', 'F')
            file = open('document/CI_' + time_format + '.pdf', 'rb')
            data = file.read()

            hash = hashlib.sha256(data).hexdigest()
            file.close()

            # 데이터 저장
            contract = Contract_CI(contractname=invoicename, sha256=hash,
                                   filename='document/CI_' + time_format + '.pdf')

            # 로그인한 사용자 정보를 Contract에 같이 저장
            user_id = request.session['user_id']
            member = Member.objects.get(user_id=user_id)
            contract.owner = member
            contract.save()
            id = Contract_CI.objects.filter(sha256=hash).values('id')[0]['id']

            process = Process(contract_id=id, user2=user_id, CI_hash=hash)
            process.save()

            return redirect('ing2')
        except Exception as e:
            print(e)
            return redirect('forms2')
    except:
        return redirect('forms2')


def submit2_1(request):
    try:
        user_id = request.session['user_id']
        srname = request.POST['srequestname']
        contract_id = request.POST['contract_id']
        a = request.POST['a']
        b = request.POST['b']
        c = request.POST['c']
        d = request.POST['d']
        e = request.POST['e']
        f = request.POST['f']
        g = request.POST['g']
        h = request.POST['h']
        i = request.POST['i']
        j = request.POST['j']
        k = request.POST['k']
        l = request.POST['l']
        m = request.POST['m']
        n = request.POST['n']
        o = request.POST['o']
        time_format = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))

        try:
            pdf = FPDF(unit='in', format='A4')
            pdf.add_page()
            pdf.set_font('Arial', '', 10.0)
            epw = pdf.w - 2 * pdf.l_margin
            records = [['No.', 'title', 'content'],
                       [1, 'Shipper:', a],
                       [2, 'Consignee:', b],
                       [3, 'Notify Party:', c],
                       [4, 'Vessel:', d],
                       [5, 'Voyage No.:', e],
                       [6, 'Port of Loading:', f],
                       [7, 'Port of Discharge:', g],
                       [8, 'Final Destination:', h],
                       [9, 'Marking:', i],
                       [10, 'Packages:', j],
                       [11, 'Description of Goods:', k],
                       [12, 'Gross Weight:', l],
                       [13, 'Measurement:', m],
                       [14, 'Freight Term:', n],
                       [15, 'Original B/L:', o],
                       ]

            pdf.set_font('Arial', 'B', 14.0)
            pdf.cell(epw, 0.0, 'Contract ID:' + contract_id + '/' + time_format, align='C')
            pdf.ln(0.25)
            pdf.set_font('Arial', '', 12.0)
            pdf.cell(epw, 0.0, srname + ' From:' + user_id, align='C')
            pdf.set_font('Arial', '', 10.0)
            pdf.ln(0.5)

            th = pdf.font_size
            for row in records:
                pdf.cell(0.5, 2 * th, str(row[0]), border=1, align='C')
                pdf.cell(3.5, 2 * th, str(row[1]), border=1)
                pdf.cell(3.5, 2 * th, str(row[2]), border=1)
                pdf.ln(2 * th)

            pdf.output('document/SR_' + time_format + '.pdf', 'F')
            file = open('document/SR_' + time_format + '.pdf', 'rb')
            data = file.read()

            hash = hashlib.sha256(data).hexdigest()
            file.close()

            # 데이터 저장
            contract = Contract_SR(contractname=srname, contract_id=contract_id, sha256=hash,
                                   filename='document/SR_' + time_format + '.pdf')

            # 로그인한 사용자 정보를 Contract에 같이 저장
            user_id = request.session['user_id']
            member = Member.objects.get(user_id=user_id)
            contract.owner = member

            contract.save()

            return redirect('ing2_1')
        except Exception as e:
            print(e)
            return redirect('forms2_1')
    except:
        return redirect('forms2_1')


def submit3(request):
    try:
        user_id = request.session['user_id']
        letteroflc = request.POST['letteroflc']
        contract_id = request.POST['contract_id']
        a = request.POST['a']
        b = request.POST['b']
        c = request.POST['c']
        d = request.POST['d']
        e = request.POST['e']
        f = request.POST['f']
        g = request.POST['g']
        h = request.POST['h']
        i = request.POST['i']
        j = request.POST['j']
        k = request.POST['k']
        l = request.POST['l']
        m = request.POST['m']
        n = request.POST['n']
        o = request.POST['o']
        p = request.POST['p']
        q = request.POST['q']
        r = request.POST['r']
        s = request.POST['s']
        t = request.POST['t']
        u = request.POST['u']
        v = request.POST['v']
        w = request.POST['w']
        x = request.POST['x']
        y = request.POST['y']
        z = request.POST['z']
        aa = request.POST['aa']
        bb = request.POST['bb']
        cc = request.POST['cc']
        dd = request.POST['dd']
        ee = request.POST['ee']
        ff = request.POST['ff']
        gg = request.POST['gg']

        time_format = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))

        try:
            pdf = FPDF(unit='in', format='A4')
            pdf.add_page()
            pdf.set_font('Arial', '', 10.0)
            epw = pdf.w - 2 * pdf.l_margin
            records = [['No.', 'title', 'content'],
                       [1, 'Transfer:', a],
                       [2, 'Credit Number:', b],
                       [3, 'Advising Bank:', c],
                       [4, 'Expiry Date:', d],
                       [5, 'Applicant:', e],
                       [6, 'Beneficiary:', f],
                       [7, 'Amount:', g],
                       [8, 'Partial Shipment:', h],
                       [9, 'Latest Shipment Date:', i],
                       [10, 'Additional Conditions:', j],
                       [11, 'All banking charges:', k],
                       [12, 'Documents delivered by:', l],
                       [13, 'Confirmation:', m],
                       [14, 'Reissue:', n],
                       [15, 'Import L/C Transfer:', o],
                       [16, 'Draft at:', p],
                       [17, 'Usance:', q],
                       [18, 'SettlingBank:', r],
                       [19, 'Credit:', s],
                       [20, 'Transshipment mode:', t],
                       [21, 'Authorization:', u],
                       [22, 'Port of Loading/Airport of Departure:', v],
                       [23, 'Place of Taking in Charge:', w],
                       [24, 'Signed/Original/Commercial Invoice:', x],
                       [25, 'Full Set of B/L:', y],
                       [26, 'Port of Loading:', z],
                       [27, 'Certificate of Origin in:', aa],
                       [28, 'Other Documents Required:', bb],
                       [29, 'Description of Goods/Services:', cc],
                       [30, 'Price Terms:', dd],
                       [31, 'Country of Origin:', ee],
                       [32, 'HS CODE:', ff],
                       [33, 'CommodityDescription:', gg],
                       ]

            pdf.set_font('Arial', 'B', 14.0)
            pdf.cell(epw, 0.0, 'Contract ID:' + contract_id + '/' + time_format, align='C')
            pdf.ln(0.25)
            pdf.set_font('Arial', '', 12.0)
            pdf.cell(epw, 0.0, letteroflc + ' From:' + user_id, align='C')
            pdf.set_font('Arial', '', 10.0)
            pdf.ln(0.5)

            th = pdf.font_size
            for row in records:
                pdf.cell(0.5, 2 * th, str(row[0]), border=1, align='C')
                pdf.cell(3.5, 2 * th, str(row[1]), border=1)
                pdf.cell(3.5, 2 * th, str(row[2]), border=1)
                pdf.ln(2 * th)

            pdf.output('document/LC_' + time_format + '.pdf', 'F')
            file = open('document/LC_' + time_format + '.pdf', 'rb')
            data = file.read()

            hash = hashlib.sha256(data).hexdigest()
            file.close()
            # 데이터 저장
            contract = Contract_LC(contractname=letteroflc, contract_id=contract_id, sha256=hash,
                                   filename='document/LC_' + time_format + '.pdf')

            # 로그인한 사용자 정보를 Contract에 같이 저장
            user_id = request.session['user_id']
            member = Member.objects.get(user_id=user_id)
            contract.owner = member

            contract.save()

            return redirect('ing3')
        except Exception as e:
            print(e)
            return redirect('forms3')
    except:
        return redirect('forms3')


def submit4_1(request):
    try:
        user_id = request.session['user_id']
        contractname = request.POST['contractname']
        contract_id = request.POST['contract_id']
        a = request.POST['a']
        b = request.POST['b']
        c = request.POST['c']
        d = request.POST['d']
        e = request.POST['e']
        f = request.POST['f']
        g = request.POST['g']
        h = request.POST['h']
        i = request.POST['i']
        j = request.POST['j']

        time_format = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
        try:
            pdf = FPDF(unit='in', format='A4')
            pdf.add_page()
            pdf.set_font('Arial', '', 10.0)
            epw = pdf.w - 2 * pdf.l_margin
            records = [['No.', 'title', 'content'],
                       [1, 'Bank:', a],
                       [2, 'Nodify party:', b],
                       [3, 'Vessel:', c],
                       [4, 'Voyage No.:', d],
                       [5, 'Place of receipt:', e],
                       [6, 'Port of Loading:', f],
                       [7, 'Place of delivery:', g],
                       [8, 'Description of goods:', h],
                       [9, 'Weight:', i],
                       [10, 'Measurement:', j],
                       ]

            pdf.set_font('Arial', 'B', 14.0)
            pdf.cell(epw, 0.0, 'Contract ID:' + contract_id + '/' + time_format, align='C')
            pdf.ln(0.25)
            pdf.set_font('Arial', '', 12.0)
            pdf.cell(epw, 0.0, contractname + ' From:' + user_id, align='C')
            pdf.set_font('Arial', '', 10.0)
            pdf.ln(0.5)

            th = pdf.font_size
            for row in records:
                pdf.cell(0.5, 2 * th, str(row[0]), border=1, align='C')
                pdf.cell(3.5, 2 * th, str(row[1]), border=1)
                pdf.cell(3.5, 2 * th, str(row[2]), border=1)
                pdf.ln(2 * th)

            pdf.output('document/BL_' + time_format + '.pdf', 'F')
            file = open('document/BL_' + time_format + '.pdf', 'rb')
            data = file.read()

            hash = hashlib.sha256(data).hexdigest()
            file.close()

            # 데이터 저장
            contract = Contract_BL(contractname=contractname, contract_id=contract_id, sha256=hash,
                                   filename='document/BL_' + time_format + '.pdf')

            # 로그인한 사용자 정보를 Contract에 같이 저장
            user_id = request.session['user_id']
            member = Member.objects.get(user_id=user_id)
            contract.owner = member

            contract.save()

            return redirect('ing4_1')
        except Exception as e:
            print(e)
            return redirect('forms4_1')
    except:
        return redirect('forms4_1')


def submit4_2(request):
    try:
        user_id = request.session['user_id']
        contractname = request.POST['contractname']
        contract_id = request.POST['contract_id']
        a = request.POST['a']
        b = request.POST['b']
        c = request.POST['c']
        d = request.POST['d']
        e = request.POST['e']
        f = request.POST['f']
        g = request.POST['g']

        time_format = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))

        try:
            pdf = FPDF(unit='in', format='A4')
            pdf.add_page()
            pdf.set_font('Arial', '', 10.0)
            epw = pdf.w - 2 * pdf.l_margin
            records = [['No.', 'title', 'content'],
                       [1, 'Agent name:', a],
                       [2, 'Restricted delivery(Yes or no):', b],
                       [3, 'Adult signature restriced delivery(Yes or no):', c],
                       [4, 'Agent Signture:', d],
                       [5, 'ID verified (yes or no):', e],
                       [6, 'USPS initals:', f],
                       [7, 'Date:', g],
                       ]

            pdf.set_font('Arial', 'B', 14.0)
            pdf.cell(epw, 0.0, 'Contract ID:' + contract_id + '/' + time_format, align='C')
            pdf.ln(0.25)
            pdf.set_font('Arial', '', 12.0)
            pdf.cell(epw, 0.0, contractname + ' From:' + user_id, align='C')
            pdf.set_font('Arial', '', 10.0)
            pdf.ln(0.5)

            th = pdf.font_size
            for row in records:
                pdf.cell(0.5, 2 * th, str(row[0]), border=1, align='C')
                pdf.cell(3.5, 2 * th, str(row[1]), border=1)
                pdf.cell(3.5, 2 * th, str(row[2]), border=1)
                pdf.ln(2 * th)

            pdf.output('document/DO_' + time_format + '.pdf', 'F')
            file = open('document/DO_' + time_format + '.pdf', 'rb')
            data = file.read()

            hash = hashlib.sha256(data).hexdigest()
            file.close()
            # 데이터 저장
            contract = Contract_DO(contractname=contractname, contract_id=contract_id, sha256=hash,
                                   filename='document/DO_' + time_format + '.pdf')

            # 로그인한 사용자 정보를 Contract에 같이 저장
            user_id = request.session['user_id']
            member = Member.objects.get(user_id=user_id)
            contract.owner = member
            contract.save()

            return redirect('ing4_2')
        except Exception as e:
            print(e)
            return redirect('forms4_2')
    except:
        return redirect('forms4_2')


def download(request):
    id = request.GET['id']
    c = Contract_LCR.objects.get(id=id)

    filepath = os.path.join(settings.BASE_DIR, c.filename)
    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
        return response


def download2(request):
    id = request.GET['id']
    c = Contract_CI.objects.get(id=id)

    filepath = os.path.join(settings.BASE_DIR, c.filename)
    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
        return response


def download2_1(request):
    id = request.GET['id']
    c = Contract_SR.objects.get(id=id)

    filepath = os.path.join(settings.BASE_DIR, c.filename)
    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
        return response


def download3(request):
    id = request.GET['id']
    c = Contract_LC.objects.get(id=id)

    filepath = os.path.join(settings.BASE_DIR, c.filename)
    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
        return response


def download4_1(request):
    id = request.GET['id']
    c = Contract_BL.objects.get(id=id)

    filepath = os.path.join(settings.BASE_DIR, c.filename)
    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
        return response


def download4_2(request):
    id = request.GET['id']
    c = Contract_DO.objects.get(id=id)
    print(c.filename)

    filepath = os.path.join(settings.BASE_DIR, c.filename)
    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
        return response


def ing(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_LCR.objects.filter(owner=member).order_by('-id')
        total_len = len(contract)
        page = request.GET.get('page')
        paginator = Paginator(contract, 6)

        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        index = lines.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 5 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2}

        return render(request, 'app/ing.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def ing2(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_CI.objects.filter(owner=member).order_by('-id')
        n = len(contract)
        total_len = len(contract)
        page = request.GET.get('page')
        paginator = Paginator(contract, 6)

        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        index = lines.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 5 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2}

        return render(request, 'app/ing2.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def ing2_1(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_SR.objects.filter(owner=member).order_by('-id')
        total_len = len(contract)
        page = request.GET.get('page')
        paginator = Paginator(contract, 6)

        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        index = lines.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 5 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2}

        return render(request, 'app/ing2_1.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def ing3(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_LC.objects.filter(owner=member).order_by('-id')
        total_len = len(contract)
        page = request.GET.get('page')
        paginator = Paginator(contract, 6)

        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        index = lines.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 5 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2}

        return render(request, 'app/ing3.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def ing4_1(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_BL.objects.filter(owner=member).order_by('-id')
        total_len = len(contract)
        page = request.GET.get('page')
        paginator = Paginator(contract, 6)

        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        index = lines.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 5 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2}

        return render(request, 'app/ing4_1.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def ing4_2(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_DO.objects.filter(owner=member).order_by('-id')
        total_len = len(contract)
        page = request.GET.get('page')
        paginator = Paginator(contract, 6)

        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        index = lines.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 5 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2}

        return render(request, 'app/ing4_2.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def cireceived(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_CI.objects.filter(share1=member).order_by('-id')
        total_len = len(contract)
        page = request.GET.get('page')
        paginator = Paginator(contract, 6)

        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        index = lines.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 5 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len,
                  'max_index': max_index - 2}

        return render(request, 'app/cireceived.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def srreceived(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_SR.objects.filter(share4=member).order_by('-id')
        total_len = len(contract)
        page = request.GET.get('page')
        paginator = Paginator(contract, 6)

        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        index = lines.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 5 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len,
                  'max_index': max_index - 2}

        return render(request, 'app/srreceived.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def blreceived1(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_BL.objects.filter(share1=member).order_by('-id')
        total_len = len(contract)
        page = request.GET.get('page')
        paginator = Paginator(contract, 6)

        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        index = lines.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 5 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len,
                  'max_index': max_index - 2}

        return render(request, 'app/blreceived1.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def lcreceived1(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_LC.objects.filter(share1=member).order_by('-id')
        total_len = len(contract)
        page = request.GET.get('page')
        paginator = Paginator(contract, 6)

        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        index = lines.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 5 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len,
                  'max_index': max_index - 2}

        return render(request, 'app/lcreceived1.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def blreceived2(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_BL.objects.filter(share2=member).order_by('-id')
        total_len = len(contract)
        page = request.GET.get('page')
        paginator = Paginator(contract, 6)

        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        index = lines.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 5 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len,
                  'max_index': max_index - 2}

        return render(request, 'app/blreceived2.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def lcreceived2(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_LC.objects.filter(share2=member).order_by('-id')
        total_len = len(contract)
        page = request.GET.get('page')
        paginator = Paginator(contract, 6)

        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        index = lines.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 5 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len,
                  'max_index': max_index - 2}

        return render(request, 'app/lcreceived2.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def doreceived(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_DO.objects.filter(share1=member).order_by('-id')
        total_len = len(contract)
        page = request.GET.get('page')
        paginator = Paginator(contract, 6)

        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        index = lines.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 5 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len,
                  'max_index': max_index - 2}

        return render(request, 'app/doreceived.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def doreceived2(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_DO.objects.filter(share3=member).order_by('-id')
        total_len = len(contract)
        page = request.GET.get('page')
        paginator = Paginator(contract, 6)

        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        index = lines.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 5 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len,
                  'max_index': max_index - 2}

        return render(request, 'app/doreceived2.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def lcrreceived(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        contract = Contract_LCR.objects.filter(share3=member).order_by('-id')
        total_len = len(contract)
        page = request.GET.get('page')
        paginator = Paginator(contract, 6)

        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        index = lines.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 5 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len,
                  'max_index': max_index - 2}

        return render(request, 'app/lcrreceived.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def logout(request):
    try:
        del request.session['user_role']
        del request.session['user_id']
        return redirect('login')
    except:
        return render(request, 'app/login.html', {})


def index(request):

    try:

        user_id = request.session['user_id']
        user_role = request.session['user_role']

        client_id = 'fpYuQKVX8str1aSVFrkc'
        client_secret = 'rLcccdn5R4'
        encText = urllib.parse.quote("국제무역,무역거래")
        url = "https://openapi.naver.com/v1/search/news?query=" + encText + '&sort=date'
        res = urllib.request.Request(url)
        res.add_header("X-Naver-Client-Id", client_id)
        res.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(res)
        result = response.read().decode('utf-8')

        news = json.loads(result)['items']
        time = json.loads(result)['lastBuildDate']

        title_list = []
        link_list = []
        for n in news:
            title = n['title'].replace('&quot;', '"').replace('&lt;', '<').replace('&gt;', '>').replace('<b>',
                                                                                                        '').replace(
                '</b>', '')
            title_list.append(title)
        for n in news:
            link = n['link']
            link_list.append(link)

        result = [{'title': title, 'link': link} for title, link in zip(title_list, link_list)]

        notice = Notice.objects.all().order_by('-id')

        templates = ''
        if user_role == '1':
            templates = 'app/index.html'
        elif user_role == '2':
            templates = 'app/index2.html'
        elif user_role == '3':
            templates = 'app/index3.html'
        elif user_role == '4':
            templates = 'app/index4.html'
        else:
            templates = 'app/login.html'

        return render(request, templates, {'user_id': user_id, 'date': time, 'notice': notice, 'result': result})
    except Exception as e:
        print(e)
        return redirect('login')


def charts(request):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    res1 = requests.get('https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD', headers=headers)
    json_data = res1.json()
    basePrice1 = json_data[0]['basePrice']
    sellprice1 = json_data[0]['cashSellingPrice']
    buyprice1 = json_data[0]['cashBuyingPrice']
    date1 = json_data[0]['date']
    time1 = json_data[0]['time']

    res2 = requests.get('https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWJPY', headers=headers)
    json_data = res2.json()
    basePrice2 = json_data[0]['basePrice']
    sellprice2 = json_data[0]['cashSellingPrice']
    buyprice2 = json_data[0]['cashBuyingPrice']

    res3 = requests.get('https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWCNY', headers=headers)
    json_data = res3.json()
    basePrice3 = json_data[0]['basePrice']
    sellprice3 = json_data[0]['cashSellingPrice']
    buyprice3 = json_data[0]['cashBuyingPrice']

    res4 = requests.get('https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWEUR', headers=headers)
    json_data = res4.json()
    basePrice4 = json_data[0]['basePrice']
    sellprice4 = json_data[0]['cashSellingPrice']
    buyprice4 = json_data[0]['cashBuyingPrice']

    try:

        user_role = request.session['user_role']

        templates = ''
        if user_role == '1':
            templates = 'app/charts.html'
        elif user_role == '2':
            templates = 'app/charts2.html'
        elif user_role == '3':
            templates = 'app/charts3.html'
        elif user_role == '4':
            templates = 'app/charts4.html'
        else:
            templates = 'app/login.html'

        return render(request, templates,
                      {'basePrice1': basePrice1, 'sellprice1': sellprice1, 'buyprice1': buyprice1, 'date1': date1,
                       'time1': time1,
                       'basePrice2': basePrice2, 'sellprice2': sellprice2, 'buyprice2': buyprice2,
                       'basePrice3': basePrice3, 'sellprice3': sellprice3, 'buyprice3': buyprice3,
                       'basePrice4': basePrice4, 'sellprice4': sellprice4, 'buyprice4': buyprice4})


    except Exception as e:
        print(e)
        return redirect('login')


def forms(request):
    user_id = request.session['user_id']
    contract = Contract_CI.objects.filter(share1=user_id).order_by('-id')
    return render(request, 'app/forms.html', {'contract': contract})


def forms2(request):
    user_id = request.session['user_id']
    return render(request, 'app/forms2.html', {'user_id':user_id})


def forms2_1(request):
    user_id = request.session['user_id']
    contract = Contract_LC.objects.filter(share2=user_id).order_by('-id')
    return render(request, 'app/forms2_1.html', {'contract': contract})


def forms3(request):
    user_id = request.session['user_id']
    contract = Contract_LCR.objects.filter(share3=user_id).order_by('-id')
    return render(request, 'app/forms3.html', {'contract': contract})


def forms4_1(request):
    user_id = request.session['user_id']
    contract = Contract_SR.objects.filter(share4=user_id).order_by('-id')
    return render(request, 'app/forms4_1.html', {'contract': contract})


def forms4_2(request):
    user_id = request.session['user_id']
    contract = Contract_BL.objects.filter(owner=user_id).order_by('-id')
    return render(request, 'app/forms4_2.html', {'contract': contract})


def login(request):
    if request.method == 'GET':
        return render(request, 'app/login.html', {})
    else:
        email = request.POST['email']
        user_pw = request.POST['password']
        user_role = request.POST['user_role']
        password = hashlib.sha256(user_pw.encode('utf-8')).hexdigest()
        result_dict = {}
        try:
            Member.objects.get(user_role=user_role, user_id=email, user_pw=password)
            result_dict['result'] = 'success'
            request.session['user_id'] = email
            request.session['user_role'] = user_role
        except Member.DoesNotExist:
            result_dict['result'] = 'fail'
        return JsonResponse(result_dict)


def registerpage(request):
    return render(request, 'app/register.html', {})


def register(request):
    result_dict = {}
    try:
        user_role = request.POST.get('user_role', False)
        user_name = request.POST.get('user_name', False)
        user_id = request.POST.get('user_id', False)
        user_pw = request.POST.get('user_pw', False)
        businessnum = request.POST['businessnum']
        tbc = request.POST['tbc']
        postcode = request.POST['postcode']
        address = request.POST['address']
        details = request.POST['details']
        extra = request.POST['extra']
        user_address = '(' + postcode + ')' + address + extra + ' ' + details

        password = hashlib.sha256(user_pw.encode('utf-8')).hexdigest()
        try:
            Member.objects.get(user_id=user_id)
            result_dict['result'] = '이미 가입된 아이디가 있습니다.'
        except Member.DoesNotExist:
            member = Member(user_role=user_role, user_id=user_id, user_pw=password, user_name=user_name,
                            address=user_address, tbc=tbc, businessnum=businessnum)
            member.c_date = timezone.now()
            member.save()
            result_dict['result'] = '가입완료'
        return JsonResponse(result_dict)
    except Exception as e:
        print(e)
        return redirect('registerpage')


def checkid(request):
    try:
        result_dict = {}
        user_id = request.POST['user_id']
        try:
            Member.objects.get(user_id=user_id)
            result_dict['result'] = "exist"
            return JsonResponse(result_dict)
        except:
            result_dict['result'] = "not exist"
            return JsonResponse(result_dict)
    except:
        pass


def forgot(request):
    if request.method == 'GET':
        return render(request, 'app/forgot.html', {})
    else:
        result_dict = {}
        try:

            user_email = request.POST['email']
            user_name = request.POST['name']
            new_pw = pyotp.random_base32()

            member_name = Member.objects.filter(user_id=user_email).values('user_name')[0]['user_name']
            menber_id = Member.objects.filter(user_id=user_email).values('user_id')[0]['user_id']

            if user_email == '' or user_name == '':
                result_dict['result'] = '공백은 사용 할 수 없습니다.'
                return JsonResponse(result_dict)

            elif user_name != member_name:
                result_dict['result'] = '이름이 일치하지 않습니다.'
                return JsonResponse(result_dict)

            elif user_email != menber_id:
                result_dict['result'] = '이메일이 일치하지 않습니다.'
                return JsonResponse(result_dict)

            else:
                try:
                    member = Member.objects.get(user_id=user_email)
                    member.user_pw = new_pw
                    member.save()

                    smtp_gmail = smtplib.SMTP('smtp.gmail.com', 587)
                    smtp_gmail.ehlo()

                    # 연결을 암호화
                    smtp_gmail.starttls()
                    smtp_gmail.login('saidtherapy23@gmail.com', 'erff8653!')
                    msg = EmailMessage()
                    msg['Subject'] = "새로운 비밀번호입니다"
                    # 내용 입력
                    msg.set_content("새로운 비밀번호는 %s 입니다." % new_pw)

                    # 보내는 사람
                    msg['From'] = 'Valkyrie Trade System'

                    # 밥는 사람
                    msg['To'] = '%s' % user_email

                    smtp_gmail.send_message(msg)
                    result_dict['result'] = 'Success'
                    return JsonResponse(result_dict)
                except Exception as e:
                    print(e)
                    result_dict['result'] = 'Fail'
                    return JsonResponse(result_dict)
        except Exception as e:
            print(e)
            result_dict['result'] = 'Fail'
            return JsonResponse(result_dict)
