# !/usr/bin/env python3
# pip3 install pycryptodome py7zr -i https://pypi.tuna.tsinghua.edu.cn/simple
# 源码参见 https://github.com/lersh/TudouCode/
# 代码更新 https://github.com/playGitboy/foYu.py/edit/main/%E4%B8%8E%E4%BD%9B%E8%AE%BA%E7%A6%85.py

from Crypto.Cipher import AES
from re import split
from py7zr import SevenZipFile
from io import BytesIO

KEY = b'XDXDtudou@KeyFansClub^_^Encode!!'
IV = b'Potato@Key@_@=_='

BYTEMARK = ['冥', '奢', '梵', '呐', '俱', '哆', '怯', '諳', '罰', '侄', '缽', '皤']

BUDDHA1 = [
    '滅', '苦', '婆', '娑', '耶', '陀', '跋', '多', '漫', '都', '殿', '悉', '夜', '爍', '帝', '吉',
    '利', '阿', '無', '南', '那', '怛', '喝', '羯', '勝', '摩', '伽', '謹', '波', '者', '穆', '僧',
    '室', '藝', '尼', '瑟', '地', '彌', '菩', '提', '蘇', '醯', '盧', '呼', '舍', '佛', '參', '沙',
    '伊', '隸', '麼', '遮', '闍', '度', '蒙', '孕', '薩', '夷', '迦', '他', '姪', '豆', '特', '逝',
    '朋', '輸', '楞', '栗', '寫', '數', '曳', '諦', '羅', '曰', '咒', '即', '密', '若', '般', '故',
    '不', '實', '真', '訶', '切', '一', '除', '能', '等', '是', '上', '明', '大', '神', '知', '三',
    '藐', '耨', '得', '依', '諸', '世', '槃', '涅', '竟', '究', '想', '夢', '倒', '顛', '離', '遠',
    '怖', '恐', '有', '礙', '心', '所', '以', '亦', '智', '道', '。', '集', '盡', '死', '老', '至']

BUDDHA2 = [
    '謹', '穆', '僧', '室', '藝', '瑟', '彌', '提', '蘇', '醯', '盧', '呼', '舍', '參', '沙', '伊',
    '隸', '麼', '遮', '闍', '度', '蒙', '孕', '薩', '夷', '他', '姪', '豆', '特', '逝', '輸', '楞',
    '栗', '寫', '數', '曳', '諦', '羅', '故', '實', '訶', '知', '三', '藐', '耨', '依', '槃', '涅',
    '竟', '究', '想', '夢', '倒', '顛', '遠', '怖', '恐', '礙', '以', '亦', '智', '盡', '老', '至',
    '吼', '足', '幽', '王', '告', '须', '弥', '灯', '护', '金', '刚', '游', '戏', '宝', '胜', '通',
    '药', '师', '琉', '璃', '普', '功', '德', '山', '善', '住', '过', '去', '七', '未', '来', '贤',
    '劫', '千', '五', '百', '万', '花', '亿', '定', '六', '方', '名', '号', '东', '月', '殿', '妙',
    '尊', '树', '根', '西', '皂', '焰', '北', '清', '数', '精', '进', '首', '下', '寂', '量', '诸',
    '多', '释', '迦', '牟', '尼', '勒', '阿', '閦', '陀', '中', '央', '众', '生', '在', '界', '者',
    '行', '于', '及', '虚', '空', '慈', '忧', '各', '令', '安', '稳', '休', '息', '昼', '夜', '修',
    '持', '心', '求', '诵', '此', '经', '能', '灭', '死', '消', '除', '毒', '害', '高', '开', '文',
    '殊', '利', '凉', '如', '念', '即', '说', '曰', '帝', '毘', '真', '陵', '乾', '梭', '哈', '敬',
    '禮', '奉', '祖', '先', '孝', '雙', '親', '守', '重', '師', '愛', '兄', '弟', '信', '朋', '友',
    '睦', '宗', '族', '和', '鄉', '夫', '婦', '教', '孫', '時', '便', '廣', '積', '陰', '難', '濟',
    '急', '恤', '孤', '憐', '貧', '創', '廟', '宇', '印', '造', '經', '捨', '藥', '施', '茶', '戒',
    '殺', '放', '橋', '路', '矜', '寡', '拔', '困', '粟', '惜', '福', '排', '解', '紛', '捐', '資']

