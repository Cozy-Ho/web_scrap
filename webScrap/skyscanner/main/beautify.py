
'''
'search.py'로 긁어온 데이터들을 이쁘게 정리하는 파일.
2번씩 긁힌 가격 데이터의 중복을 제거하여 'setted_data_1.txt' 와 'setted_data_2.txt'로 저장한다.
'''


# 중복제거 함수
def remove_duplicates(li):
    my_set = set()
    res = []
    for e in li:
        if e not in my_set:
            res.append(e)
            my_set.add(e)
    return res


result_1 = open("result_2.txt","r")

set_data = result_1.read().split("\n")

setted_data = remove_duplicates(set_data)

setdata = open('setted_data_2.txt','w')

for i in setted_data:
    setdata.write(i+"\n")

setdata.close()
