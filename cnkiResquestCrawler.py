import requests
import util
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import time


# 获取网页信息
def requestUrl(fundId):
    url = "https://kns.cnki.net/KNS8/Brief/GetGridTableHtml"
    headers = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7",
        "Connection": "keep-alive",
        "Content-Length": "5414",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": '''Ecp_notFirstLogin=ahFJRa; cangjieStatus_NZKPT2=false; Ecp_ClientId=c220512155201683929; Ecp_loginuserbk=dx0752; knsLeftGroupSelectItem=1%3B2%3B; SID_sug=126004; Ecp_session=1; ASP.NET_SessionId=xfebh54jtpqlqzc2kjnkrnoy; SID_kns8=123160; ASPSESSIONIDASBQCARB=NEILJOLDIAGMCKNJLOLFBIPE; CurrSortField=%e7%9b%b8%e5%85%b3%e5%ba%a6%2frelevant%2c(%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2c%27time%27)+desc; CurrSortFieldType=desc; Ecp_ClientIp=202.113.189.252; SID_kcms=015126026; SID_docpre=128001; SID_kns_new=kns128006; _pk_ref=%5B%22%22%2C%22%22%2C1663120799%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DHH-ohc-RRydHuIr6NVRIt-FPoDL-2_BmMthyMoNDJy7%26wd%3D%26eqid%3D967cab3f000457540000000363212b9d%22%5D; _pk_id=21779c79-8106-4eee-83d9-7be37eaf914c.1652341966.7.1663121468.1663120799.; LID=WEEvREcwSlJHSldSdmVqMDh6cEFFeVNmNFVzMU0xc1hUbXdBVkE1RUZlUT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!; Ecp_LoginStuts={"IsAutoLogin":false,"UserName":"dx0752","ShowName":"%E5%A4%A9%E6%B4%A5%E5%A4%A7%E5%AD%A6","UserType":"bk","BUserName":"","BShowName":"","BUserType":"","r":"ahFJRa"}; dblang=ch; c_m_LinID=LinID=WEEvREcwSlJHSldSdmVqMDh6cEFFeVNmNFVzMU0xc1hUbXdBVkE1RUZlUT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!&ot=09%2f14%2f2022%2011%3a24%3a41; c_m_expire=2022-09-14%2011%3a24%3a41''',
        "Host": "kns.cnki.net",
        "Origin": "https://kns.cnki.net",
        "Referer": "https://kns.cnki.net/kns8/AdvSearch?dbcode=CFLS",
        "sec-ch-ua": '''"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"''',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "macOS",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    form_data = {
        "IsSearch": "true",
        "QueryJson": "{\"Platform\":\"\",\"DBCode\":\"CFLS\",\"KuaKuCode\":\"CJFQ,CCND,CIPD,CDMD,BDZK,CISD,SNAD,CCJD,GXDB_SECTION,CJFN,CCVD\",\"QNode\":{\"QGroup\":[{\"Key\":\"Subject\",\"Title\":\"\",\"Logic\":4,\"Items\":[],\"ChildItems\":[{\"Key\":\"input[data-tipid=gradetxt-1]\",\"Title\":\"基金\",\"Logic\":0,\"Items\":[{\"Key\":\"\",\"Title\":\"" + f"{fundId}" + f"\",\"Logic\":1,\"Name\":\"FU\",\"Operate\":\"=\",\"Value\":\"" + f"{fundId}" + "\",\"ExtendType\":1,\"ExtendValue\":\"中英文对照\",\"Value2\":\"\"}],\"ChildItems\":[]}]},{\"Key\":\"ControlGroup\",\"Title\":\"\",\"Logic\":1,\"Items\":[],\"ChildItems\":[]}]}}",
        "PageName": "DefaultResult",
        "DBCode": "SCDB",
        "KuaKuCodes": "CJFQ,CCND,CIPD,CDMD,BDZK,CISD,SNAD,CCJD,GXDB_SECTION,CJFN,CCVD",
        # "SearchSql": "0645419CC2F0B23BC604FFC82ADF67C6E920108EDAD48468E8156BA693E89F481391D6F5096D7FFF3585B29E8209A884EFDF8EF1B43B4C7232E120D4832CCC896D30C069E762ACAB990E5EBAAD03C09721B4573440249365A4157D3C93DC874963F6078A465F9A4E6BEED14E5FD119B250F0488206491CF1C7F670020480B48EE2FF3341B3B9C8A0A38F9913EF596174EDD44BBA8277DA2BE793C92DF83782297DE55F70BBF92D5397159D64D1D3DAC96FAD28213BD3E1912A5B4A4AD58E5965CBDBA01069691140F14FD0298FBD1F452C7779EFF17124633292E356C88367122976245AA928FA07D061C0E091BB1136031750CD76D7D64E9D75B7FBAB11CAA5B80183AC60BB0885D2C0A0938C7D1F849656014326473DCB797D5D273C845DAF7FCE49D21478E9B06B77ADE6253ACD4FE1D87EE31B4B2C94E071EE733B3A64EA6EE9CD5F222FCD3DA1D83D9133EF8C9BED9ED3E55DA15F3B4A37C85463B60D2F0BEA46FC7135898D7D93F63AF8B2246716E32B699238901588EE5D1DEF30A01DCE9957CF6934E8B11E273747F9A9BB8ADF535E5E76F6A9386CFBE605748C132DA05E2D31832199B0A4ECF170ACA47154423CF6BBD9607FC505765E95637F93DC865AA738F5EE92B26DB9AF56509A5FC96FF9C3A1720633EBDDC62EC2162E7D5349CAC851ED0AD4E36DCF6FE25EBEAB42BF931DBE3CF4ED1A7BB8FD887C3C33D86B768B0BA7267C4E0E7DEE53D0931F71F07AE13BAFC46034A444EC24C7EA8F0086FAD197A8D2F18C6CBC5DF48050AF8D4C84DE03B9A6F1DF928D63286B1C924B7EC3BA8C2591D60491F95D271F0E7F02AA2AA93C3888B8CCEBB0414BD7145AD15A3166DB4860F85BC476B1B193C219EAE52E33E6BBC9B3AAAD97196977B7DABA36C04093ED723AD874EC6480477C6412B0F589DE6CC7D959855E41265213DCBB4D91238716DF38BF78C951259572F8E5968FAC5C5CDC006DBE919EEB5E5518F51162FCE7CDE520F60093D333FBE121D3164C6D2451F6431FB7973C659E6A9D287B545EC044DE2CBE170F3627719F8418D44E17987CEC7A89B52CB5525AF795DA892475ABF871C3A5A5FCBC5B03EB9BEC8598C8ADD7A68984BBBEF1244DD90386C05756687AB9D87A0B521319C093C3EC0D5EBEFDAB5459E29F1DA03D4C25DE740BF9FA2BC07DD510386E3BBE89F10D45513E29C8CF904763E723CE4BF2928D4DC2A731DD53595E9AACED90679FCDDACED022ECD59D72600A736D555A8B76BFE4CCD861E6A7F5A219EBE9A228BD008928299DB999D18F9CDD2E57E8C03EDF236E62EDB17A1FE5B023CF6E5A11892A5FA17EE5CFE348CA290DC691987A535223133D8CA101E8ABF13EFCAD929635E090B3C6BB6838E33B7C78C1DBA274101A6584300EF8D38C983AD544264217F6793562D19715CD711295C5410C72E88A64BD23D9049E5DF15EA6B3EB4473C1DDEBB416459322FEF0CC61D894476DCD62569527BE23FB7F66DF3F5182ABF2472FB60039CA77218F356D7F82E4EBAAA4C6875B5BD4729C81A29BDF55ED223AA0DAB04E1B248524FC504711360C330186327A780D6487BA831ABE55AAE38E69A0FBEF89D560E7AA26B991966E4B644338863E80AD9D1ACAD459EA933644C5A0D2EA44AD17205AED3BE66AEC01F48BA032EEBD620E2713082FE8D31E4A05A34F18BD389587FA4D3A9DFBB8C16AEE9C5FA9E667BA12A07B757D82F7BB41AC8867D9947CCBA3BB26381EC6D0D3966338DB6FA3D1A61F99A978C3B5ED2B31B7C14D54A4F688C4925C8AF99CB3EE3C2C06C7D35AD891BF0CFC820529FD990F2FF319BE195B1AD23C1667031C072EB1964F8512BB779125E46773C01714FCF0E339AEB0C44FB91B896A7A95AF4F81EB49006B570BC03ECA7D8DA45679F3B46A7AE3B46ED8D319CED49A3A5881A37CD3770703BDF026ACEF7D8662F85AFDBDD36C540FD419E18F30EA0483D24350B7C34C43F3D0065F339EAC15749DF8849F3880378FEA4AD7CCBAA827C828A5CAF7D56E97A87A3FAEEAE136B35FB37E8CE0233D9AF8DEABD47BD5B36A1B42B995D4F96FE744A2E25E9B6107801CACCA0DDC2B7ED5BFD39F68AB2E2BB66AB8286061049F3B5FFE871FFA520A7C0EEE3DEDF417D078DF9013B5F525C84BE257C0E19D7818928D36ACF368B21B36FDA0541F68BEC55F16C4300222A4186510D6D60CC27081D6315297C056CA5E950694B13A35535329912B1947961CA16DAED1708E77040DCD6C57D2A5290760352E880AC682E33F6BC1FB4DC98DE0590C5F64054DDA83A03DEC4CF13327CE8486BE653E88364331E034C6C090AA3F73CC5B1BC018775DF40043E5DE1B6E96CE7054F6EE308127DAB0229252F58284A55B9C7AFA5F0A4717CC4F3D5F826381FBE4FA4F77AC75FFA6A98BA51989F485B0812B143ADFF7F2D5AF39C5379AF16D797C7255CBD0D2FC3612A80F6D9A33DDB106C4C85843B9ECD514ECD4AB760C4E007843660CD1813E3E7ECFC6D5141EDA6394CEFE74FF821A529CBF431CE81AF039A991B413927B68B3E0B22924C377D38BD301B559E31C4350920462839F217DE6DEE37B74A974EA231F9F966EB300BFE09B99FD9C6D6E9BA9B493C017D0ADCD18A7CDE3265511DE7BF7848A13AA9C464A8077A0F4F717C6CE96D66559649C348BD09D7E0AAEFB7FC6698660A7D80D82C0AF2101DEA7AE5FA3B7E15AA3F352E2E65136E01DEC871E46A15D1BF77C8703ABCF2A2AE3892BE9EB8125B56D254C30DBA828172B77ACAFD26427132E9CBF8B90F07C3B0660CC43F5BF7CAAEE5B6F9AB263B0E80527D1AC86665829870EAA8FAA00F1E70C19B84AFE67412D93807EFD164948F5AE5905C05B154DAFD77B85D1CCE3489C6E20A60D0519BA32744A7F75039A46E5738D9912E878B9CD6417B1D3363F03F4FD5B63683576D87F6BB81093FD8C01FB94CBDC2A",
        "CurPage": "1",
        "RecordsCntPerPage": "100",
        "CurDisplayMode": "listmode",
        "CurrSortField": "",
        "CurrSortFieldType": "desc",
        "IsSentenceSearch": "false",
        "Subject": ""
    }

    resp = requests.post(url, headers=headers, data=form_data)
    res = resp.text
    return res


