import smtplib
import urllib.request
import requests
from email.message import EmailMessage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import hashlib

from django.views.decorators.csrf import csrf_exempt
from fpdf import FPDF, HTMLMixin
import pyotp
import os
import time
from pandas.io import json
from app.models import Contract_LCR, Member, Contract_OS, Contract_SR, Contract_BL, Contract_DO, Contract_LC, Process, \
    Notice, Contract_CI
from valweb import settings
from django.utils import timezone
from cryptography.fernet import Fernet


@csrf_exempt
def os_confirm(request):
    result_dict = {}
    try:
        user_id = request.session['user_id']
        contract_id = request.POST['c_id']
        c = Contract_OS.objects.get(id=contract_id)
        if c.status == 'new':
            otp = request.POST['otp']
            key = b'PvyhpBY3ACtXhj_wm9ueKhFSYyKAz4ntMc3p6sKYvuI='
            cipher_suite = Fernet(key)
            with open('otpkey/%s.bin' % user_id, 'rb') as file_object:
                for line in file_object:
                    encryptedpwd = line
            uncipher_text = cipher_suite.decrypt(encryptedpwd)
            otpkey = bytes(uncipher_text).decode("utf-8")
            totp = pyotp.TOTP(otpkey)
            nowotp = totp.now()
            owner = str(c.owner)
            share_user = c.share1
            hash = c.sha256
            if otp == nowotp:
                url = (
                        'http://222.239.231.247:8001/add_OS/' + contract_id + '- Exporter: ' + owner + '- importer: ' + share_user + '- offer sheet: ' + hash)
                response = requests.post(url)
                res = response.text
                if res == "The contract already exists":
                    result_dict['result'] = 'The contract already exists'
                else:
                    process = Process(contract_id=contract_id, user2=owner, OS_hash=hash, status='ing')
                    process.user1 = share_user
                    process.save()
                    c.status = 'confirmed'
                    c.save()
                    result_dict['result'] = 'success'
                    return JsonResponse(result_dict)
            else:
                result_dict['result'] = "Check OTP"
                return JsonResponse(result_dict)
        elif c.status == 'confirmed':
            result_dict['result'] = 'already confirmed'
        elif c.status == 'rejected':
            result_dict['result'] = 'already rejected'
        else:
            result_dict['result'] = 'locked'
    except Exception as e:
        result_dict['result'] = 'fail'
        print(e)
    return JsonResponse(result_dict)


@csrf_exempt
def lcr_confirm(request):
    result_dict = {}
    try:
        user_id = request.session['user_id']
        c_id = request.POST['c_id']
        c = Contract_LCR.objects.get(id=c_id)
        contract_id = c.contract_id
        if c.status == 'new':
            otp = request.POST['otp']
            key = b'PvyhpBY3ACtXhj_wm9ueKhFSYyKAz4ntMc3p6sKYvuI='
            cipher_suite = Fernet(key)
            with open('otpkey/%s.bin' % user_id, 'rb') as file_object:
                for line in file_object:
                    encryptedpwd = line
            uncipher_text = cipher_suite.decrypt(encryptedpwd)
            otpkey = bytes(uncipher_text).decode("utf-8")
            totp = pyotp.TOTP(otpkey)
            nowotp = totp.now()
            owner = str(c.owner)
            share_user = c.share3
            hash = c.sha256
            if otp == nowotp:
                url = (
                        'http://222.239.231.247:8001/add_LCR/' + contract_id + '- importer: ' + owner + '- bank: ' + share_user + '- letter of credit request: ' + hash)
                response = requests.post(url)
                res = response.text
                if res == "Fail":
                    result_dict['result'] = 'Fail'
                else:
                    process = Process.objects.get(contract_id=contract_id)
                    process.LCR_hash = hash
                    process.user3 = share_user
                    process.save()
                    c.status = 'confirmed'
                    c.save()
                    result_dict['result'] = 'success'
                return JsonResponse(result_dict)
            else:
                result_dict['result'] = "Check OTP"
                return JsonResponse(result_dict)
        elif c.status == 'confirmed':
            result_dict['result'] = 'already confirmed'
        elif c.status == 'rejected':
            result_dict['result'] = 'already rejected'
        else:
            result_dict['result'] = 'locked'
    except Exception as e:
        result_dict['result'] = 'fail'
        print(e)
    return JsonResponse(result_dict)


@csrf_exempt
def lc_confirm(request):
    result_dict = {}
    try:
        user_id = request.session['user_id']
        c_id = request.POST['c_id']
        c = Contract_LC.objects.get(id=c_id)
        contract_id = c.contract_id
        if c.status == 'new':
            otp = request.POST['otp']
            key = b'PvyhpBY3ACtXhj_wm9ueKhFSYyKAz4ntMc3p6sKYvuI='
            cipher_suite = Fernet(key)
            with open('otpkey/%s.bin' % user_id, 'rb') as file_object:
                for line in file_object:
                    encryptedpwd = line
            uncipher_text = cipher_suite.decrypt(encryptedpwd)
            otpkey = bytes(uncipher_text).decode("utf-8")
            totp = pyotp.TOTP(otpkey)
            nowotp = totp.now()
            owner = str(c.owner)
            share_user = c.share2
            hash = c.sha256
            if otp == nowotp:
                url = (
                        'http://222.239.231.247:8001/add_LC/' + contract_id + '- bank: ' + owner + '- exporter: ' + share_user + '- letter of credit: ' + hash)
                response = requests.post(url)
                res = response.text
                if res == "Fail":
                    result_dict['result'] = 'Fail'
                else:
                    process = Process.objects.get(contract_id=contract_id)
                    process.LC_hash = hash
                    process.save()
                    c.status = 'confirmed'
                    c.save()
                    result_dict['result'] = 'success'
                return JsonResponse(result_dict)
            else:
                result_dict['result'] = "Check OTP"
                return JsonResponse(result_dict)
        elif c.status == 'confirmed':
            result_dict['result'] = 'already confirmed'
        elif c.status == 'rejected':
            result_dict['result'] = 'already rejected'
        else:
            result_dict['result'] = 'locked'
    except Exception as e:
        result_dict['result'] = 'fail'
        print(e)
    return JsonResponse(result_dict)


@csrf_exempt
def sr_confirm(request):
    result_dict = {}
    try:
        user_id = request.session['user_id']
        c_id = request.POST['c_id']
        c = Contract_SR.objects.get(id=c_id)
        contract_id = c.contract_id
        if c.status == 'new':
            otp = request.POST['otp']
            key = b'PvyhpBY3ACtXhj_wm9ueKhFSYyKAz4ntMc3p6sKYvuI='
            cipher_suite = Fernet(key)
            with open('otpkey/%s.bin' % user_id, 'rb') as file_object:
                for line in file_object:
                    encryptedpwd = line
            uncipher_text = cipher_suite.decrypt(encryptedpwd)
            otpkey = bytes(uncipher_text).decode("utf-8")
            totp = pyotp.TOTP(otpkey)
            nowotp = totp.now()
            owner = str(c.owner)
            share_user = c.share4
            hash = c.sha256
            if otp == nowotp:
                url = (
                        'http://222.239.231.247:8001/add_SR/' + contract_id + '- exporter: ' + owner + '- shipper: ' + share_user + '- shipping request: ' + hash)
                response = requests.post(url)
                res = response.text
                if res == "Fail":
                    result_dict['result'] = 'Fail'
                else:
                    process = Process.objects.get(contract_id=contract_id)
                    process.SR_hash = hash
                    process.user4 = share_user
                    process.save()
                    c.status = 'confirmed'
                    c.save()
                    result_dict['result'] = 'success'
                return JsonResponse(result_dict)
            else:
                result_dict['result'] = "Check OTP"
                return JsonResponse(result_dict)
        elif c.status == 'confirmed':
            result_dict['result'] = 'already confirmed'
        elif c.status == 'rejected':
            result_dict['result'] = 'already rejected'
        else:
            result_dict['result'] = 'locked'
    except Exception as e:
        result_dict['result'] = 'fail'
        print(e)
    return JsonResponse(result_dict)


@csrf_exempt
def bl_confirm(request):
    result_dict = {}
    try:
        user_id = request.session['user_id']
        c_id = request.POST['c_id']
        c = Contract_BL.objects.get(id=c_id)
        contract_id = c.contract_id
        if c.status2 == 'new':
            otp = request.POST['otp']
            key = b'PvyhpBY3ACtXhj_wm9ueKhFSYyKAz4ntMc3p6sKYvuI='
            cipher_suite = Fernet(key)
            with open('otpkey/%s.bin' % user_id, 'rb') as file_object:
                for line in file_object:
                    encryptedpwd = line
            uncipher_text = cipher_suite.decrypt(encryptedpwd)
            otpkey = bytes(uncipher_text).decode("utf-8")
            totp = pyotp.TOTP(otpkey)
            nowotp = totp.now()

            if otp == nowotp:
                process = Process.objects.get(contract_id=contract_id)
                c.status2 = 'confirmed'
                c.status3 = 'new'
                c.share3 = process.user3
                c.save()
                result_dict['result'] = 'success'
                return JsonResponse(result_dict)
            else:
                result_dict['result'] = "Check OTP"
                return JsonResponse(result_dict)
        elif c.status2 == 'confirmed':
            result_dict['result'] = 'already confirmed'
        elif c.status2 == 'rejected':
            result_dict['result'] = 'already rejected'
        else:
            result_dict['result'] = 'locked'
    except Exception as e:
        result_dict['result'] = 'fail'
        print(e)
    return JsonResponse(result_dict)


@csrf_exempt
def bl_confirm1(request):
    result_dict = {}
    try:
        c_id = request.POST['c_id']
        c = Contract_BL.objects.get(id=c_id)
        if c.status1 == 'new':
            c.status1 = 'confirmed'
            c.save()
            result_dict['result'] = 'success'
            return JsonResponse(result_dict)
        elif c.status2 == 'confirmed':
            result_dict['result'] = 'already confirmed'
        else:
            result_dict['result'] = 'locked'
    except Exception as e:
        result_dict['result'] = 'fail'
        print(e)
    return JsonResponse(result_dict)


@csrf_exempt
def bl_confirm2(request):
    result_dict = {}
    try:
        user_id = request.session['user_id']
        c_id = request.POST['c_id']
        c = Contract_BL.objects.get(id=c_id)
        contract_id = c.contract_id
        if c.status3 == 'new':
            otp = request.POST['otp']
            key = b'PvyhpBY3ACtXhj_wm9ueKhFSYyKAz4ntMc3p6sKYvuI='
            cipher_suite = Fernet(key)
            with open('otpkey/%s.bin' % user_id, 'rb') as file_object:
                for line in file_object:
                    encryptedpwd = line
            uncipher_text = cipher_suite.decrypt(encryptedpwd)
            otpkey = bytes(uncipher_text).decode("utf-8")
            totp = pyotp.TOTP(otpkey)
            nowotp = totp.now()
            owner = str(c.owner)
            share_user = c.share2
            hash = c.sha256

            if otp == nowotp:
                url = (
                        'http://222.239.231.247:8001/add_BL/' + contract_id + '- shipper: ' + owner + '- exporter: ' + share_user + '- bills of letter: ' + hash)
                response = requests.post(url)
                res = response.text
                if res == "Fail":
                    result_dict['result'] = 'Fail'
                else:
                    process = Process.objects.get(contract_id=contract_id)
                    process.BL_hash = hash
                    process.save()
                    c.share1 = process.user1
                    c.status3 = 'confirmed'
                    c.status1 = 'new'
                    c.save()
                    result_dict['result'] = 'success'
                    return JsonResponse(result_dict)
            else:
                result_dict['result'] = "Check OTP"
                return JsonResponse(result_dict)
        elif c.status3 == 'confirmed':
            result_dict['result'] = 'already confirmed'
        elif c.status3 == 'rejected':
            result_dict['result'] = 'already rejected'
        else:
            result_dict['result'] = 'locked'
    except Exception as e:
        result_dict['result'] = 'fail'
        print(e)
    return JsonResponse(result_dict)