BUDDHA3 = {
    '啰':'e', '羯':'E', '婆':'t', '提':'T', '摩':'a', '埵':'A', '诃':'o', '迦':'O', '耶':'i', '吉':'I', 
    '娑':'n', '佛':'N', '夜':'s', '驮':'S', '那':'h', '谨':'H', '悉':'r', '墀':'R', '阿':'d', '呼':'D', 
    '萨':'l', '尼':'L', '陀':'c', '唵':'C', '唎':'u', '伊':'U', '卢':'m', '喝':'M', '帝':'w', '烁':'W', 
    '醯':'f', '蒙':'F', '罚':'g', '沙':'G', '嚧':'y', '他':'Y', '南':'p', '豆':'P', '无':'b', '孕':'B', 
    '菩':'v', '伽':'V', '怛':'k', '俱':'K', '哆':'j', '度':'J', '皤':'x', '阇':'X', '室':'q', '地':'Q', 
    '利':'z', '遮':'Z', '穆':'0', '参':'1', '舍':'2', '苏':'3', '钵':'4', '曳':'5', '数':'6', '写':'7', 
    '栗':'8', '楞':'9', '咩':'+', '输':'/', '漫':'='
}

# https://www.keyfc.net/bbs/tools/tudoucode.aspx
# 知哆提怯等呐心罰是呐悉呐亦奢無皤以真皤密阿諸怯薩奢想穆
# 佛曰
def DecryptBUDDHA1(ciphertext):
    data = b''
    i = 0
    while i < len(ciphertext):
        if ciphertext[i] in BYTEMARK:
            i += 1
            data += bytes([BUDDHA1.index(ciphertext[i]) + 128])
        else:
            data += bytes([BUDDHA1.index(ciphertext[i])])
        i += 1
    cryptor = AES.new(KEY, AES.MODE_CBC, IV)
    result = cryptor.decrypt(data)
    flag = result[-1]
    if flag < 16 and result[-flag] == flag:
        result = result[:-flag]
    return result.decode('utf-16le')

# https://www.keyfc.net/bbs/tools/tudoucode.aspx
# 如是我闻
def DecryptBUDDHA2(ciphertext):
    data = b''
    for i in ciphertext:
        data += bytes([BUDDHA2.index(i)])
    cryptor = AES.new(KEY, AES.MODE_CBC, IV)
    fsevenZip=SevenZipFile(BytesIO(cryptor.decrypt(data)))
    zipContent = fsevenZip.readall()['default'].read()
    return zipContent

# http://www.atoolbox.net/Tool.php?Id=1027
# https://github.com/takuron/talk-with-buddha
# 栗沙啰皤烁唎夜俱曳数悉栗提曳穆诃地无俱烁帝唎利沙吉伽摩伊穆咩陀唎诃漫
# 佛又曰
def DecryptBUDDHA3(ciphertext):
    for k,v in zip(BUDDHA3.keys(),BUDDHA3.values()):
        ciphertext = ciphertext.replace(k,v)
    data = ciphertext.encode("utf-8")
    # password = "takuron.top";
    password = b"U2FsdGVkX1+9azMGhHoOZ59u"
    cryptor = AES.new(password, AES.MODE_CBC, IV)
    result = cryptor.decrypt(data)
    flag = result[-1]
    if flag < 16 and result[-flag] == flag:
        result = result[:-flag]
    return result.decode('utf-16le')

# http://hi.pcmoe.net/buddha.html
# 諸羯隸羯僧羯降羯吽諸陀摩隸僧羯缽羯薩咤羯尊如羯阿如如羯囑囑羯
# 新佛曰
def DecryptBUDDHA4(ciphertext):
    pass

def decode(ciphertext):
    out = ''
    try:
        out = DecryptBUDDHA1(ciphertext)
        return out
    except Exception as _: pass

    try:
        out = DecryptBUDDHA2(ciphertext)
        return out
    except Exception as _: raise _