# 获取论文json
def getPaperContent(res, fundId):
    soup = BeautifulSoup(res, 'lxml')
    if soup.find('p', class_='no-content'):
        return []

    name_td = soup.find_all('td', class_="name")
    author_td = soup.find_all('td', class_="author")
    source_td = soup.find_all('td', class_="source")
    date_td = soup.find_all('td', class_="date")
    data_td = soup.find_all('td', class_="data")
    operate_td = soup.find_all('td', class_="operat")

    name_list = getPaperNameList(name_td)
    author_list = getAuthorList(author_td)
    source_list = getSourceList(source_td)
    date_list = getDateList(date_td)
    data_list = getDataList(data_td)
    operate_list = getDownUrlList(operate_td)

    json_list = []
    for i in range(len(name_td)):
        paper_info = {"title": name_list[i],
                      "authors": author_list[i],
                      "source": source_list[i],
                      "date": date_list[i],
                      "data": data_list[i],
                      "operate_list": operate_list[i],
                      "fundId": fundId}
        paper_json = json.dumps(paper_info, ensure_ascii=False)
        json_list.append(paper_json)

    return json_list


# 返回当前页面所有的作者列表 字典形式对应作者：链接
def getAuthorList(author_td):
    author_list_all = []
    for item in author_td:
        author_list = []
        author_a = item.find_all('a', class_="KnowledgeNetLink")
        for author in author_a:
            author_link = author.get('href')
            author_info = {author.text: util.changeAuthor(author_link)}
            author_list.append(author_info)
        author_list_all.append(author_list)
    return author_list_all