@csrf_exempt
def ci_confirm(request):
    result_dict = {}
    try:
        user_id = request.session['user_id']
        c_id = request.POST['c_id']
        c = Contract_CI.objects.get(id=c_id)
        contract_id = c.contract_id
        if c.status == 'new':
            otp = request.POST['otp']
            key = b'PvyhpBY3ACtXhj_wm9ueKhFSYyKAz4ntMc3p6sKYvuI='
            cipher_suite = Fernet(key)
            with open('otpkey/%s.bin' % user_id, 'rb') as file_object:
                for line in file_object:
                    encryptedpwd = line
            uncipher_text = cipher_suite.decrypt(encryptedpwd)
            otpkey = bytes(uncipher_text).decode("utf-8")
            totp = pyotp.TOTP(otpkey)
            nowotp = totp.now()
            owner = str(c.owner)
            share_user = c.share1
            hash = c.sha256
            if otp == nowotp:
                url = (
                        'http://222.239.231.247:8001/add_CI/' + contract_id + '- exporter: ' + owner + '- importer: ' + share_user + '- commercial invoice: ' + hash)
                response = requests.post(url)
                res = response.text
                if res == "Fail":
                    result_dict['result'] = 'Fail'
                else:
                    process = Process.objects.get(contract_id=contract_id)
                    process.CI_hash = hash
                    process.save()
                    c.status = 'confirmed'
                    c.save()
                    result_dict['result'] = 'success'
                return JsonResponse(result_dict)
            else:
                result_dict['result'] = "Check OTP"
                return JsonResponse(result_dict)
        elif c.status == 'confirmed':
            result_dict['result'] = 'already confirmed'
        elif c.status == 'rejected':
            result_dict['result'] = 'already rejected'
        else:
            result_dict['result'] = 'locked'
    except Exception as e:
        result_dict['result'] = 'fail'
        print(e)
    return JsonResponse(result_dict)


@csrf_exempt
def do_confirm(request):
    result_dict = {}
    try:
        user_id = request.session['user_id']
        c_id = request.POST['c_id']
        c = Contract_DO.objects.get(id=c_id)
        contract_id = c.contract_id
        if c.status == 'new':
            otp = request.POST['otp']
            key = b'PvyhpBY3ACtXhj_wm9ueKhFSYyKAz4ntMc3p6sKYvuI='
            cipher_suite = Fernet(key)
            with open('otpkey/%s.bin' % user_id, 'rb') as file_object:
                for line in file_object:
                    encryptedpwd = line
            uncipher_text = cipher_suite.decrypt(encryptedpwd)
            otpkey = bytes(uncipher_text).decode("utf-8")
            totp = pyotp.TOTP(otpkey)
            nowotp = totp.now()
            owner = str(c.owner)
            share_user = c.share1
            hash = c.sha256
            if otp == nowotp:
                url = (
                            'http://222.239.231.247:8001/add_DO/' + contract_id + '- shipper: ' + owner + '- importer: ' + share_user + '- delivery order: ' + hash)
                response = requests.post(url)
                res = response.text
                if res == "Fail":
                    result_dict['result'] = 'Fail'
                else:
                    process = Process.objects.get(contract_id=contract_id)
                    process.DO_hash = hash
                    process.status = 'complete'
                    process.save()
                    os_status = Contract_OS.objects.get(id=contract_id)
                    os_status.status = 'complete'
                    os_status.save()
                    lcr_status = Contract_LCR.objects.get(contract_id=contract_id)
                    lcr_status.status = 'complete'
                    lcr_status.save()
                    lc_status = Contract_LC.objects.get(contract_id=contract_id)
                    lc_status.status = 'complete'
                    lc_status.save()
                    sr_status = Contract_SR.objects.get(contract_id=contract_id)
                    sr_status.status = 'complete'
                    sr_status.save()
                    bl_status = Contract_BL.objects.get(contract_id=contract_id)
                    bl_status.status1 = 'complete'
                    bl_status.status2 = 'complete'
                    bl_status.status3 = 'complete'
                    bl_status.save()
                    ci_status = Contract_CI.objects.get(contract_id=contract_id)
                    ci_status.status = 'complete'
                    ci_status.save()
                    c.status = 'complete'
                    c.save()
                    result_dict['result'] = 'success'
                return JsonResponse(result_dict)
            else:
                result_dict['result'] = "Check OTP"
                return JsonResponse(result_dict)
        elif c.status == 'confirmed':
            result_dict['result'] = 'already confirmed'
        elif c.status == 'rejected':
            result_dict['result'] = 'already rejected'
        else:
            result_dict['result'] = 'locked'
    except Exception as e:
        result_dict['result'] = 'fail'
        print(e)
    return JsonResponse(result_dict)


@csrf_exempt
def os_reject(request):
    result_dict = {}
    try:
        contract_id = request.POST['c_id']
        c = Contract_OS.objects.get(id=contract_id)
        if c.status == 'new':
            c.status = 'rejected'
            c.share1 = ''
            c.save()
            result_dict['result'] = 'rejected'
        elif c.status == 'confirmed':
            result_dict['result'] = 'already confirmed'
        elif c.status == 'rejected':
            result_dict['result'] = 'already rejected'
        else:
            result_dict['result'] = 'locked'
    except Exception as e:
        result_dict['result'] = 'fail'
        print(e)
    return JsonResponse(result_dict)


@csrf_exempt
def lcr_reject(request):
    result_dict = {}
    try:
        contract_id = request.POST['c_id']
        c = Contract_LCR.objects.get(id=contract_id)
        if c.status == 'new':
            c.status = 'rejected'
            c.share3 = ''
            c.save()
            result_dict['result'] = 'rejected'
        elif c.status == 'confirmed':
            result_dict['result'] = 'already confirmed'
        elif c.status == 'rejected':
            result_dict['result'] = 'already rejected'
        else:
            result_dict['result'] = 'locked'
    except Exception as e:
        result_dict['result'] = 'fail'
        print(e)
    return JsonResponse(result_dict)


@csrf_exempt
def lc_reject(request):
    result_dict = {}
    try:
        contract_id = request.POST['c_id']
        c = Contract_LC.objects.get(id=contract_id)
        if c.status == 'new':
            c.status = 'rejected'
            c.share2 = ''
            c.save()
            result_dict['result'] = 'rejected'
        elif c.status == 'confirmed':
            result_dict['result'] = 'already confirmed'
        elif c.status == 'rejected':
            result_dict['result'] = 'already rejected'
        else:
            result_dict['result'] = 'locked'
    except Exception as e:
        result_dict['result'] = 'fail'
        print(e)
    return JsonResponse(result_dict)


@csrf_exempt
def sr_reject(request):
    result_dict = {}
    try:
        contract_id = request.POST['c_id']
        c = Contract_SR.objects.get(id=contract_id)
        if c.status == 'new':
            c.status = 'rejected'
            c.share4 = ''
            c.save()
            result_dict['result'] = 'rejected'
        elif c.status == 'confirmed':
            result_dict['result'] = 'already confirmed'
        elif c.status == 'rejected':
            result_dict['result'] = 'already rejected'
        else:
            result_dict['result'] = 'locked'
    except Exception as e:
        result_dict['result'] = 'fail'
        print(e)
    return JsonResponse(result_dict)


@csrf_exempt
def bl_reject(request):
    result_dict = {}
    try:
        contract_id = request.POST['c_id']
        c = Contract_BL.objects.get(id=contract_id)
        if c.status2 == 'new':
            c.status2 = 'rejected'
            c.share2 = ''
            c.save()
            result_dict['result'] = 'rejected'
        elif c.status2 == 'confirmed':
            result_dict['result'] = 'already confirmed'
        elif c.status2 == 'rejected':
            result_dict['result'] = 'already rejected'
        else:
            result_dict['result'] = 'locked'
    except Exception as e:
        result_dict['result'] = 'fail'
        print(e)
    return JsonResponse(result_dict)


@csrf_exempt
def bl_reject2(request):
    result_dict = {}
    try:
        contract_id = request.POST['c_id']
        c = Contract_BL.objects.get(id=contract_id)
        if c.status3 == 'new':
            c.status3 = 'rejected'
            c.share2 = ''
            c.save()
            result_dict['result'] = 'rejected'
        elif c.status3 == 'confirmed':
            result_dict['result'] = 'already confirmed'
        elif c.status3 == 'rejected':
            result_dict['result'] = 'already rejected'
        else:
            result_dict['result'] = 'locked'
    except Exception as e:
        result_dict['result'] = 'fail'
        print(e)
    return JsonResponse(result_dict)


@csrf_exempt
def ci_reject(request):
    result_dict = {}
    try:
        contract_id = request.POST['c_id']
        c = Contract_CI.objects.get(id=contract_id)
        if c.status == 'new':
            c.status = 'rejected'
            c.share1 = ''
            c.save()
            result_dict['result'] = 'rejected'
        elif c.status == 'confirmed':
            result_dict['result'] = 'already confirmed'
        elif c.status == 'rejected':
            result_dict['result'] = 'already rejected'
        else:
            result_dict['result'] = 'locked'
    except Exception as e:
        result_dict['result'] = 'fail'
        print(e)
    return JsonResponse(result_dict)


@csrf_exempt
def do_reject(request):
    result_dict = {}
    try:
        contract_id = request.POST['c_id']
        c = Contract_DO.objects.get(id=contract_id)
        if c.status == 'new':
            c.status = 'rejected'
            c.share1 = ''
            c.save()
            result_dict['result'] = 'rejected'
        elif c.status == 'confirmed':
            result_dict['result'] = 'already confirmed'
        elif c.status == 'rejected':
            result_dict['result'] = 'already rejected'
        else:
            result_dict['result'] = 'locked'
    except Exception as e:
        result_dict['result'] = 'fail'
        print(e)
    return JsonResponse(result_dict)


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
        user_id = request.session['user_id']
        if user_role == '1':
            return render(request, 'app/mypage1.html', {'user_id': user_id})
        elif user_role == '2':
            return render(request, 'app/mypage2.html', {'user_id': user_id})
        elif user_role == '3':
            return render(request, 'app/mypage3.html', {'user_id': user_id})
        elif user_role == '4':
            return render(request, 'app/mypage4.html', {'user_id': user_id})
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
        user_id = request.session['user_id']
        if user_role == '1':
            return render(request, 'app/mypage1.html', {'user_id': user_id})
        elif user_role == '2':
            return render(request, 'app/mypage2.html', {'user_id': user_id})
        elif user_role == '3':
            return render(request, 'app/mypage3.html', {'user_id': user_id})
        elif user_role == '4':
            return render(request, 'app/mypage4.html', {'user_id': user_id})
        else:
            return redirect('index')
    else:
        result_dict = {}
        try:

            mytrade = request.POST['mytrade']
            trade = Process.objects.filter(contract_id=mytrade).values('OS_hash', 'LCR_hash', 'LC_hash', 'SR_hash',
                                                                       'BL_hash',
                                                                       'CI_hash',
                                                                       'DO_hash')
            return JsonResponse({'trade': list(trade)})
        except Exception as e:
            result_dict['result'] = "Invalid Contract"
            return JsonResponse(result_dict)


def addressmodify(request):
    if request.method == 'GET':
        user_role = request.session['user_role']
        user_id = request.session['user_id']
        if user_role == '1':
            return render(request, 'app/mypage1.html', {'user_id': user_id})
        elif user_role == '2':
            return render(request, 'app/mypage2.html', {'user_id': user_id})
        elif user_role == '3':
            return render(request, 'app/mypage3.html', {'user_id': user_id})
        elif user_role == '4':
            return render(request, 'app/mypage4.html', {'user_id': user_id})
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
        user_id = request.session['user_id']
        if user_role == '1':
            return render(request, 'app/mypage1.html', {'user_id': user_id})
        elif user_role == '2':
            return render(request, 'app/mypage2.html', {'user_id': user_id})
        elif user_role == '3':
            return render(request, 'app/mypage3.html', {'user_id': user_id})
        elif user_role == '4':
            return render(request, 'app/mypage4.html', {'user_id': user_id})
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
        user_id = request.session['user_id']
        if user_role == '1':
            return render(request, 'app/mypage1.html', {'user_id': user_id})
        elif user_role == '2':
            return render(request, 'app/mypage2.html', {'user_id': user_id})
        elif user_role == '3':
            return render(request, 'app/mypage3.html', {'user_id': user_id})
        elif user_role == '4':
            return render(request, 'app/mypage4.html', {'user_id': user_id})
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

        if Member.objects.filter(user_id=user_id).values('otpkey')[0]['otpkey'] == 'Not yet issued':
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
            mytrade = Process.objects.filter(user1=user_id, status='ing').order_by('-id')
            complete = Process.objects.filter(user1=user_id, status='complete').order_by('-id')
            a = len(mytrade)
            b = len(complete)
            user_info = Member.objects.get(user_id=user_id)
            return render(request, 'app/mypage1.html',
                          {'mytrade': mytrade, 'user_info': user_info, 'complete': complete, 'a': a, 'b': b,
                           'user_id': user_id})
        except:
            return render(request, 'app/mypage1.html', {})
    except Exception as e:
        print(e)
        return redirect('index')


def mypage2(request):
    try:
        user_id = request.session['user_id']
        try:
            mytrade = Process.objects.filter(user2=user_id, status='ing').order_by('-id')
            complete = Process.objects.filter(user2=user_id, status='complete').order_by('-id')
            user_info = Member.objects.get(user_id=user_id)
            a = len(mytrade)
            b = len(complete)
            return render(request, 'app/mypage2.html',
                          {'mytrade': mytrade, 'user_info': user_info, 'complete': complete, 'a': a, 'b': b,
                           'user_id': user_id})
        except:
            return render(request, 'app/mypage2.html', {})
    except Exception as e:
        print(e)
        return redirect('index')


