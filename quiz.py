from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABdRBBm3a17hzUV9wK6ObmRCI5mwNeHyPKhQ2EqGZYWzck3rO--QFxntyYD-7MSkVMjMPDg0njSMcx1Ll9hMFD8nCgxATA-jQ76zPWBLuqq3LRYPMyGhW-FbjIgGl1IGHNiX07DINmb26z-bf6uFQPHFaQPc7YhcwCbFOFAcYSJmY_bU-8='


def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
