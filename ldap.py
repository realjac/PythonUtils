
import ldap
from lib.utils.time_utils import convert_ad_timestamp

from lib.utils.get_py_version import *
from lib.utils.logger import logger
# 连接ldap的账号密码和ldap的访问链接
from lib.conf.config import get_ldap_info
ldap_url, ldap_user_bind_dn, ldap_password = get_ldap_info()


def con_ldap(user=ldap_user_bind_dn, password=ldap_password):
   
    # 连接ldap服务器
    ld_con = ldap.initialize(ldap_url)
    ld_con.protocol_version = ldap.VERSION3
    ld_con.simple_bind_s(user, password)

    return ld_con


def find_ldap_user(attrlist, dn):
    '''
    从ldap批量取用户信息
    :param attrlist: 需要的字段，如 ['sAMAccountName', 'name', 'userAccountControl', 'msExchHomeServerName']
    :param dn: DN条件，查询的范围
    :return: account_list普通账号的信息
    '''
    import ldap.controls
    # 分页查询
    page_control = ldap.controls.SimplePagedResultsControl(True, size=1000, cookie='')

    # 最后生成的用户列表
    account_list = []
    try:
        con = con_ldap()
        while 1:
            msgid = con.search_ext(dn, ldap.SCOPE_SUBTREE, attrlist=attrlist, serverctrls=[page_control])
            a, res_data, b, srv_ctrls = con.result3(msgid)
            for info in res_data:
                # TODO ：此处可去除这两种条件限制，在后面过滤
                # msExchHomeServerName 表明用户具有exchange server邮箱，而不是其他类型的AD账号
                if 'userAccountControl' in str(info[1]) and 'Exchange' in str(info[1]):
                    if PY2:
                        # userAccountControl记录AD账号的属性，该属性标志是累积性的，32不需要密码，512是普通账号66048=65536+512,514是禁用账号，
                        if info[1]['userAccountControl'][0] in ['512', '544', '66048', '66080', '262656', '262688',
                                                                '328192', '328224']:
                            account_list.append(info)

                    elif PY3:
                        if info[1]['userAccountControl'][0] in [b'512', b'544', b'66048', b'66080', b'262656',
                                                                b'262688',
                                                                b'328192', b'328224']:
                            account_list.append(info)

            cookie = srv_ctrls[0].cookie
            if cookie:
                page_control.cookie = cookie
            else:
                break

    except Exception as e:
        logger.error(e)

    return account_list
