from Crypto.Cipher import AES
import binascii


BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

class SagepayCrypt:
    def __init__(self, key):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)

        cipher = AES.new( self.key, AES.MODE_CBC, self.key )
        encrypted_text = binascii.hexlify(cipher.encrypt(raw))
        return encrypted_text.decode('utf-8').upper()


    def decrypt(self, enc):
        """
        Requires hex encoded param to decrypt
        """
        enc = binascii.unhexlify(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.key )
        decrypt = cipher.decrypt(enc)
        decrypted_text = decrypt.decode('utf8')
        unpadded = unpad(decrypted_text)
        return unpadded

if __name__== "__main__":
    # EXAMPLE USAGE
    # From the sagepay documentation
    key = "55a51621a6648525"
    basket_data = 'VendorTxCode=TxCode-1310917599-223087284&Amount=36.95&Currency=GBP&Description=description&CustomerName=Fname Surname&CustomerEMail=customer@example.com&BillingSurname=Surname&BillingFirstnames=Fname&BillingAddress1=BillAddress Line 1&BillingCity=BillCity&BillingPostCode=W1A 1BL&BillingCountry=GB&BillingPhone=447933000000&DeliveryFirstnames=Fname&DeliverySurname=Surname&DeliveryAddress1=BillAddress Line 1&DeliveryCity=BillCity&DeliveryPostCode=W1A 1BL&DeliveryCountry=GB&DeliveryPhone=447933000000&SuccessURL=https://example.com/success&FailureURL=https://example.com/failure'
    # Encypt the basket data using our key and padding
    result = SagepayCrypt(key).encrypt(basket_data)
    # Post to the url
    url = 'https://test.sagepay.com/gateway/service/vspform-register.vsp?VPSProtocol=3.00&TxType=AUTHENTICATE&Vendor=VENDORNAME&Crypt=@' + result
    # Test the decrypted text is the same as the basket_data
    decrypt = SagepayCrypt(key).decrypt(result)
    print(decrypt)
