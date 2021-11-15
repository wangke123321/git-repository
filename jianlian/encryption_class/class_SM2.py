from gmssl import sm2
# sm2的公私钥
SM2_PRIVATE_KEY = '198624c5d1c8955bc108450c03cf55fa736e4a5c6d1bf7f0269062703c4775f6'
SM2_PUBLIC_KEY = '04137c854d36efaf201a02b4e236364172733df6d4ada2fe57249b945732b62e2326f92b8be608d914fab44e2dc264acb53767e6d32034ff38ef6175648a199046'

sm2_crypt = sm2.CryptSM2(public_key=SM2_PUBLIC_KEY, private_key=SM2_PRIVATE_KEY)

# 加密
def encrypt(info):
    encode_info = sm2_crypt.encrypt(info.encode(encoding="utf-8"))
    return encode_info


# 解密
def decrypt(info):
    decode_info = sm2_crypt.decrypt(info).decode(encoding="utf-8")
    return decode_info


if __name__ == "__main__":
    info = "{'agentAccount':'dljianl','details':[{'subAgentAccount':'csdl1028103','serialNumber':'csdlo2021081623','operatingType':'2','machineNo':'PM20212116031','machineStatus':'1','merCode':'847109200004098'}]}"
    encode_info = encrypt(info)
    print(encode_info)
    # decode_info = decrypt(encode_info)
    # print(decode_info)