def mypage3(request):
    try:
        user_id = request.session['user_id']
        try:
            mytrade = Process.objects.filter(user3=user_id, status='ing').order_by('-id')
            complete = Process.objects.filter(user3=user_id, status='complete').order_by('-id')
            user_info = Member.objects.get(user_id=user_id)
            a = len(mytrade)
            b = len(complete)
            return render(request, 'app/mypage3.html',
                          {'mytrade': mytrade, 'user_info': user_info, 'complete': complete, 'a': a, 'b': b,
                           'user_id': user_id})
        except:
            return render(request, 'app/mypage3.html', {})
    except:
        return redirect('index')


def mypage4(request):
    try:
        user_id = request.session['user_id']
        try:
            mytrade = Process.objects.filter(user4=user_id, status='ing').order_by('-id')
            complete = Process.objects.filter(user4=user_id, status='complete').order_by('-id')
            user_info = Member.objects.get(user_id=user_id)
            a = len(mytrade)
            b = len(complete)
            return render(request, 'app/mypage4.html',
                          {'mytrade': mytrade, 'user_info': user_info, 'complete': complete, 'a': a, 'b': b,
                           'user_id': user_id})
        except:
            return render(request, 'app/mypage4.html', {})
    except:
        return redirect('index')


def about(request):
    return render(request, 'app/about.html', {})


def search1(request):
    user_id = request.session['user_id']
    try:
        cid = str(request.POST['cid'])
        url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
        res = requests.post(url)
        history = res.json()

        if len(history) == 0:
            return redirect('index')
        else:
            history.reverse()
            return render(request, 'app/search1.html', {'cid': cid, 'history': history, 'user_id': user_id})
    except Exception as e:
        print(e)
        pass
    try:
        cid = str(request.POST['mytrade'])
        url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
        res = requests.post(url)
        history = res.json()

        if len(history) == 0:
            return redirect('mypage1')
        else:
            history.reverse()
            return render(request, 'app/search1.html', {'cid': cid, 'history': history, 'user_id': user_id})
    except Exception as e:
        print(e)
        pass
    try:
        cid = str(request.POST['complete'])
        url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
        res = requests.post(url)
        history = res.json()

        if len(history) == 0:
            return redirect('mypage1')
        else:
            history.reverse()
            return render(request, 'app/search1.html', {'cid': cid, 'history': history, 'user_id': user_id})
    except Exception as e:
        print(e)
        return redirect('index')


def search2(request):
    user_id = request.session['user_id']
    try:
        cid = str(request.POST['cid'])
        url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
        res = requests.post(url)
        history = res.json()

        if len(history) == 0:
            return redirect('index2')
        else:
            history.reverse()
            return render(request, 'app/search2.html', {'cid': cid, 'history': history, 'user_id': user_id})
    except Exception as e:
        print(e)
        pass
    try:
        cid = str(request.POST['mytrade'])
        url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
        res = requests.post(url)
        history = res.json()

        if len(history) == 0:
            return redirect('mypage2')
        else:
            history.reverse()
            return render(request, 'app/search2.html', {'cid': cid, 'history': history, 'user_id': user_id})
    except Exception as e:
        print(e)
        pass
        try:
            cid = str(request.POST['complete'])
            url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
            res = requests.post(url)
            history = res.json()

            if len(history) == 0:
                return redirect('mypage2')
            else:
                history.reverse()
                return render(request, 'app/search1.html', {'cid': cid, 'history': history, 'user_id': user_id})
        except Exception as e:
            print(e)
            return redirect('index2')


def search3(request):
    user_id = request.session['user_id']
    try:
        cid = str(request.POST['cid'])
        url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
        res = requests.post(url)
        history = res.json()

        if len(history) == 0:
            return redirect('index3')
        else:
            history.reverse()
            return render(request, 'app/search3.html', {'cid': cid, 'history': history, 'user_id': user_id})
    except Exception as e:
        print(e)
        pass
    try:
        cid = str(request.POST['mytrade'])
        url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
        res = requests.post(url)
        history = res.json()

        if len(history) == 0:
            return redirect('mypage3')
        else:
            history.reverse()
            return render(request, 'app/search3.html', {'cid': cid, 'history': history, 'user_id': user_id})
    except Exception as e:
        print(e)
        pass
        try:
            cid = str(request.POST['complete'])
            url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
            res = requests.post(url)
            history = res.json()

            if len(history) == 0:
                return redirect('mypage3')
            else:
                history.reverse()
                return render(request, 'app/search1.html', {'cid': cid, 'history': history, 'user_id': user_id})
        except Exception as e:
            print(e)
            return redirect('index3')


def search4(request):
    user_id = request.session['user_id']
    try:
        cid = str(request.POST['cid'])
        url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
        res = requests.post(url)
        history = res.json()

        if len(history) == 0:
            return redirect('index4')
        else:
            history.reverse()
            return render(request, 'app/search4.html', {'cid': cid, 'history': history, 'user_id': user_id})
    except Exception as e:
        print(e)
        pass
    try:
        cid = str(request.POST['mytrade'])
        url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
        res = requests.post(url)
        history = res.json()

        if len(history) == 0:
            return redirect('mypage4')
        else:
            history.reverse()
            return render(request, 'app/search4.html', {'cid': cid, 'history': history, 'user_id': user_id})
    except Exception as e:
        print(e)
        pass
        try:
            cid = str(request.POST['complete'])
            url = ("http://222.239.231.247:8001/keyHistory/%s" % cid)
            res = requests.post(url)
            history = res.json()

            if len(history) == 0:
                return redirect('mypage4')
            else:
                history.reverse()
                return render(request, 'app/search1.html', {'cid': cid, 'history': history, 'user_id': user_id})
        except Exception as e:
            print(e)
            return redirect('inde4')


def share1(request):
    try:
        otp = request.POST['otp']
        check_id = request.POST['check_id']
        share_user = request.POST['share_user']
        user_id = request.session['user_id']
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
            if otp == nowotp and Member.objects.get(user_id=share_user, user_role='3'):
                share = Contract_LCR.objects.get(id=check_id)
                if share.share3 == '':
                    share.share3 = share_user
                    share.status = "new"
                    share.save()
                    result_dict['result'] = 'Success'
                    return JsonResponse(result_dict)
                else:
                    result_dict['result'] = 'Already sent'
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
        return redirect('ing')


def share2_1(request):
    try:
        otp = request.POST['otp']
        check_id = request.POST['check_id']
        share_user = request.POST['share_user']
        user_id = request.session['user_id']
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
            if otp == nowotp and Member.objects.get(user_id=share_user, user_role='1'):
                share = Contract_OS.objects.get(id=check_id)
                if share.share1 == '':
                    share.share1 = share_user
                    share.status = "new"
                    share.save()
                    result_dict['result'] = 'Success'
                    return JsonResponse(result_dict)
                else:
                    result_dict['result'] = 'Already sent'
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
        return redirect('ing2_1')


def share2_2(request):
    try:
        otp = request.POST['otp']
        check_id = request.POST['check_id']
        share_user = request.POST['share_user']
        user_id = request.session['user_id']
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
            if otp == nowotp and Member.objects.get(user_id=share_user, user_role='4'):
                share = Contract_SR.objects.get(id=check_id)
                if share.share4 == '':
                    share.share4 = share_user
                    share.status = "new"
                    share.save()
                    result_dict['result'] = 'Success'
                    return JsonResponse(result_dict)
                else:
                    result_dict['result'] = 'Already sent'
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
        return redirect('ing2_2')


def share2_3(request):
    try:
        otp = request.POST['otp']
        check_id = request.POST['check_id']
        share_user = request.POST['share_user']
        user_id = request.session['user_id']
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
            if otp == nowotp and Member.objects.get(user_id=share_user, user_role='1'):
                share = Contract_CI.objects.get(id=check_id)
                if share.share1 == '':
                    share.share1 = share_user
                    share.status = "new"
                    share.save()
                    result_dict['result'] = 'Success'
                    return JsonResponse(result_dict)
                else:
                    result_dict['result'] = 'Already sent'
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
        return redirect('ing2_3')


def share3(request):
    try:
        otp = request.POST['otp']
        check_id = request.POST['check_id']
        share_user = request.POST['share_user']
        share_user2 = request.POST['share_user2']
        user_id = request.session['user_id']
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
            if otp == nowotp and Member.objects.get(user_id=share_user, user_role='1') and Member.objects.get(user_id=share_user2, user_role='2'):
                share = Contract_LC.objects.get(id=check_id)
                if share.share1 == '' and share.share2 == '':
                    share.share1 = share_user
                    share.share2 = share_user2
                    share.status = "new"
                    share.save()
                    result_dict['result'] = 'Success'
                    return JsonResponse(result_dict)
                else:
                    result_dict['result'] = 'Already sent'
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
        return redirect('ing3')


def share4_1(request):
    try:
        otp = request.POST['otp']
        check_id = request.POST['check_id']
        share_user = request.POST['share_user']
        user_id = request.session['user_id']
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
            if otp == nowotp and Member.objects.get(user_id=share_user, user_role='2'):
                share = Contract_BL.objects.get(id=check_id)
                if share.share1 == '' and share.share2 == '':
                    share.share2 = share_user
                    share.status2 = "new"
                    share.save()
                    result_dict['result'] = 'Success'
                    return JsonResponse(result_dict)
                else:
                    result_dict['result'] = 'Already sent'
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
        return redirect('ing4_1')


def share4_2(request):
    try:
        otp = request.POST['otp']
        check_id = request.POST['check_id']
        share_user = request.POST['share_user']
        user_id = request.session['user_id']
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
            if otp == nowotp and Member.objects.get(user_id=share_user, user_role='1'):
                share = Contract_DO.objects.get(id=check_id)
                if share.share1 == '' and share.share3 == '':
                    share.share1 = share_user
                    share.status = "new"
                    share.save()
                    result_dict['result'] = 'Success'
                    return JsonResponse(result_dict)
                else:
                    result_dict['result'] = 'Already sent'
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
        return redirect('ing4_2')


@csrf_exempt
def remove(request):
    check_id = request.POST['check_ids']
    check_ids = check_id.split(',')
    result_dict = {}
    try:
        for check_id in check_ids:
            if Contract_LCR.objects.get(id=check_id).share3 == '':
                Contract_LCR.objects.get(id=check_id).delete()
                result_dict['result'] = 'deleted'
            else:
                result_dict['result'] = 'Could not delete'
        return JsonResponse(result_dict)
    except Exception as e:
        print(e)
        return redirect('ing')


@csrf_exempt
def remove2_1(request):
    check_id = request.POST['check_ids']
    check_ids = check_id.split(',')
    result_dict = {}
    try:
        for check_id in check_ids:
            if Contract_OS.objects.get(id=check_id).share1 == '':
                Contract_OS.objects.get(id=int(check_id)).delete()
                result_dict['result'] = 'deleted'
            else:
                result_dict['result'] = 'Could not delete'
        return JsonResponse(result_dict)
    except Exception as e:
        print(e)
        return redirect('ing2_1')


@csrf_exempt
def remove2_2(request):
    check_id = request.POST['check_ids']
    check_ids = check_id.split(',')
    result_dict = {}
    try:
        for check_id in check_ids:
            if Contract_SR.objects.get(id=check_id).share4 == '':
                Contract_SR.objects.get(id=check_id).delete()
                result_dict['result'] = 'deleted'
            else:
                result_dict['result'] = 'Could not delete'
        return JsonResponse(result_dict)
    except Exception as e:
        print(e)
        return redirect('ing2_2')


@csrf_exempt
def remove2_3(request):
    check_id = request.POST['check_ids']
    check_ids = check_id.split(',')
    result_dict = {}
    try:
        for check_id in check_ids:
            if Contract_CI.objects.get(id=check_id).share1 == '':
                Contract_CI.objects.get(id=check_id).delete()
                result_dict['result'] = 'deleted'
            else:
                result_dict['result'] = 'Could not delete'
        return JsonResponse(result_dict)

    except Exception as e:
        print(e)
        return redirect('ing2_3')


@csrf_exempt
def remove3(request):
    check_id = request.POST['check_ids']
    check_ids = check_id.split(',')
    result_dict = {}
    try:
        for check_id in check_ids:
            if Contract_LC.objects.get(id=check_id).share1 == '' and Contract_LC.objects.get(id=check_id).share2 == '':
                Contract_LC.objects.get(id=check_id).delete()
                result_dict['result'] = 'deleted'
            else:
                result_dict['result'] = 'Could not delete'
        return JsonResponse(result_dict)

    except Exception as e:
        print(e)
        return redirect('ing3')


