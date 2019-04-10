from dadata.find_party import DadataFindPartyClient
import time, uuid
keyy = 'abf14d0b25b6fb82ea3a316353fdb9d06eaf5d76'
def mainn(inn):
    start_time = time.time()
    #____________________________________________________<для выгрузки инфы по организации>
    def start(inn):
        key = str(uuid.uuid4())
        all_info = []
        dadata = DadataFindPartyClient(key=keyy)
        data = dadata.request(inn)
        return (data,key)
    #____________________________________________________</для выгрузки инфы по организации>

    data,key = start(inn)
    if data is None:
        print('Введен некорректный ИНН')
    else:
        data = data[0]
    
    print("--- %s seconds ---" % (time.time() - start_time))
    return (data,key)
            
if __name__ == "__main__":
    print (sys.argv[1])
    mainn(sys.argv[1])
