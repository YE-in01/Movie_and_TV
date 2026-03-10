# import hashlib
# import time
# from django.conf import settings
#
# def generate_verify_token(email):
#     """生成邮箱验证token（有效期1小时）"""
#     # 组合邮箱和时间戳，加盐加密
#     timestamp = int(time.time()) + 3600  # 1小时有效期
#     content = f"{email}_{timestamp}_{settings.SECRET_KEY}".encode()
#     token = hashlib.md5(content).hexdigest()
#     return f"{token}_{timestamp}"  # 格式：token_时间戳
#
#
# def verify_token(email, token_str):
#     """验证token是否有效"""
#     try:
#         token, timestamp = token_str.split('_')
#         # 检查是否过期
#         if int(timestamp) < int(time.time()):
#             return False
#         # 重新计算token并对比
#         content = f"{email}_{timestamp}_{settings.SECRET_KEY}".encode()
#         expected_token = hashlib.md5(content).hexdigest()
#         return token == expected_token
#     except (ValueError, IndexError):
#         return False


import urllib.parse
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
import logging
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

# 生成验证token（修复编码问题）
def generate_verify_token(email):
    """生成无空格的验证token"""
    signer = TimestampSigner()
    # 替换token中的空格，避免URL解析异常
    token = signer.sign(email).replace(' ', '_')
    return token


# 验证token（增加过期时间判断）
def verify_token(email, token, max_age=86400):
    """验证token有效性，max_age默认24小时"""
    signer = TimestampSigner()
    try:
        # 反向替换：将_换回空格
        token = token.replace('_', ' ')
        # 验证token并检查过期时间
        original_email = signer.unsign(token, max_age=max_age)
        return original_email == email
    except (BadSignature, SignatureExpired):
        return False


# 生成验证链接（核心修复：正确拼接URL，避免二次编码）
def generate_verify_url(email):
    """生成无空格、编码正确的验证链接"""
    token = generate_verify_token(email)
    # 严格编码参数（确保无空格/特殊字符）
    encoded_email = urllib.parse.quote(email, safe='')
    encoded_token = urllib.parse.quote(token, safe='')

    # 核心：使用前端设备可访问的IP（不能用localhost）
    # 替换为前端所在电脑的局域网IP（如192.168.1.100）
    verify_url = f"{settings.SITE_DOMAIN}/verify-email?email={encoded_email}&token={encoded_token}"

    return verify_url


def send_verification_email(email, is_resend=False):
    """
    公共的邮箱验证邮件发送函数
    :param email: 接收邮件的邮箱
    :param is_resend: 是否是重新发送（用于区分邮件标题/内容）
    :return: tuple (success: bool, message: str)
    """
    try:
        verify_url = generate_verify_url(email)
        # 根据是否重发，设置不同的邮件内容
        if is_resend:
            subject = "【影视平台】重新发送邮箱验证链接"
            #兼容老式客户端
            plain_message = f""" 
            您请求重新发送邮箱验证链接，请在1小时内点击下方链接完成验证：

            {verify_url}

            若点击链接无法打开，请复制整段链接到浏览器地址栏手动打开。
            验证链接有效期1小时，超时需再次申请。
            """
            html_message = f"""
            <div style="font-family: Arial, sans-serif; line-height: 1.6;">
                <p>您请求重新发送邮箱验证链接，请在1小时内完成验证：</p>
                <p style="margin: 20px 0;">
                    <a href="{verify_url}" target="_blank" style="
                        padding: 10px 20px;
                        background: #409eff;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                    ">点击验证邮箱</a>
                </p>
                <p>若按钮无法点击，请复制以下链接到浏览器打开：</p>
                <p style="word-break: break-all; color: #666;">{verify_url}</p>
                <p>验证链接有效期1小时，超时需再次申请。</p>
            </div>
            """
        else:
            subject = "【影视平台】邮箱验证通知"
            plain_message = f"""
            恭喜您注册影视平台成功！请在1小时内点击下方链接完成邮箱验证：

            {verify_url}

            若点击链接无法打开，请复制整段链接到浏览器地址栏手动打开。
            如非本人操作，请忽略此邮件。
            """
            html_message = f"""
            <div style="font-family: Arial, sans-serif; line-height: 1.6;">
                <p>恭喜您注册影视平台成功！请在1小时内完成邮箱验证：</p>
                <p style="margin: 20px 0;">
                    <a href="{verify_url}" target="_blank" style="
                        padding: 10px 20px;
                        background: #409eff;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                    ">点击验证邮箱</a>
                </p>
                <p>若按钮无法点击，请复制以下链接到浏览器打开：</p>
                <p style="word-break: break-all; color: #666;">{verify_url}</p>
                <p>验证链接有效期1小时，超时需重新注册。</p>
            </div>
            """

        # 发送邮件（双格式兼容）
        send_mail(
            subject=subject,
            message=plain_message.strip(),
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return True, "邮件发送成功"

    except Exception as e:
        logger.error(f"发送验证邮件失败（邮箱：{email}）: {str(e)}")
        return False, f"邮件发送失败：{str(e)}"