@csrf_exempt
def remove4_1(request):
    check_id = request.POST['check_ids']
    check_ids = check_id.split(',')
    result_dict = {}
    try:
        for check_id in check_ids:
            if Contract_BL.objects.get(id=check_id).share1 == '' and Contract_BL.objects.get(
                    id=check_id).share2 == '' and Contract_BL.objects.get(id=check_id).share3 == '':
                Contract_BL.objects.get(id=check_id).delete()
                result_dict['result'] = 'deleted'
            else:
                result_dict['result'] = 'Could not delete'
        return JsonResponse(result_dict)

    except Exception as e:
        print(e)
        return redirect('ing4_1')


@csrf_exempt
def remove4_2(request):
    check_id = request.POST['check_ids']
    check_ids = check_id.split(',')
    result_dict = {}
    try:
        for check_id in check_ids:
            if Contract_DO.objects.get(id=check_id).share1 == '':
                Contract_DO.objects.get(id=check_id).delete()
                result_dict['result'] = 'deleted'
            else:
                result_dict['result'] = 'Could not delete'
        return JsonResponse(result_dict)

    except Exception as e:
        print(e)
        return redirect('ing4_2')


def osremove(request):
    # deletes all objects from Car database table
    # Contract.objects.get('id').delete()
    check_id = request.GET['check_id']
    check_ids = check_id.split(',')

    for id in check_ids:
        try:
            share = Contract_OS.objects.get(id=id)
            share.share1 = ' '
            share.save()
        except:
            pass
    return redirect('osreceived')


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


def blremove3(request):
    # deletes all objects from Car database table
    # Contract.objects.get('id').delete()
    check_id = request.GET['check_id']
    check_ids = check_id.split(',')

    for id in check_ids:
        try:
            share = Contract_BL.objects.get(id=id)
            share.share3 = ' '
            share.save()
        except:
            pass
    return redirect('blreceived3')


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
    return redirect('osreceived')


def submit(request):
    result_dict = {}
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


        package = Contract_OS.objects.filter(id=contract_id)

        item1 = package.values('item1')[0]['item1']
        description1 = package.values('description1')[0]['description1']
        quantity1 = package.values('quantity1')[0]['quantity1']
        price1 = package.values('price1')[0]['price1']
        amount1 = package.values('amount1')[0]['amount1']

        item2 = package.values('item2')[0]['item2']
        description2 = package.values('description2')[0]['description2']
        quantity2 = package.values('quantity2')[0]['quantity2']
        price2= package.values('price2')[0]['price2']
        amount2 = package.values('amount2')[0]['amount2']

        item3 = package.values('item3')[0]['item3']
        description3 = package.values('description3')[0]['description3']
        quantity3 = package.values('quantity3')[0]['quantity3']
        price3 = package.values('price3')[0]['price3']
        amount3 = package.values('amount3')[0]['amount3']

        item4 = package.values('item4')[0]['item4']
        description4 = package.values('description4')[0]['description4']
        quantity4 = package.values('quantity4')[0]['quantity4']
        price4 = package.values('price4')[0]['price4']
        amount4 = package.values('amount4')[0]['amount4']

        item5 = package.values('item5')[0]['item5']
        description5 = package.values('description5')[0]['description5']
        quantity5 = package.values('quantity5')[0]['quantity5']
        price5 = package.values('price5')[0]['price5']
        amount5 = package.values('amount5')[0]['amount5']

        # beneficiary = Member.objects.filter(user_id=c)
        # applicant = Member.objects.filter(user_id=d)
        # beneficiary_name = beneficiary.values('user_name')[0]['user_name']
        # beneficiary_address = beneficiary.values('address')[0]['address']
        # applicant_name = applicant.values('user_name')[0]['user_name']
        # applicant_address = applicant.values('address')[0]['address']
        # beneficiary_info = beneficiary_name + '\n' + beneficiary_address
        # applicant_info = applicant_name + '\n' + applicant_address


        time_format = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
        if len(Contract_LCR.objects.filter(contract_id=contract_id)) == 0:
            try:
                pdf = FPDF(unit='in', format='A4')
                pdf.add_page()
                pdf.set_font('Arial', '', 10.0)
                epw = pdf.w - 2 * pdf.l_margin
                records = [['1.Advising bank:', '2.Type:'],
                           ['>  '+a, '>  '+b],
                           ['3.Beneficiary:', '4.Applicant:'],
                           ['>  '+c, '>  '+d],
                           ['5.L/C Amount and Tolerance:', '6.Latest shipment date:'],
                           ['>  '+e, '>  '+k],
                           ['7.Partial shipment:', '8.Transshipment:'],
                           ['>  '+f, '>  '+g],
                           ['9.Loading(shipment from):', '10.Discharging(shipment to):'],
                           ['>  '+i, '>  '+j]]

                pdf.ln(0.5)
                pdf.set_font('Arial', 'BU', 16.0)
                pdf.cell(epw, 0.0, 'APPLICATION FOR IRREVOCABLE DOCUMENTRAY CREADIT', align='C')
                pdf.ln(0.25)
                pdf.set_font('Arial', 'B', 14.0)
                pdf.cell(epw, 0.0, 'Contract ID:' + contract_id + '/' + time_format, align='C')
                pdf.ln(0.25)
                pdf.set_font('Arial', '', 12.0)
                pdf.ln(0.5)

                th = pdf.font_size
                for row in records:
                    pdf.cell(epw/2, 2 * th, str(row[0]), border=1)
                    pdf.cell(epw/2, 2 * th, str(row[1]), border=1)
                    pdf.ln(2 * th)
                pdf.cell(epw, 2 * th, 'Trnasport mode : ' + h, border=1)
                pdf.ln(2 * th)
                tables = [['Item No.', 'Description', 'Quantity', 'Unit Price', 'Amount'],
                          [item1, description1, quantity1, price1, amount1],
                          [item2, description2, quantity2, price2, amount2],
                          [item3, description3, quantity3, price3, amount3],
                          [item4, description4, quantity4, price4, amount4],
                          [item5, description5, quantity5, price5, amount5]]
                pdf.set_font('Arial', '', 12.0)
                pdf.cell(epw, 0.5, 'Description of Goods and/or Services', align='C')
                pdf.ln(0.5)
                for row in tables:
                    pdf.cell(epw/7, 2 * th, str(row[0]), border=1, align='C')
                    pdf.cell(3*epw/7, 2 * th, str(row[1]), border=1, align='C')
                    pdf.cell(epw/7, 2 * th, str(row[2]), border=1, align='C')
                    pdf.cell(epw/7, 2 * th, str(row[3]), border=1, align='C')
                    pdf.cell(epw/7, 2 * th, str(row[4]), border=1, align='C')
                    pdf.ln(2 * th)
                pdf.ln(0.5)
                pdf.cell(epw, 2 * th, ' All banking charges : ' + l, border=1)
                pdf.ln(2 * th)
                pdf.cell(epw, 2 * th, ' Confirmation : ' + m, border=1)
                pdf.ln(2 * th)
                pdf.cell(epw, 2 * th, ' T/T reimbursement : ' + n, border=1)
                pdf.ln(0.5)
                pdf.cell(epw, 2 * th,  ' Request By : ' + user_id, border=0, align='R')
                pdf.ln(2 * th)


                pdf.output('document/LCR_' + time_format + '.pdf', 'F')
                file = open('document/LCR_' + time_format + '.pdf', 'rb')
                data = file.read()

                hash = hashlib.sha256(data).hexdigest()
                file.close()

                # 데이터 저장
                contract = Contract_LCR(contractname=contractname, contract_id=contract_id, sha256=hash, status='new',
                                        filename='document/LCR_' + time_format + '.pdf', advisingbank=a, applicant=c, beneficiary=d, amount=e, particalshipment=f, transshipment=g, loding=i)

                # 로그인한 사용자 정보를 Contract에 같이 저장
                user_id = request.session['user_id']
                member = Member.objects.get(user_id=user_id)
                contract.owner = member
                contract.save()
                result_dict['result'] = "작성완료"
                return JsonResponse(result_dict)
            except Exception as e:
                print(e)
                result_dict['result'] = "영어로 작성해주세요."
                return JsonResponse(result_dict)
        else:
            result_dict['result'] = "해당 contract id 는 사용할 수 없습니다."
            return JsonResponse(result_dict)
    except Exception as e:
        print(e)
        result_dict['result'] = "양식을 완성해주세요."
        return JsonResponse(result_dict)


def submit2_1(request):
    result_dict = {}
    try:
        user_id = request.session['user_id']
        contractname = request.POST['contractname']

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

        j2 = request.POST['j2']
        k2 = request.POST['k2']
        l2 = request.POST['l2']
        m2 = request.POST['m2']
        n2 = request.POST['n2']
        o2 = request.POST['o2']

        j3 = request.POST['j3']
        k3 = request.POST['k3']
        l3 = request.POST['l3']
        m3 = request.POST['m3']
        n3 = request.POST['n3']
        o3 = request.POST['o3']

        j4 = request.POST['j4']
        k4 = request.POST['k4']
        l4 = request.POST['l4']
        m4 = request.POST['m4']
        n4 = request.POST['n4']
        o4 = request.POST['o4']

        j5 = request.POST['j5']
        k5 = request.POST['k5']
        l5 = request.POST['l5']
        m5 = request.POST['m5']
        n5 = request.POST['n5']
        o5 = request.POST['o5']

        time_format = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
        try:
            pdf = FPDF(unit='in', format='A4')
            pdf.add_page()

            pdf.set_font('Arial', '', 10.0)
            epw = pdf.w - 2 * pdf.l_margin

            pdf.ln(0.75)
            pdf.set_font('Arial', 'BU', 16.0)
            pdf.cell(epw, 0.0, 'OFFER SHEET', align='C')
            pdf.ln(0.25)
            pdf.set_font('Arial', 'B', 14.0)
            pdf.cell(epw, 0.0, time_format, align='C')
            pdf.ln(0.25)
            pdf.set_font('Arial', '', 12.0)
            pdf.ln(0.5)
            pdf.cell(epw, 0.0, 'We are pleased to offer under-mentioned article(s) as per conditions and details described as follows', align='L')
            pdf.ln(0.25)
            th = pdf.font_size
            records = [['Item No.', 'Description', 'Unit', 'Quantity', 'Unit Price', 'Amount'],
                       [j, k, l, m, n, o],
                       [j2, k2, l2, m2, n2, o2],
                       [j3, k3, l3, m3, n3, o3],
                       [j4, k4, l4, m4, n4, o4],
                       [j5, k5, l5, m5, n5, o5]]

            for row in records:
                pdf.cell(1, 2 * th, str(row[0]), border=1, align='C')
                pdf.cell(2.5, 2 * th, str(row[1]), border=1, align='C')
                pdf.cell(1, 2 * th, str(row[2]), border=1, align='C')
                pdf.cell(1, 2 * th, str(row[3]), border=1, align='C')
                pdf.cell(1, 2 * th, str(row[4]), border=1, align='C')
                pdf.cell(1, 2 * th, str(row[5]), border=1, align='C')
                pdf.ln(2 * th)
            pdf.ln(0.5)
            bottom_content = [['Origin', ':', a],
                              ['Packing', ':', b],
                              ['Shipment', ':', c],
                              ['Shipping Port', ':', d],
                              ['Inspection', ':', e],
                              ['Destination', ':', f],
                              ['Payment', ':', g],
                              ['Validity', ':', h],
                              ['Remarks', ':', i]]

            for b in bottom_content:
                pdf.cell(1, 2 * th, str(b[0]), align='L')
                pdf.cell(1, 2 * th, str(b[1]), align='C')
                pdf.cell(5.5, 2 * th, str(b[2]), align='L')
                pdf.ln(2 * th)
            pdf.ln(1)
            pdf.cell(epw, 0.0, 'Looking forward to your valued order for the above offer, we are' , align='R')
            pdf.ln(0.5)
            pdf.cell(epw, 0.0, 'yours faithfully', align='R')
            pdf.ln(0.5)
            pdf.cell(epw, 0.0, user_id, align='R')
            pdf.ln(0.5)

            pdf.output('document/OS_' + time_format + '.pdf', 'F')
            file = open('document/OS_' + time_format + '.pdf', 'rb')
            data = file.read()

            hash = hashlib.sha256(data).hexdigest()
            file.close()

            # 데이터 저장
            contract = Contract_OS(contractname=contractname, sha256=hash, status='new',
                                   filename='document/OS_' + time_format + '.pdf',
                                   item1=j, item2=j2, item3=j3, item4=j4, item5=j5,
                                   description1=k, description2=k2, description3=k3, description4=k4, description5=k5,
                                   quantity1=m, quantity2=m2, quantity3=m3, quantity4=m4, quantity5=m5,
                                   price1=n, price2=n2, price3=n3, price4=n4, price5=n5,
                                   amount1=o, amount2=o2, amount3=o3, amount4=o4, amount5=o5)

            # 로그인한 사용자 정보를 Contract에 같이 저장
            user_id = request.session['user_id']
            member = Member.objects.get(user_id=user_id)
            contract.owner = member
            contract.save()
            result_dict['result'] = "작성완료"
            return JsonResponse(result_dict)
        except Exception as e:
            result_dict['result'] = "영어로 작성해주세요."
            return JsonResponse(result_dict)
    except Exception as e:
        print(e)
        result_dict['result'] = "양식을 완성해주세요."
        return JsonResponse(result_dict)


