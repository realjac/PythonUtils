import smtplib
import imaplib
import poplib
from email.header import Header
from email.mime.text import MIMEText

from utils.logger import logger



class Pop3Mail(object):
    def __init__(self, smtpserver='mail.test.com'):
        self.smtpserver = smtpserver
        self.timeout = 5
        
    def conn(self,user, password):
        try:
            server = poplib.POP3_SSL(self.smtpserver, 995)
            server.user(user)
            server.pass_(password)
            print("login success!")
        except Exception as e:
            print("login failed!")
            print(e)

class Imap4Mail(object):
    def __init__(self, smtpserver='mail.test.com'):
        self.smtpserver = smtpserver
        self.timeout = 5
        
    def conn(self,login_name, password):
        server = imaplib.IMAP4_SSL(self.smtpserver, 993)
        full_password = password
        try:
            server.login(login_name, full_password)
            print(login_name + ' | ' + full_password)
            print('[+]  Login Success!')
        except Exception as e:
            print(e)

class SmtpMail(object):
    """
    用法：
    SendMail("mail.test.com").send("test@test.com", aliasname='',password='',mailto=['admin@test.com'], subject='test',content='这是一个测试邮件',header='')
    """

    def __init__(self, smtpserver='mail.test.com'):
        self.smtpserver = smtpserver
        self.timeout = 5
    

    def send_email(self, sender, aliasname=None, password=None, mailto=[], subject='', content='', header=''):
        '''
        发送邮件
        :param sender: 发送者，可用于发送匿名邮件
        :param aliasname: 别名，认证方式时使用别名登录
        :param password: 密码，认证登录
        :param mailto: 收件者
        :param subject: 邮件主题
        :param content: 邮件内容
        :param header: header类型，可以用于伪造收件者
        :return:
        '''
        smtpserver = self.smtpserver
        msg = MIMEText(content, 'html', 'utf-8')
        msg['subject'] = subject
        msg['from'] = sender
        msg['to'] = Header(header, 'utf-8')
        msg['to'] = ','.join(mailto)

        try:
            if (aliasname is not None) and (password is not None):
                smtpobj = smtplib.SMTP(smtpserver, 587)
                smtpobj.ehlo()
                smtpobj.starttls()
                smtpobj.login(aliasname, password)
            else:
                smtpobj = smtplib.SMTP(smtpserver, 25)
            smtpobj.sendmail(sender, mailto, msg.as_string())
            smtpobj.quit()
            logger.info('邮件发送成功，发送给{}'.format(mailto))
            # print('-' * 60 + '\n' + '邮件发送成功')
        except Exception as e:
            logger.error('邮件发送失败，{}'.format(e))
            # print(e, '\n-----------\n邮件发送失败')
            
            