# 返回当前页面所有的论文名
def getPaperNameList(name_td):
    paper_list_all = []
    for item in name_td:
        name_a = item.find('a', class_="fz14")
        # 消除引号对json格式文件的影响
        name_info = {item.text.replace('\n', '').replace('\r', '').replace('\"', '').strip(' '): util.changeUrl(
            name_a.get('href'))}
        paper_list_all.append(name_info)
    return paper_list_all


# 返回当前页面所有文献的来源
def getSourceList(source_td):
    source_list_all = []
    for item in source_td:
        source_a = item.find('a')
        source_info = {source_a.text: source_a.get('href')}
        source_list_all.append(source_info)
    return source_list_all


# 返回当前页面所有文献的发表时间
def getDateList(date_td):
    date_list_all = []
    for item in date_td:
        date_info = {"date": item.text.replace('\n', '').replace('\r', '').replace('\"', '').strip(' ')}
        date_list_all.append(date_info)
    return date_list_all


# 返回当前页面所有文献的文献类型
def getDataList(data_td):
    data_list_all = []
    for item in data_td:
        data_info = {"data": item.text.replace('\n', '').replace('\r', '').replace('\"', '').strip(' ')}
        data_list_all.append(data_info)
    return data_list_all


# 返回当前页面所有文献的下载链接
def getDownUrlList(operate_td):
    url_list_all = []
    for item in operate_td:
        url_a = item.find('a')
        url_info = {"downUrl": url_a.get('href')}
        url_list_all.append(url_info)
    return url_list_all


if __name__ == '__main__':
    for file in util.getAllDataPath():
        idList = util.getAllProjectId(file)
        for i in tqdm(range(len(idList)), desc=f'{file}'):
            projectId = idList[i]
            if projectId[0:1] == 'SQ':
                paper_json_list = getPaperContent(requestUrl(projectId), projectId)
                print(paper_json_list)
                if len(paper_json_list) == 0:
                    continue
                util.saveJson(projectId, paper_json_list)
                time.sleep(2)
            else:
                for j in range(0, 7):
                    paper_json_list = getPaperContent(requestUrl(projectId[:-1] + str(j)), projectId[:-1] + str(j))
                    print(paper_json_list)
                    if len(paper_json_list) == 0:
                        continue
                    util.saveJson(projectId[:-1] + str(j), paper_json_list)
                    time.sleep(2)

# for file in util.getAllDataPath():
#     idList = util.getAllProjectId(file)
#     for id in idList:
#         if id[0:1] == 'SQ':
#             res = requestUrl(id)
#         else:
#             for i in range(0, 7):
#                 res = requestUrl(id[:-1] + str(i))
