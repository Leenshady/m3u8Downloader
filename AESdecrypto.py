from Crypto.Cipher import AES
#from Crypto.Util.Padding import pad, unpad

def aesDecrypt(key, data, iv):
    '''
    :param key: 密钥
    :param data: 加密后的数据（密文）
    :param iv: IV
    :return:明文
    '''
    cipher = AES.new(key,AES.MODE_CBC,iv)

    counts=0
    #补位
    counts = len(data) % 16
    for i in range(counts):
        data += b"0"
    #解密 
    text_decrypted = cipher.decrypt(data)
    #去补位
    for i in range(counts):
        text_decrypted -= b"0"
    return text_decrypted