def submit2_2(request):
    result_dict = {}
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

        package = Contract_OS.objects.filter(id=contract_id)

        item1 = package.values('item1')[0]['item1']
        description1 = package.values('description1')[0]['description1']
        quantity1 = package.values('quantity1')[0]['quantity1']
        price1 = package.values('price1')[0]['price1']
        amount1 = package.values('amount1')[0]['amount1']

        item2 = package.values('item2')[0]['item2']
        description2 = package.values('description2')[0]['description2']
        quantity2 = package.values('quantity2')[0]['quantity2']
        price2 = package.values('price2')[0]['price2']
        amount2 = package.values('amount2')[0]['amount2']

        item3 = package.values('item3')[0]['item3']
        description3 = package.values('description3')[0]['description3']
        quantity3 = package.values('quantity3')[0]['quantity3']
        price3 = package.values('price3')[0]['price3']
        amount3 = package.values('amount3')[0]['amount3']

        item4 = package.values('item4')[0]['item4']
        description4 = package.values('description4')[0]['description4']
        quantity4 = package.values('quantity4')[0]['quantity4']
        price4 = package.values('price4')[0]['price4']
        amount4 = package.values('amount4')[0]['amount4']

        item5 = package.values('item5')[0]['item5']
        description5 = package.values('description5')[0]['description5']
        quantity5 = package.values('quantity5')[0]['quantity5']
        price5 = package.values('price5')[0]['price5']
        amount5 = package.values('amount5')[0]['amount5']

        exporter = user_id
        importer = package.values('share1')[0]['share1']
        time_format = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
        if len(Contract_SR.objects.filter(contract_id=contract_id)) == 0:
            try:
                pdf = FPDF(unit='in', format='A4')
                pdf.add_page()
                pdf.set_font('Arial', '', 10.0)
                epw = pdf.w - 2 * pdf.l_margin
                records = [['1.Exporter:', '2.Importer:'],
                           ['>  '+exporter, '>  '+importer],
                           ['3.Consignee:', '4.Notify Party:'],
                           ['>  '+a, '>  '+b],
                           ['5.Departure Date.:', '6.Type:'],
                           ['>  '+c, '>  '+e],
                           ['7.Loading Port:', '8.Discharging Port:'],
                           ['>  '+d, '>  '+h],
                           ['9.Terms of Delivery:', '10.Terms of Payment:'],
                           ['>  '+f, '>  '+g],
                           ['11.Cargo Type:', '12.Pick up Date of Cargo:'],
                           ['>  '+i, '>  '+j]]

                pdf.ln(0.75)
                pdf.set_font('Arial', 'BU', 16.0)
                pdf.cell(epw, 0.0, 'SHIPPING REQUEST', align='C')
                pdf.ln(0.25)
                pdf.set_font('Arial', 'B', 14.0)
                pdf.cell(epw, 0.0, 'Contract ID:' + contract_id + '/' + time_format, align='C')
                pdf.ln(0.5)
                pdf.set_font('Arial', '', 12.0)

                th = pdf.font_size
                for row in records:
                    pdf.cell(epw/2, 2.5 * th, str(row[0]), border=1)
                    pdf.cell(epw/2, 2.5 * th, str(row[1]), border=1)
                    pdf.ln(2.5 * th)

                tables = [['Item No.', 'Description', 'Quantity', 'Unit Price', 'Amount'],
                          [item1, description1, quantity1, price1, amount1],
                          [item2, description2, quantity2, price2, amount2],
                          [item3, description3, quantity3, price3, amount3],
                          [item4, description4, quantity4, price4, amount4],
                          [item5, description5, quantity5, price5, amount5]]
                pdf.set_font('Arial', '', 12.0)
                pdf.cell(epw, 0.5, 'Description of Goods and/or Services', align='C')
                pdf.ln(0.5)
                for row in tables:
                    pdf.cell(epw / 7, 2.5 * th, str(row[0]), border=1, align='C')
                    pdf.cell(3 * epw / 7, 2.5 * th, str(row[1]), border=1, align='C')
                    pdf.cell(epw / 7, 2.5 * th, str(row[2]), border=1, align='C')
                    pdf.cell(epw / 7, 2.5 * th, str(row[3]), border=1, align='C')
                    pdf.cell(epw / 7, 2.5 * th, str(row[4]), border=1, align='C')
                    pdf.ln(2.5 * th)
                pdf.cell(epw, 0.5, ' Request By:' + user_id, align='R')
                pdf.ln(0.5)
                pdf.output('document/SR_' + time_format + '.pdf', 'F')
                file = open('document/SR_' + time_format + '.pdf', 'rb')
                data = file.read()

                hash = hashlib.sha256(data).hexdigest()
                file.close()

                # 데이터 저장
                contract = Contract_SR(contractname=srname, contract_id=contract_id, sha256=hash, status='new', lport=d , dport=h, notify=b, consignee=a,
                                       filename='document/SR_' + time_format + '.pdf')

                # 로그인한 사용자 정보를 Contract에 같이 저장
                user_id = request.session['user_id']
                member = Member.objects.get(user_id=user_id)
                contract.owner = member
                contract.save()
                result_dict['result'] = "작성완료"
                return JsonResponse(result_dict)
            except Exception as e:
                print(e)
                result_dict['result'] = "영어로 작성해주세요."
                return JsonResponse(result_dict)
        else:
            result_dict['result'] = "해당 contract id 는 사용할 수 없습니다."
            return JsonResponse(result_dict)
    except Exception as e:
        print(e)
        result_dict['result'] = "양식을 완성해주세요."
        return JsonResponse(result_dict)


def submit2_3(request):
    result_dict = {}
    try:
        user_id = request.session['user_id']
        contractname = request.POST['contractname']
        contract_id = request.POST['contract_id']
        a = request.POST['a']
        b = request.POST['b']

        package = Contract_OS.objects.filter(id=contract_id)
        importer = package.values('share1')[0]['share1']
        item1 = package.values('item1')[0]['item1']
        description1 = package.values('description1')[0]['description1']
        quantity1 = package.values('quantity1')[0]['quantity1']
        price1 = package.values('price1')[0]['price1']
        amount1 = package.values('amount1')[0]['amount1']

        item2 = package.values('item2')[0]['item2']
        description2 = package.values('description2')[0]['description2']
        quantity2 = package.values('quantity2')[0]['quantity2']
        price2 = package.values('price2')[0]['price2']
        amount2 = package.values('amount2')[0]['amount2']

        item3 = package.values('item3')[0]['item3']
        description3 = package.values('description3')[0]['description3']
        quantity3 = package.values('quantity3')[0]['quantity3']
        price3 = package.values('price3')[0]['price3']
        amount3 = package.values('amount3')[0]['amount3']

        item4 = package.values('item4')[0]['item4']
        description4 = package.values('description4')[0]['description4']
        quantity4 = package.values('quantity4')[0]['quantity4']
        price4 = package.values('price4')[0]['price4']
        amount4 = package.values('amount4')[0]['amount4']

        item5 = package.values('item5')[0]['item5']
        description5 = package.values('description5')[0]['description5']
        quantity5 = package.values('quantity5')[0]['quantity5']
        price5 = package.values('price5')[0]['price5']
        amount5 = package.values('amount5')[0]['amount5']

        sr = Contract_SR.objects.filter(contract_id=contract_id)
        consignee = sr.values('consignee')[0]['consignee']
        notify = sr.values('notify')[0]['notify']
        lport = sr.values('lport')[0]['lport']

        bl = Contract_BL.objects.filter(contract_id=contract_id)
        finaldestination = bl.values('finaldestination')[0]['finaldestination']
        vessel = bl.values('vessel')[0]['vessel']
        shipper = bl.values('owner_id')[0]['owner_id']



        time_format = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
        if len(Contract_CI.objects.filter(contract_id=contract_id)) == 0:
            try:
                pdf = FPDF(unit='in', format='A4')
                pdf.add_page()
                pdf.set_font('Arial', '', 10.0)
                epw = pdf.w - 2 * pdf.l_margin


                pdf.set_font('Arial', 'B', 14.0)
                pdf.cell(epw, 0.0, 'Contract ID:' + contract_id + '/' + time_format, align='C')
                pdf.ln(0.25)
                pdf.set_font('Arial', '', 12.0)
                pdf.cell(epw, 0.0, contractname + ' From:' + user_id, align='C')
                pdf.set_font('Arial', '', 10.0)
                pdf.ln(0.5)
                th = pdf.font_size
                records = [['1.Shipper:', '2.Exporter:'],
                           [shipper, user_id],
                           ['3.Importer:', '4.Consignee:'],
                           [importer, consignee],
                           ['5.Notify Party:', '6.Remarks:'],
                           [notify, a],
                           ['7.Loading Port:', '8.Final Destination:'],
                           [lport, finaldestination],
                           ['9.Vessel:', '10.Sailng On:'],
                           [vessel, b]]

                pdf.ln(0.5)
                pdf.set_font('Arial', 'BU', 16.0)
                pdf.cell(epw, 0.0, 'COMMERCIAL INVOICE', align='C')
                pdf.ln(0.25)
                pdf.set_font('Arial', 'B', 14.0)
                pdf.cell(epw, 0.0, 'Contract ID:' + contract_id + '/' + time_format, align='C')
                pdf.ln(0.25)
                pdf.set_font('Arial', '', 12.0)
                pdf.ln(0.5)
                for row in records:
                    pdf.cell(3.5, 2.5 * th, str(row[0]), border=1)
                    pdf.cell(3.5, 2.5 * th, str(row[1]), border=1)
                    pdf.ln(2.5 * th)
                tables = [['Item No.', 'Description', 'Quantity', 'Unit Price', 'Amount'],
                          [item1, description1, quantity1, price1, amount1],
                          [item2, description2, quantity2, price2, amount2],
                          [item3, description3, quantity3, price3, amount3],
                          [item4, description4, quantity4, price4, amount4],
                          [item5, description5, quantity5, price5, amount5]]
                pdf.set_font('Arial', '', 12.0)
                pdf.cell(epw, 0.5, 'Description of Goods and/or Services', align='C')
                pdf.ln(0.5)
                for row in tables:
                    pdf.cell(epw / 7, 2.5 * th, str(row[0]), border=1, align='C')
                    pdf.cell(3 * epw / 7, 2.5 * th, str(row[1]), border=1, align='C')
                    pdf.cell(epw / 7, 2.5 * th, str(row[2]), border=1, align='C')
                    pdf.cell(epw / 7, 2.5 * th, str(row[3]), border=1, align='C')
                    pdf.cell(epw / 7, 2.5 * th, str(row[4]), border=1, align='C')
                    pdf.ln(2.5 * th)
                pdf.cell(epw, 0.5, ' Signed By:' + user_id, align='R')
                pdf.ln(0.5)
                pdf.output('document/CI_' + time_format + '.pdf', 'F')
                file = open('document/CI_' + time_format + '.pdf', 'rb')
                data = file.read()

                hash = hashlib.sha256(data).hexdigest()
                file.close()

                # 데이터 저장
                contract = Contract_CI(contractname=contractname, contract_id=contract_id, sha256=hash, status='new',
                                       filename='document/CI_' + time_format + '.pdf')

                # 로그인한 사용자 정보를 Contract에 같이 저장
                user_id = request.session['user_id']
                member = Member.objects.get(user_id=user_id)
                contract.owner = member
                contract.save()
                result_dict['result'] = "작성완료"
                return JsonResponse(result_dict)
            except Exception as e:
                result_dict['result'] = "영어로 작성해주세요."
                return JsonResponse(result_dict)
        else:
            result_dict['result'] = "해당 contract id 는 사용할 수 없습니다."
            return JsonResponse(result_dict)
    except Exception as e:
        print(e)
        result_dict['result'] = "양식을 완성해주세요."
        return JsonResponse(result_dict)


