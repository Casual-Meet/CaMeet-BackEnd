def active_message(domain, uidb64, token):
    return f"아래 링크를 클릭하면 학교 인증이 완료됩니다.\n\n 학교 인증 링크 : http://{domain}/accounts/activate/{uidb64}/{token}\n\n감사합니다."