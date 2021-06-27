import socket
import binascii
from Crypto.Util.Padding import pad,unpad


class Attack:
    BLOCK_SIZE = 16
    BUF_SIZE = 4096
    USER = 'aemin'
    PASSWORD = 'g0ld3n_b0y'
    #PASSWORD = 'y' * 10
    TRY_AGAIN = 'Please try again.'
    LOGGED_IN = 'Logged in successfully!'
    CBC_WARNING = 'Data must be padded to 16 byte boundary in CBC mode'
    FAILURE = '[FAILURE]'
    SUCCESS = '[SUCCESS]'
    VALID_DATA = 'logged_username=' + USER + '&password=' + PASSWORD
    EXAMPLE = "7e1777b89d33bed4d41c3f2d99e6d12b743d884083e007ff4b08ae80ee0d1872f661abae70ac3440f1fba3eb45b6fc0c"
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def _connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        self.s = s

    def _recv_msg(self):
        return self.s.recv(self.BUF_SIZE).decode()

    def _send_msg(self, msg):
        self.s.send(msg)

    def _negotiate(self, password, ciphertext):
        self._recv_msg()
        self._send_msg(self.USER.encode())
        self._recv_msg()
        self._send_msg(password.encode())
        self._recv_msg()
        leak = self._recv_msg().split('\n')[0][19:]
        self._send_msg(ciphertext.encode())
        response = self._recv_msg()
        print(response)
        return leak, response

    def _one_time_connection(self, password, ciphertext, just_leak=False):
        self._connect()
        if not just_leak:
            ciphertext = self._xor_last_byte().hex()
            print(ciphertext)
            leak, response = self._negotiate(password, ciphertext)
            if response == self.TRY_AGAIN or self.CBC_WARNING in response:
                print(self.FAILURE)
                print(response)
            elif self.LOGGED_IN in response:
                print(self.SUCCESS * 100)
                print(self._recv_msg())
                exit()
        else:
            leak, response = self._negotiate(password, ciphertext)
            self._process(leak)
        self.s.close()

    def _process(self, leak):
        print(f'[lEAK]: {leak}')
        leak = binascii.unhexlify(leak)
        self.leak = leak
        print(leak)
        self.data = leak[:41]
        self.padding = leak[41:]
        print('padding', self.padding)
        print('padding len', len(self.padding))
        print('data len', len(self.data))
        hex_data = binascii.hexlify(self.data).decode()
        print(f'[DATA]: {hex_data}')
    
    def _xor_last_byte(self):
        ind = 0
        first_byte = self.data[ind]
        #ind2 = ind * 2
        #second_byte = self.data[ind2]
        #print(first_byte)
        first_byte ^= self.xor_value
        #second_byte ^= self.data[ind2]
        #print(first_byte)
        #print('data[:-1] len', len(self.data[:-1]))
        #new_data = self.data[:ind] + chr(first_byte).encode() + self.data[ind + 1:ind2] + chr(second_byte).encode() + self.data[ind2 + 1:]  + self.padding
        print(ind)
        print(chr(first_byte))
        print(chr(first_byte).encode())
        first_byte = chr(first_byte).encode()
        if len(first_byte) > 1:
            return b'nothing'
        new_data = self.data[:ind] + first_byte + self.data[ind + 1:] + self.padding
        print(self.leak)
        print(new_data)
        print(len(new_data))
        #self.not_found = False
        return new_data

    def launch(self):
        self._one_time_connection(self.PASSWORD, self.EXAMPLE, True)
        self.not_found = True
        for i in range(1, 128):
            self.xor_value = i
            print(f'[ITERATION]: {self.xor_value}')
            self._one_time_connection(self.PASSWORD, self.EXAMPLE)


def main():
    #ip = '188.166.169.77'
    #port = 30618
    ip = '127.0.0.1'
    port = 1337
    attack = Attack(ip, port)
    attack.launch()
    

if __name__=='__main__':
    main()