def submit3(request):
    result_dict = {}
    try:
        user_id = request.session['user_id']
        letteroflc = request.POST['letteroflc']
        contract_id = request.POST['contract_id']
        a = request.POST['a']
        b = request.POST['b']
        c = request.POST['c']
        d = request.POST['d']

        lcr = Contract_LCR.objects.filter(contract_id=contract_id)
        e = lcr.values('advisingbank')[0]['advisingbank']
        f = lcr.values('applicant')[0]['applicant']
        g = lcr.values('beneficiary')[0]['beneficiary']
        h = lcr.values('amount')[0]['amount']
        i = lcr.values('particalshipment')[0]['particalshipment']
        j = lcr.values('transshipment')[0]['transshipment']
        k = lcr.values('loding')[0]['loding']

        package = Contract_OS.objects.filter(id=contract_id)

        item1 = package.values('item1')[0]['item1']
        description1 = package.values('description1')[0]['description1']
        quantity1 = package.values('quantity1')[0]['quantity1']
        price1 = package.values('price1')[0]['price1']
        amount1 = package.values('amount1')[0]['amount1']

        item2 = package.values('item2')[0]['item2']
        description2 = package.values('description2')[0]['description2']
        quantity2 = package.values('quantity2')[0]['quantity2']
        price2 = package.values('price2')[0]['price2']
        amount2 = package.values('amount2')[0]['amount2']

        item3 = package.values('item3')[0]['item3']
        description3 = package.values('description3')[0]['description3']
        quantity3 = package.values('quantity3')[0]['quantity3']
        price3 = package.values('price3')[0]['price3']
        amount3 = package.values('amount3')[0]['amount3']

        item4 = package.values('item4')[0]['item4']
        description4 = package.values('description4')[0]['description4']
        quantity4 = package.values('quantity4')[0]['quantity4']
        price4 = package.values('price4')[0]['price4']
        amount4 = package.values('amount4')[0]['amount4']

        item5 = package.values('item5')[0]['item5']
        description5 = package.values('description5')[0]['description5']
        quantity5 = package.values('quantity5')[0]['quantity5']
        price5 = package.values('price5')[0]['price5']
        amount5 = package.values('amount5')[0]['amount5']

        time_format = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
        if len(Contract_LC.objects.filter(contract_id=contract_id)) == 0:
            try:
                pdf = FPDF(unit='in', format='A4')
                pdf.add_page()
                pdf.set_font('Arial', '', 10.0)
                epw = pdf.w - 2 * pdf.l_margin
                records = [['1.Advising bank:', '2.Credit No.:'],
                           ['>  '+e, '>  '+a],
                           ['3.Date of Issue:', '4.Expiry Date:'],
                           ['>  '+b, '>  '+c],
                           ['5.Applicant:', '6.Beneficiary:'],
                           ['>  '+f, '>  '+g],
                           ['7.Amount of Credit:', '8.Loding on board:'],
                           ['>  '+h, '>  '+k],
                           ['9.Partial Shipments:', '10.Transshipment:'],
                           ['>  '+i, '>  '+j]]

                pdf.ln(0.5)
                pdf.set_font('Arial', 'BU', 16.0)
                pdf.cell(epw, 0.0, 'LETTER OF CREDIT', align='C')
                pdf.ln(0.25)
                pdf.set_font('Arial', 'B', 14.0)
                pdf.cell(epw, 0.0, 'Contract ID:' + contract_id + '/' + time_format, align='C')
                pdf.ln(0.25)
                pdf.set_font('Arial', '', 12.0)
                pdf.ln(0.5)

                th = pdf.font_size
                for row in records:
                    pdf.cell(epw/2, 2.5 * th, str(row[0]), border=1)
                    pdf.cell(epw/2, 2.5 * th, str(row[1]), border=1)
                    pdf.ln(2.5 * th)
                pdf.cell(epw, 2.5 * th, 'Credit Available With :' + d, border=1)
                pdf.ln(2.5 * th)
                pdf.cell(epw, 2.5 * th, 'Covering details :' + d, border=1)
                pdf.ln(2.5 * th)
                pdf.cell(epw, 2.5 * th, 'Description of Goods and/or Services :', border=0, align='C')
                pdf.ln(2.5 * th)
                tables = [['Item No.', 'Description', 'Quantity', 'Unit Price', 'Amount'],
                          [item1, description1, quantity1, price1, amount1],
                          [item2, description2, quantity2, price2, amount2],
                          [item3, description3, quantity3, price3, amount3],
                          [item4, description4, quantity4, price4, amount4],
                          [item5, description5, quantity5, price5, amount5]]

                for row in tables:
                    pdf.cell(epw / 7, 2.5 * th, str(row[0]), border=1, align='C')
                    pdf.cell(3 * epw / 7, 2.5 * th, str(row[1]), border=1, align='C')
                    pdf.cell(epw / 7, 2.5 * th, str(row[2]), border=1, align='C')
                    pdf.cell(epw / 7, 2.5 * th, str(row[3]), border=1, align='C')
                    pdf.cell(epw / 7, 2.5 * th, str(row[4]), border=1, align='C')
                    pdf.ln(2.5 * th)
                pdf.cell(epw, 2.5 * th, ' Confirmed by : ' + user_id, border=0, align='R')
                pdf.ln(2.5 * th)
                pdf.output('document/LC_' + time_format + '.pdf', 'F')
                file = open('document/LC_' + time_format + '.pdf', 'rb')
                data = file.read()

                hash = hashlib.sha256(data).hexdigest()
                file.close()
                # 데이터 저장
                contract = Contract_LC(contractname=letteroflc, contract_id=contract_id, sha256=hash, status='new',
                                       filename='document/LC_' + time_format + '.pdf')

                # 로그인한 사용자 정보를 Contract에 같이 저장
                user_id = request.session['user_id']
                member = Member.objects.get(user_id=user_id)
                contract.owner = member
                contract.save()
                result_dict['result'] = "작성완료"
                return JsonResponse(result_dict)
            except Exception as e:
                print(e)
                result_dict['result'] = "영어로 작성해주세요."
                return JsonResponse(result_dict)
        else:
            result_dict['result'] = "해당 contract id 는 사용할 수 없습니다."
            return JsonResponse(result_dict)
    except Exception as e:
        print(e)
        result_dict['result'] = "양식을 완성해주세요."
        return JsonResponse(result_dict)


def submit4_1(request):
    result_dict = {}
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

        sr = Contract_SR.objects.filter(contract_id=contract_id)
        consignee = sr.values('consignee')[0]['consignee']
        notify = sr.values('notify')[0]['notify']
        lport = sr.values('lport')[0]['lport']
        dport = sr.values('dport')[0]['dport']
        time_format = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
        if len(Contract_BL.objects.filter(contract_id=contract_id)) == 0:
            try:
                pdf = FPDF(unit='in', format='A4')
                pdf.add_page()
                pdf.set_font('Arial', '', 10.0)
                epw = pdf.w - 2 * pdf.l_margin
                records = [
                           ['1.Shipper:', '2.Consignee:'],
                           ['>  '+user_id, '>  '+consignee],
                           ['3.Nodify party:', '4.Place of Receipt:'],
                           ['>  '+notify, '>  '+b],
                           ['5.Voyage No.:', '6.Loading Port:'],
                           ['>  '+a,'>  '+lport],
                           ['7.Discharging Port:', '8.Final Destination:'],
                           ['>  '+dport,'>  '+c]]

                pdf.ln(0.5)
                pdf.set_font('Arial', 'BU', 16.0)
                pdf.cell(epw, 0.0, 'BILLS OF LADING', align='C')
                pdf.ln(0.25)
                pdf.set_font('Arial', 'B', 14.0)
                pdf.cell(epw, 0.0, 'Contract ID:' + contract_id + '/' + time_format, align='C')
                pdf.set_font('Arial', '', 12.0)
                pdf.ln(0.5)

                th = pdf.font_size
                for row in records:
                    pdf.cell(epw/2, 3 * th, str(row[0]), border=1)
                    pdf.cell(epw/2, 3 * th, str(row[1]), border=1)
                    pdf.ln(3 * th)

                pdf.cell(epw / 2, 3 * th, '9.Seal No.', border=1)
                pdf.cell(epw / 2, 3 * th, '10.Kind of Packages', border=1)
                pdf.ln(3 * th)
                pdf.cell(epw / 2, 10 * th, '>  '+e, border=1)
                pdf.cell(epw / 2, 10 * th, '>  '+f, border=1)
                pdf.ln(10 * th)
                pdf.cell(epw / 3, 3 * th, '11.Description of goods:', border=1)
                pdf.cell(epw / 3, 3 * th, '12.Gross Weight:', border=1)
                pdf.cell(epw / 3, 3 * th, '13.Measurement:', border=1)
                pdf.ln(3 * th)
                pdf.cell(epw / 3, 10 * th, '>  '+d, border=1)
                pdf.cell(epw / 3, 10 * th, '>  '+g, border=1)
                pdf.cell(epw / 3, 10 * th, '>  '+h, border=1)
                pdf.ln(10 * th)
                pdf.cell(epw, 2.5 * th, ' Issued by : ' + user_id, border=0, align='R')
                pdf.ln(2.5 * th)

                pdf.output('document/BL_' + time_format + '.pdf', 'F')
                file = open('document/BL_' + time_format + '.pdf', 'rb')
                data = file.read()

                hash = hashlib.sha256(data).hexdigest()
                file.close()

                # 데이터 저장
                contract = Contract_BL(contractname=contractname, contract_id=contract_id, sha256=hash, status2='new', finaldestination=c,vessel=a,
                                       filename='document/BL_' + time_format + '.pdf')

                # 로그인한 사용자 정보를 Contract에 같이 저장
                user_id = request.session['user_id']
                member = Member.objects.get(user_id=user_id)
                contract.owner = member
                contract.save()
                result_dict['result'] = "작성완료"
                return JsonResponse(result_dict)
            except Exception as e:
                result_dict['result'] = "영어로 작성해주세요."
                return JsonResponse(result_dict)
        else:
            result_dict['result'] = "해당 contract id 는 사용할 수 없습니다."
            return JsonResponse(result_dict)
    except Exception as e:
        print(e)
        result_dict['result'] = "양식을 완성해주세요."
        return JsonResponse(result_dict)


def submit4_2(request):
    result_dict = {}
    try:
        user_id = request.session['user_id']
        contractname = request.POST['contractname']
        contract_id = request.POST['contract_id']
        a = request.POST['a']
        b = request.POST['b']
        c = request.POST['c']

        package = Contract_OS.objects.filter(id=contract_id)

        item1 = package.values('item1')[0]['item1']
        description1 = package.values('description1')[0]['description1']
        quantity1 = package.values('quantity1')[0]['quantity1']
        price1 = package.values('price1')[0]['price1']
        amount1 = package.values('amount1')[0]['amount1']

        item2 = package.values('item2')[0]['item2']
        description2 = package.values('description2')[0]['description2']
        quantity2 = package.values('quantity2')[0]['quantity2']
        price2 = package.values('price2')[0]['price2']
        amount2 = package.values('amount2')[0]['amount2']

        item3 = package.values('item3')[0]['item3']
        description3 = package.values('description3')[0]['description3']
        quantity3 = package.values('quantity3')[0]['quantity3']
        price3 = package.values('price3')[0]['price3']
        amount3 = package.values('amount3')[0]['amount3']

        item4 = package.values('item4')[0]['item4']
        description4 = package.values('description4')[0]['description4']
        quantity4 = package.values('quantity4')[0]['quantity4']
        price4 = package.values('price4')[0]['price4']
        amount4 = package.values('amount4')[0]['amount4']

        item5 = package.values('item5')[0]['item5']
        description5 = package.values('description5')[0]['description5']
        quantity5 = package.values('quantity5')[0]['quantity5']
        price5 = package.values('price5')[0]['price5']
        amount5 = package.values('amount5')[0]['amount5']
        importer = package.values('share1')[0]['share1']
        time_format = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
        if len(Contract_DO.objects.filter(contract_id=contract_id)) == 0:
            try:
                pdf = FPDF(unit='in', format='A4')
                pdf.add_page()
                pdf.set_font('Arial', '', 10.0)
                epw = pdf.w - 2 * pdf.l_margin
                pdf.ln(0.75)
                pdf.set_font('Arial', 'BU', 16.0)
                pdf.cell(epw, 0.0, 'DELIVERY ORDER', align='C')
                pdf.ln(0.25)
                pdf.set_font('Arial', 'B', 14.0)
                pdf.cell(epw, 0.0, 'Contract ID:' + contract_id + '/' + time_format, align='C')
                pdf.ln(0.25)
                pdf.set_font('Arial', '', 12.0)
                pdf.ln(0.5)
                th = pdf.font_size
                pdf.cell(epw, 3 * th, 'Delivery To : ' + importer, border=0, align='C')
                pdf.ln(3 * th)
                pdf.cell(epw, 3 * th, 'Delivery Address :' , border=0, align='C')
                pdf.ln(3 * th)
                pdf.cell(epw, 3 * th, 'Delivery Date : ' + a, border=0, align='C')
                pdf.ln(3 * th)
                pdf.cell(epw, 3 * th, 'Delivery Time :' + b, border=0, align='C')
                pdf.ln(3 * th)
                pdf.cell(epw, 2.5 * th, 'Description of Goods and/or Services :', border=0, align='C')
                pdf.ln(2.5 * th)
                tables = [['Item No.', 'Description', 'Quantity', 'Unit Price', 'Amount'],
                          [item1, description1, quantity1, price1, amount1],
                          [item2, description2, quantity2, price2, amount2],
                          [item3, description3, quantity3, price3, amount3],
                          [item4, description4, quantity4, price4, amount4],
                          [item5, description5, quantity5, price5, amount5]]

                for row in tables:
                    pdf.cell(epw / 7, 2.5 * th, str(row[0]), border=1, align='C')
                    pdf.cell(3 * epw / 7, 2.5 * th, str(row[1]), border=1, align='C')
                    pdf.cell(epw / 7, 2.5 * th, str(row[2]), border=1, align='C')
                    pdf.cell(epw / 7, 2.5 * th, str(row[3]), border=1, align='C')
                    pdf.cell(epw / 7, 2.5 * th, str(row[4]), border=1, align='C')
                    pdf.ln(2.5 * th)
                pdf.cell(epw, 2.5 * th, 'Remarks:', border=1, align='R')
                pdf.ln(2.5 * th)
                pdf.cell(epw, 2.5 * th, '>  '+ c, border=1, align='R')
                pdf.ln(2.5 * th)
                pdf.cell(epw, 2.5 * th, ' Confirmed by : ' + user_id, border=0, align='R')
                pdf.ln(2.5 * th)


                pdf.output('document/DO_' + time_format + '.pdf', 'F')
                file = open('document/DO_' + time_format + '.pdf', 'rb')
                data = file.read()

                hash = hashlib.sha256(data).hexdigest()
                file.close()
                # 데이터 저장
                contract = Contract_DO(contractname=contractname, contract_id=contract_id, sha256=hash, status='new',
                                       filename='document/DO_' + time_format + '.pdf')

                # 로그인한 사용자 정보를 Contract에 같이 저장
                user_id = request.session['user_id']
                member = Member.objects.get(user_id=user_id)
                contract.owner = member
                contract.save()
                result_dict['result'] = "작성완료"
                return JsonResponse(result_dict)
            except Exception as e:
                result_dict['result'] = "영어로 작성해주세요."
                return JsonResponse(result_dict)
        else:
            result_dict['result'] = "해당 Contract id 는 사용할 수 없습니다."
            return JsonResponse(result_dict)
    except Exception as e:
        print(e)
        result_dict['result'] = "양식을 완성해주세요."
        return JsonResponse(result_dict)


