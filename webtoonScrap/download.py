import requests
import shutil

'''
긁어왔던 링크들을 한줄씩 읽어서 다운받는 스크립트.
링크하나당 컷 하나라 보고, 링크 갯수만큼 for문을 돌린다.
이미지 이름을 지정해주고 돌리면 콘솔창에서 진행도를 확인할 수 있다.
'''

with open("srclist.txt",'r') as f:
    count = 1
    for i in range(1,1493):
        line = f.readline()
        r = requests.get('%s' % line, stream=True )
        with open("./남과여/남과여-" + str(count) + ".jpg", 'wb') as g:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, g)
            count += 1
        print('done...' + str(count))
