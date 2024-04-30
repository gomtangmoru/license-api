from flask import Flask, request, jsonify
import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()

app = Flask(__name__)

def db_search(search, value):
    print(value)
    if type(value) == str:
        c.execute(f'SELECT COUNT(*) FROM license WHERE {search} =  "{value}"')
    elif type(value) == int:
        c.execute(f'SELECT COUNT(*) FROM license WHERE {search} =  {value}')
    else:
        return False
    result = c.fetchone() 
    print(result)
    if result[0] > 0:
        return True
    else:
        return False
        
    

@app.route('/license', methods=['POST'])
def license():
    try:
        try:
            data = request.get_json()
        except:
            return jsonify({'result': 'fail', 'msg': '잘못된 요청입니다. (JSON 형식이 아님)'})
        print(data)
        try:
            privatekey_value = data['privatekey']
            type_value = data['type']
            name_value = data['name']
            print(privatekey_value, type_value, name_value)
            print("[ private key debug] : ", privatekey_value)
        except:
            return jsonify({'result': 'fail', 'msg': '잘못된 요청입니다. (필수 요소가 없음)'})
        if db_search('privatekey', privatekey_value) == False:
            return jsonify({'result': 'fail', 'msg': '라이선스가 존재하지 않습니다.'})
        if db_search('type', type_value) == False:
            return jsonify({'result': 'fail', 'msg': '라이선스 유효성 검증에 실패하였습니다.'})
        if db_search('name', name_value) == False:
            return jsonify({'result': 'fail', 'msg': '라이선스 유효성 검증에 실패하였습니다.'})
        return jsonify({'result': 'success', 'msg': '라이선스가 검증되었습니다.'})
    except:
        return jsonify({'result': 'fail', 'msg': '알 수 없는 오류가 발생하였습니다. 관리자에게 문의해주세요.'})



if __name__ == '__main__':
    app.run(port=8080, debug=True)