def download(request):
    id = request.GET['id']
    c = Contract_LCR.objects.get(id=id)

    filepath = os.path.join(settings.BASE_DIR, c.filename)
    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
        return response


def download2_1(request):
    id = request.GET['id']
    c = Contract_OS.objects.get(id=id)

    filepath = os.path.join(settings.BASE_DIR, c.filename)
    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
        return response


def download2_2(request):
    id = request.GET['id']
    c = Contract_SR.objects.get(id=id)

    filepath = os.path.join(settings.BASE_DIR, c.filename)
    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
        return response


def download2_3(request):
    id = request.GET['id']
    c = Contract_CI.objects.get(id=id)

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


@csrf_exempt
def ing(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        try:
            if request.POST['filter'] == "new":
                contract = Contract_LCR.objects.filter(owner=member, status="new").order_by('-id')
                filter = "New"
            elif request.POST['filter'] == "rejected":
                contract = Contract_LCR.objects.filter(owner=member, status="rejected").order_by('-id')
                filter = "Rejected"
            elif request.POST['filter'] == "confirmed":
                contract = Contract_LCR.objects.filter(owner=member, status="confirmed").order_by('-id')
                filter = "Confirmed"
            elif request.POST['filter'] == "complete":
                contract = Contract_LCR.objects.filter(owner=member, status="complete").order_by('-id')
                filter = "Complete"
            else:
                contract = Contract_LCR.objects.filter(owner=member).order_by('-id')
                filter = "All"
        except:
            contract = Contract_LCR.objects.filter(owner=member).order_by('-id')
            filter = "All"
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

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2,
                  'filter': filter, 'user_id': user_id}

        return render(request, 'app/ing.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def ing2_1(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        try:
            if request.POST['filter'] == "new":
                contract = Contract_OS.objects.filter(owner=member, status="new").order_by('-id')
                filter = "New"
            elif request.POST['filter'] == "rejected":
                contract = Contract_OS.objects.filter(owner=member, status="rejected").order_by('-id')
                filter = "Rejected"
            elif request.POST['filter'] == "confirmed":
                contract = Contract_OS.objects.filter(owner=member, status="confirmed").order_by('-id')
                filter = "Confirmed"
            elif request.POST['filter'] == "complete":
                contract = Contract_OS.objects.filter(owner=member, status="complete").order_by('-id')
                filter = "Complete"
            else:
                contract = Contract_OS.objects.filter(owner=member).order_by('-id')
                filter = "All"
        except:
            contract = Contract_OS.objects.filter(owner=member).order_by('-id')
            filter = "All"
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

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2,
                  'filter': filter, 'user_id': user_id}

        return render(request, 'app/ing2_1.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def ing2_2(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        try:
            if request.POST['filter'] == "new":
                contract = Contract_SR.objects.filter(owner=member, status="new").order_by('-id')
                filter = "New"
            elif request.POST['filter'] == "rejected":
                contract = Contract_SR.objects.filter(owner=member, status="rejected").order_by('-id')
                filter = "Rejected"
            elif request.POST['filter'] == "confirmed":
                contract = Contract_SR.objects.filter(owner=member, status="confirmed").order_by('-id')
                filter = "Confirmed"
            elif request.POST['filter'] == "complete":
                contract = Contract_SR.objects.filter(owner=member, status="complete").order_by('-id')
                filter = "Complete"
            else:
                contract = Contract_SR.objects.filter(owner=member).order_by('-id')
                filter = "All"
        except:
            contract = Contract_SR.objects.filter(owner=member).order_by('-id')
            filter = "All"
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

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2,
                  'filter': filter, 'user_id': user_id}

        return render(request, 'app/ing2_2.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def ing2_3(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        try:
            if request.POST['filter'] == "new":
                contract = Contract_CI.objects.filter(owner=member, status="new").order_by('-id')
                filter = "New"
            elif request.POST['filter'] == "rejected":
                contract = Contract_CI.objects.filter(owner=member, status="rejected").order_by('-id')
                filter = "Rejected"
            elif request.POST['filter'] == "confirmed":
                contract = Contract_CI.objects.filter(owner=member, status="confirmed").order_by('-id')
                filter = "Confirmed"
            elif request.POST['filter'] == "complete":
                contract = Contract_CI.objects.filter(owner=member, status="complete").order_by('-id')
                filter = "Complete"
            else:
                contract = Contract_CI.objects.filter(owner=member).order_by('-id')
                filter = "All"
        except:
            contract = Contract_CI.objects.filter(owner=member).order_by('-id')
            filter = "All"
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

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2,
                  'filter': filter, 'user_id': user_id}

        return render(request, 'app/ing2_3.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def ing3(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        try:
            if request.POST['filter'] == "new":
                contract = Contract_LC.objects.filter(owner=member, status="new").order_by('-id')
                filter = "New"
            elif request.POST['filter'] == "rejected":
                contract = Contract_LC.objects.filter(owner=member, status="rejected").order_by('-id')
                filter = "Rejected"
            elif request.POST['filter'] == "confirmed":
                contract = Contract_LC.objects.filter(owner=member, status="confirmed").order_by('-id')
                filter = "Confirmed"
            elif request.POST['filter'] == "complete":
                contract = Contract_LC.objects.filter(owner=member, status="complete").order_by('-id')
                filter = "Complete"
            else:
                contract = Contract_LC.objects.filter(owner=member).order_by('-id')
                filter = "All"
        except:
            contract = Contract_LC.objects.filter(owner=member).order_by('-id')
            filter = "All"
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

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2,
                  'filter': filter, 'user_id': user_id}

        return render(request, 'app/ing3.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def ing4_1(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        try:
            if request.POST['filter'] == "new":
                contract = Contract_BL.objects.filter(owner=member, status2="new").order_by('-id')
                filter = "New"
            elif request.POST['filter'] == "rejected":
                contract = Contract_BL.objects.filter(owner=member, status2="rejected").order_by('-id')
                filter = "Rejected"
            elif request.POST['filter'] == "confirmed":
                contract = Contract_BL.objects.filter(owner=member, status2="confirmed").order_by('-id')
                filter = "Confirmed"
            elif request.POST['filter'] == "complete":
                contract = Contract_BL.objects.filter(owner=member, status2="complete").order_by('-id')
                filter = "Complete"
            else:
                contract = Contract_BL.objects.filter(owner=member).order_by('-id')
                filter = "All"
        except:
            contract = Contract_BL.objects.filter(owner=member).order_by('-id')
            filter = "All"
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

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2,
                  'filter': filter, 'user_id': user_id}

        return render(request, 'app/ing4_1.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def ing4_2(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        try:
            if request.POST['filter'] == "new":
                contract = Contract_DO.objects.filter(owner=member, status="new").order_by('-id')
                filter = "New"
            elif request.POST['filter'] == "rejected":
                contract = Contract_DO.objects.filter(owner=member, status="rejected").order_by('-id')
                filter = "Rejected"
            elif request.POST['filter'] == "confirmed":
                contract = Contract_DO.objects.filter(owner=member, status="confirmed").order_by('-id')
                filter = "Confirmed"
            elif request.POST['filter'] == "complete":
                contract = Contract_DO.objects.filter(owner=member, status="complete").order_by('-id')
                filter = "Complete"
            else:
                contract = Contract_DO.objects.filter(owner=member).order_by('-id')
                filter = "All"
        except:
            contract = Contract_DO.objects.filter(owner=member).order_by('-id')
            filter = "All"
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

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2,
                  'filter': filter, 'user_id': user_id}

        return render(request, 'app/ing4_2.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def osreceived(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        try:
            if request.POST['filter'] == "new":
                contract = Contract_OS.objects.filter(share1=member, status="new").order_by('-id')
                filter = "New"
            elif request.POST['filter'] == "rejected":
                contract = Contract_OS.objects.filter(share1=member, status="rejected").order_by('-id')
                filter = "Rejected"
            elif request.POST['filter'] == "confirmed":
                contract = Contract_OS.objects.filter(share1=member, status="confirmed").order_by('-id')
                filter = "Confirmed"
            elif request.POST['filter'] == "complete":
                contract = Contract_OS.objects.filter(share1=member, status="complete").order_by('-id')
                filter = "Complete"
            else:
                contract = Contract_OS.objects.filter(share1=member).order_by('-id')
                filter = "All"
        except:
            contract = Contract_OS.objects.filter(share1=member).order_by('-id')
            filter = "All"
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
                  'max_index': max_index - 2, 'filter': filter, 'user_id': user_id}

        return render(request, 'app/osreceived.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def cireceived(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        try:
            if request.POST['filter'] == "new":
                contract = Contract_CI.objects.filter(share1=member, status="new").order_by('-id')
                filter = "New"
            elif request.POST['filter'] == "rejected":
                contract = Contract_CI.objects.filter(share1=member, status="rejected").order_by('-id')
                filter = "Rejected"
            elif request.POST['filter'] == "confirmed":
                contract = Contract_CI.objects.filter(share1=member, status="confirmed").order_by('-id')
                filter = "Confirmed"
            elif request.POST['filter'] == "complete":
                contract = Contract_CI.objects.filter(share1=member, status="complete").order_by('-id')
                filter = "Complete"
            else:
                contract = Contract_CI.objects.filter(share1=member).order_by('-id')
                filter = "All"
        except:
            contract = Contract_CI.objects.filter(share1=member).order_by('-id')
            filter = "All"
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
                  'max_index': max_index - 2, 'filter': filter, 'user_id': user_id}

        return render(request, 'app/cireceived.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def srreceived(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        try:
            if request.POST['filter'] == "new":
                contract = Contract_SR.objects.filter(share4=member, status="new").order_by('-id')
                filter = "New"
            elif request.POST['filter'] == "rejected":
                contract = Contract_SR.objects.filter(share4=member, status="rejected").order_by('-id')
                filter = "Rejected"
            elif request.POST['filter'] == "confirmed":
                contract = Contract_SR.objects.filter(share4=member, status="confirmed").order_by('-id')
                filter = "Confirmed"
            elif request.POST['filter'] == "complete":
                contract = Contract_SR.objects.filter(share4=member, status="complete").order_by('-id')
                filter = "Complete"
            else:
                contract = Contract_SR.objects.filter(share4=member).order_by('-id')
                filter = "All"
        except:
            contract = Contract_SR.objects.filter(share4=member).order_by('-id')
            filter = "All"
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
                  'max_index': max_index - 2, 'filter': filter, 'user_id': user_id}

        return render(request, 'app/srreceived.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def blreceived1(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        try:
            if request.POST['filter'] == "new":
                contract = Contract_BL.objects.filter(share1=member, status1="new").order_by('-id')
                filter = "New"
            elif request.POST['filter'] == "rejected":
                contract = Contract_BL.objects.filter(share1=member, status1="rejected").order_by('-id')
                filter = "Rejected"
            elif request.POST['filter'] == "confirmed":
                contract = Contract_BL.objects.filter(share1=member, status1="confirmed").order_by('-id')
                filter = "Confirmed"
            elif request.POST['filter'] == "complete":
                contract = Contract_BL.objects.filter(share1=member, status1="complete").order_by('-id')
                filter = "Complete"
            else:
                contract = Contract_BL.objects.filter(share1=member).order_by('-id')
                filter = "All"
        except:
            contract = Contract_BL.objects.filter(share1=member).order_by('-id')
            filter = "All"
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
                  'max_index': max_index - 2, 'filter': filter, 'user_id': user_id}

        return render(request, 'app/blreceived1.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def lcreceived1(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        try:
            if request.POST['filter'] == "new":
                contract = Contract_LC.objects.filter(share1=member, status="new").order_by('-id')
                filter = "New"
            elif request.POST['filter'] == "rejected":
                contract = Contract_LC.objects.filter(share1=member, status="rejected").order_by('-id')
                filter = "Rejected"
            elif request.POST['filter'] == "confirmed":
                contract = Contract_LC.objects.filter(share1=member, status="confirmed").order_by('-id')
                filter = "Confirmed"
            elif request.POST['filter'] == "complete":
                contract = Contract_LC.objects.filter(share1=member, status="complete").order_by('-id')
                filter = "Complete"
            else:
                contract = Contract_LC.objects.filter(share1=member).order_by('-id')
                filter = "All"
        except:
            contract = Contract_LC.objects.filter(share1=member).order_by('-id')
            filter = "All"
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
                  'max_index': max_index - 2, 'filter': filter, 'user_id': user_id}

        return render(request, 'app/lcreceived1.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def blreceived2(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        try:
            if request.POST['filter'] == "new":
                contract = Contract_BL.objects.filter(share2=member, status2="new").order_by('-id')
                filter = "New"
            elif request.POST['filter'] == "rejected":
                contract = Contract_BL.objects.filter(share2=member, status2="rejected").order_by('-id')
                filter = "Rejected"
            elif request.POST['filter'] == "confirmed":
                contract = Contract_BL.objects.filter(share2=member, status2="confirmed").order_by('-id')
                filter = "Confirmed"
            elif request.POST['filter'] == "complete":
                contract = Contract_BL.objects.filter(share2=member, status2="complete").order_by('-id')
                filter = "Complete"
            else:
                contract = Contract_BL.objects.filter(share2=member).order_by('-id')
                filter = "All"
        except:
            contract = Contract_BL.objects.filter(share2=member).order_by('-id')
            filter = "All"
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
                  'max_index': max_index - 2, 'filter': filter, 'user_id': user_id}

        return render(request, 'app/blreceived2.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def blreceived3(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        try:
            if request.POST['filter'] == "new":
                contract = Contract_BL.objects.filter(share3=member, status3="new").order_by('-id')
                filter = "New"
            elif request.POST['filter'] == "rejected":
                contract = Contract_BL.objects.filter(share3=member, status3="rejected").order_by('-id')
                filter = "Rejected"
            elif request.POST['filter'] == "confirmed":
                contract = Contract_BL.objects.filter(share3=member, status3="confirmed").order_by('-id')
                filter = "Confirmed"
            elif request.POST['filter'] == "complete":
                contract = Contract_BL.objects.filter(share3=member, status3="complete").order_by('-id')
                filter = "Complete"
            else:
                contract = Contract_BL.objects.filter(share3=member).order_by('-id')
                filter = "All"
        except:
            contract = Contract_BL.objects.filter(share3=member).order_by('-id')
            filter = "All"
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
                  'max_index': max_index - 2, 'filter': filter, 'user_id': user_id}

        return render(request, 'app/blreceived3.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def lcreceived2(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        try:
            if request.POST['filter'] == "new":
                contract = Contract_LC.objects.filter(share2=member, status="new").order_by('-id')
                filter = "New"
            elif request.POST['filter'] == "rejected":
                contract = Contract_LC.objects.filter(share2=member, status="rejected").order_by('-id')
                filter = "Rejected"
            elif request.POST['filter'] == "confirmed":
                contract = Contract_LC.objects.filter(share2=member, status="confirmed").order_by('-id')
                filter = "Confirmed"
            elif request.POST['filter'] == "complete":
                contract = Contract_LC.objects.filter(share2=member, status="complete").order_by('-id')
                filter = "Complete"
            else:
                contract = Contract_LC.objects.filter(share2=member).order_by('-id')
                filter = "All"
        except:
            contract = Contract_LC.objects.filter(share2=member).order_by('-id')
            filter = "All"
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
                  'max_index': max_index - 2, 'filter': filter, 'user_id': user_id}

        return render(request, 'app/lcreceived2.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def doreceived(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        try:
            if request.POST['filter'] == "new":
                contract = Contract_DO.objects.filter(share1=member, status="new").order_by('-id')
                filter = "New"
            elif request.POST['filter'] == "rejected":
                contract = Contract_DO.objects.filter(share1=member, status="rejected").order_by('-id')
                filter = "Rejected"
            elif request.POST['filter'] == "confirmed":
                contract = Contract_DO.objects.filter(share1=member, status="confirmed").order_by('-id')
                filter = "Confirmed"
            elif request.POST['filter'] == "complete":
                contract = Contract_DO.objects.filter(share1=member, status="complete").order_by('-id')
                filter = "Complete"
            else:
                contract = Contract_DO.objects.filter(share1=member).order_by('-id')
                filter = "All"
        except:
            contract = Contract_DO.objects.filter(share1=member).order_by('-id')
            filter = "All"
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
                  'max_index': max_index - 2, 'filter': filter, 'user_id': user_id}

        return render(request, 'app/doreceived.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def lcrreceived(request):
    try:
        user_id = request.session['user_id']
        member = Member.objects.get(user_id=user_id)
        try:
            if request.POST['filter'] == "new":
                contract = Contract_LCR.objects.filter(share3=member, status="new").order_by('-id')
                filter = "New"
            elif request.POST['filter'] == "rejected":
                contract = Contract_LCR.objects.filter(share3=member, status="rejected").order_by('-id')
                filter = "Rejected"
            elif request.POST['filter'] == "confirmed":
                contract = Contract_LCR.objects.filter(share3=member, status="confirmed").order_by('-id')
                filter = "Confirmed"
            elif request.POST['filter'] == "complete":
                contract = Contract_LCR.objects.filter(share3=member, status="complete").order_by('-id')
                filter = "Complete"
            else:
                contract = Contract_LCR.objects.filter(share3=member).order_by('-id')
                filter = "All"
        except:
            contract = Contract_LCR.objects.filter(share3=member).order_by('-id')
            filter = "All"
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
                  'max_index': max_index - 2, 'filter': filter, 'user_id': user_id}

        return render(request, 'app/lcrreceived.html', notice)
    except Exception as e:
        print(e)
        return redirect('index')


def logout(request):
    try:
        del request.session['user_role']
        del request.session['user_id']
        return redirect('about')
    except Exception as e:
        print(e)
        return render(request, 'app/about.html', {})


def index(request):
    try:
        user_id = request.session['user_id']

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

        new_os = len(Contract_OS.objects.filter(share1=user_id, status='new'))
        new_lc = len(Contract_LC.objects.filter(share1=user_id, status='new'))
        new_bl = len(Contract_BL.objects.filter(share1=user_id, status1='new'))
        new_ci = len(Contract_CI.objects.filter(share1=user_id, status='new'))
        new_do = len(Contract_DO.objects.filter(share1=user_id, status='new'))
        ing = len(Process.objects.filter(user1=user_id, status='ing'))
        complete = len(Process.objects.filter(user1=user_id, status='complete'))
        all_doc = new_do + new_bl + new_ci + new_lc + new_os
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

        return render(request, 'app/index.html',
                      {'user_id': user_id, 'date': time, 'notice': notice, 'result': result, 'complete': complete,
                       'ing': ing, 'new_os': new_os, 'new_lc': new_lc, 'new_bl': new_bl, 'new_ci': new_ci,
                       'new_do': new_do, 'all_doc': all_doc})
    except Exception as e:
        print(e)
        return redirect('login')


def index2(request):
    try:

        user_id = request.session['user_id']

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

        new_lc = len(Contract_LC.objects.filter(share2=user_id, status='new'))
        new_bl = len(Contract_BL.objects.filter(share2=user_id, status2='new'))
        ing = len(Process.objects.filter(user2=user_id, status='ing'))
        complete = len(Process.objects.filter(user2=user_id, status='complete'))
        all_doc = new_lc + new_bl
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

        data = {'user_id': user_id, 'date': time, 'notice': notice, 'result': result, 'complete': complete, 'ing': ing,
                'new_lc': new_lc, 'new_bl': new_bl, 'all_doc': all_doc}
        return render(request, 'app/index2.html', data)
    except Exception as e:
        print(e)
        return redirect('login')


def index3(request):
    try:

        user_id = request.session['user_id']

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

        new_lcr = len(Contract_LCR.objects.filter(share3=user_id, status='new'))
        new_bl = len(Contract_BL.objects.filter(share3=user_id, status3='new'))
        ing = len(Process.objects.filter(user3=user_id, status='ing'))
        complete = len(Process.objects.filter(user3=user_id, status='complete'))
        all_doc = new_lcr + new_bl
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

        return render(request, 'app/index3.html',
                      {'user_id': user_id, 'date': time, 'notice': notice, 'result': result, 'complete': complete,
                       'ing': ing, 'new_lcr': new_lcr, 'new_bl': new_bl, 'all_doc': all_doc})
    except Exception as e:
        print(e)
        return redirect('login')


def index4(request):
    try:

        user_id = request.session['user_id']

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

        new_sr = len(Contract_SR.objects.filter(share4=user_id, status='new'))
        ing = len(Process.objects.filter(user4=user_id, status='ing'))
        complete = len(Process.objects.filter(user4=user_id, status='complete'))
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

        return render(request, 'app/index4.html',
                      {'user_id': user_id, 'date': time, 'notice': notice, 'result': result, 'complete': complete,
                       'ing': ing, 'new_sr': new_sr, })
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
        user_id = request.session['user_id']
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
                       'basePrice4': basePrice4, 'sellprice4': sellprice4, 'buyprice4': buyprice4, 'user_id': user_id})


    except Exception as e:
        print(e)
        return redirect('login')


def forms(request):
    user_id = request.session['user_id']
    contract = Contract_OS.objects.filter(share1=user_id, status='confirmed').order_by('-id')
    return render(request, 'app/forms.html', {'contract': contract, 'user_id': user_id})


def forms2_1(request):
    user_id = request.session['user_id']
    return render(request, 'app/forms2_1.html', {'user_id': user_id})


def forms2_2(request):
    user_id = request.session['user_id']
    contract = Contract_LC.objects.filter(share2=user_id, status='confirmed').order_by('-id')
    return render(request, 'app/forms2_2.html', {'contract': contract, 'user_id': user_id})


def forms2_3(request):
    user_id = request.session['user_id']
    contract = Contract_BL.objects.filter(share2=user_id, status3='confirmed').order_by('-id')
    return render(request, 'app/forms2_3.html', {'contract': contract, 'user_id': user_id})


def forms3(request):
    user_id = request.session['user_id']
    contract = Contract_LCR.objects.filter(share3=user_id, status='confirmed').order_by('-id')
    return render(request, 'app/forms3.html', {'contract': contract, 'user_id': user_id})


def forms4_1(request):
    user_id = request.session['user_id']
    contract = Contract_SR.objects.filter(share4=user_id, status='confirmed').order_by('-id')
    return render(request, 'app/forms4_1.html', {'contract': contract, 'user_id': user_id})


def forms4_2(request):
    user_id = request.session['user_id']
    contract = Contract_BL.objects.filter(owner=user_id, status3='confirmed').order_by('-id')
    return render(request, 'app/forms4_2.html', {'contract': contract, 'user_id': user_id})


def login(request):
    if request.method == 'GET':
        return render(request, 'app/login.html', {})
    else:
        email = request.POST['email']
        user_pw = request.POST['password']
        user_role = request.POST['user_role']
        password = hashlib.sha256(user_pw.encode('utf-8')).hexdigest()

        try:
            Member.objects.get(user_role=user_role, user_id=email, user_pw=password)
            result_dict = {'result': 'success', 'role': user_role}
            request.session['user_id'] = email
            request.session['user_role'] = user_role
        except Member.DoesNotExist:
            result_dict = {'result': 'fail'}
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
                            address=user_address, tbc=tbc, businessnum=businessnum, otpkey="Not yet issued")
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
