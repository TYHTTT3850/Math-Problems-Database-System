from flask import Flask, jsonify, request
from sqlalchemy import text

from config import BaseConfig
from flask_sqlalchemy import SQLAlchemy
import auth
# from aliyunsms.sms_send import send_sms
import datetime
from redis import StrictRedis

# 创建redis对象
redis_store = StrictRedis(host=BaseConfig.REDIS_HOST, port=BaseConfig.REDIS_PORT, decode_responses=True)

# 跨域
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # 允许所有来源访问

# 添加配置数据库
app.config.from_object(BaseConfig)
# 初始化拓展,app到数据库的ORM映射
db = SQLAlchemy(app)

# 检查数据库连接是否成功
with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute(text("select 1"))
        # print(rs.fetchone())

# 定义问题模型，对应数据库中的 problems 表
class Problem(db.Model):
    __tablename__ = 'problems'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    tag = db.Column(db.String, nullable=False)
    Uploader = db.Column(db.String, nullable=False)
    Upload_time = db.Column(db.DateTime, nullable=False)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String, nullable=False, unique=True)  # 确保标签唯一

# 获取手机号
def get_token_phone(token):
    data = auth.decode_func(token)
    phone = data['telephone']
    return phone

# 获取用户名
def get_token_username(token):
    data = auth.decode_func(token)
    username = data.get("username")
    if username:
        return username
    # 如果没有 "username" 字段，可以选择返回默认值 "anonymous"
    return "anonymous"

@app.route("/")
def home():
    return jsonify({
        "message": "系统API服务器运行正常",
        "status": 200,
        "available_endpoints": [
            "/user/login (POST)",
            "/user/shop (GET)",
            "/user/addorder (POST)",
            "/manager/shop (GET/POST/DELETE)"
        ]
    })

# 添加一个简单的健康检查路由
@app.route("/health")
def health_check():
    return jsonify({"status": "OK", "timestamp": datetime.datetime.now().isoformat()})


# 用户登录
@app.route("/user/login", methods=["POST"])
def user_login():
    # print(request.json)
    userTelephone = request.json.get("userTelephone").strip()
    password = request.json.get("password").strip()
    sql = text('SELECT * FROM user WHERE telephone = :telephone AND password = :password')
    params = {'telephone': userTelephone, 'password': password}
    data = db.session.execute(sql, params).first()
    # print(data)
    if data is not None:
        user = {'id': data[0], 'username': data[1], 'telephone': data[2], 'password': data[3]}
        # 生成token
        token = auth.encode_func(user)
        # print(token)
        return jsonify({"code": 200, "msg": "登录成功", "token": token, "role": data[4]})
    else:
        return jsonify({"code": 1000, "msg": "用户名或密码错误"})


# 用户注册__发送验证码
# @app.route("/user/register/send_sms", methods=["POST"])
#
# def register_sms():
#     # print(request.json)
#     phone = request.json.get("telephone")
#     # print(str(phone))
#     # params = {'code': '756821'}  # abcd就是发发送的验证码，code就是模板中定义的变量
#     # print(params)
#     # 生成随机的6位验证码
#     num = random.randrange(100000, 999999)
#     params = {'code': 123456}
#     params['code'] = num
#
#     # 将验证码保存到redis中，第一个参数是key，第二个参数是value，第三个参数表示60秒后过期
#     redis_store.set('valid_code:{}'.format(phone), num, 600)
#     print(redis_store.get('valid_code:{}'.format(phone)))
#     # 调用send_sms函数来发送短信验证码
#     result = send_sms(str(phone), json.dumps(params))
#     print(result)
#     if result[3]:
#         return jsonify({"code": "200", "msg": "验证码发送成功"})
#     else:
#         return jsonify({"code": '1000', "msg": "验证码发送失败"})

# @app.route("/user/findback", methods=["POST"])
# def findback():
#     rq = request.json
#     # 获取验证码和手机号
#     password = rq.get("password")
#     vercode = rq.get("vercode")
#     telephone = rq.get("telephone")
#
#     if vercode != redis_store.get('valid_code:{}'.format(telephone)):
#         return jsonify({"status": "1000", "msg": "验证码错误"})


# 用户注册__检测验证码和手机是否在数据库中
# @app.route("/user/register/test", methods=["POST"])
#
# def register_test():
#     rq = request.json
#     # 获取验证码和手机号
#     username = rq.get("username")
#     password = rq.get("password")
#     vercode = rq.get("vercode")
#     telephone = rq.get("telephone")
#
#     # 先判断验证码对错
#     if vercode != redis_store.get('valid_code:{}'.format(telephone)):
#         return jsonify({"status": "1000", "msg": "验证码错误"})
#
#     data = db.session.execute(text('select * from user where telephone="%s"' % telephone)).fetchall()
#     if not data:
#         db.session.execute(text('insert into user(username,password,telephone,role) value("%s","%s","%s",0)' % (
#             username, password, telephone)))
#         db.session.commit()
#         return jsonify({"status": "200", "msg": "注册成功"})
#     else:
#         return jsonify({"status": "1000", "msg": "该用户已存在"})


# 获取用户信息
@app.route("/user/usermsg", methods=["GET"])
def usermsg():
    telephone = get_token_phone(request.headers.get('token'))
    query = text('SELECT username, telephone FROM user WHERE telephone=:telephone')
    result = db.session.execute(query, {'telephone': telephone}).fetchone()

    if result:
            data = dict(username=result.username, telephone=result.telephone)
            return jsonify(status=200, data=data)
    else:
        return jsonify(status=404, message="User not found")


# 更改密码
@app.route("/user/pwd_chg", methods=["POST"])
def user_pwd_chg():
    try:
        data = request.get_json()
        new_pwd = data.get('new_pwd')
        old_pwd = data.get('old_pwd')
        token = request.headers.get('token')
        if not token:
            return jsonify(status=400, msg='缺少 token'), 400

        phone = get_token_phone(token)

        # 参数化查询，避免使用字符串拼接
        query = text('SELECT * FROM user WHERE telephone=:phone AND password=:old_pwd')
        user_data = db.session.execute(query, {"phone": phone, "old_pwd": old_pwd}).fetchall()
        if not user_data:
            return jsonify(status=1000, msg="原始密码错误")
        else:
            update_query = text('UPDATE user SET password=:new_pwd WHERE telephone=:phone')
            db.session.execute(update_query, {"new_pwd": new_pwd, "phone": phone})
            db.session.commit()
            return jsonify(status=200, msg="修改成功")
    except Exception as e:
        db.session.rollback()
        print("Error in user_pwd_chg:", e)
        return jsonify(status=500, msg=str(e)), 500


# 获取题目接口，从数据库中查询 problems 表
@app.route("/api/problems", methods=["GET"])
def get_problems():
    try:
        sql = text("SELECT id, content, tag, Uploader, Upload_time FROM problems")
        result = db.session.execute(sql).fetchall()
        problems = []
        for row in result:
            problems.append({
                'id': row[0],
                'content': row[1],
                'tag': row[2],
                'Uploader': row[3],
                'Upload_time': row[4].strftime('%Y-%m-%d %H:%M:%S') if row[4] else None
            })
        return jsonify({"status": 200, "data": problems})
    except Exception as e:
        return jsonify({"status": 500, "msg": str(e)})


# 上传题目接口（POST 方法），用于写入题目数据到 problems 表中
@app.route("/api/problems", methods=["POST"])
def add_problem():
    data = request.get_json()
    if not data:
        return jsonify({"status": 400, "message": "No input data provided"}), 400

    content = data.get("content")
    tag = data.get("tag", "无标签")
    Uploader = data.get("Uploader", "anonymous")
    Upload_time_str = data.get("Upload_time")

    # 检查必要字段
    if not content:
        return jsonify({"status": 400, "message": "内容不能为空"}), 400
    if not Upload_time_str:
        return jsonify({"status": 400, "message": "Upload_time 不能为空"}), 400

    # 将上传时间字符串转换为 datetime 对象
    try:
        Upload_time = datetime.datetime.fromisoformat(Upload_time_str)
    except Exception as e:
        return jsonify({"status": 400, "message": f"Upload_time 格式错误: {str(e)}"}), 400

    # 查询当前表中的最大 id
    try:
        result = db.session.execute(text("SELECT MAX(id) FROM problems")).fetchone()
        max_id = result[0] if result[0] is not None else 0
    except Exception as e:
        return jsonify({"status": 500, "message": f"查询最大ID失败: {str(e)}"}), 500

    new_id = max_id + 1

    # 通过请求头中的 token 来获取当前登录用户的用户名
    token = request.headers.get("token")
    username = get_token_username(token)  # 保证这里获取的是正确的用户名

    # 创建新的题目记录时，手动指定 id
    new_problem = Problem(
        id=new_id,
        content=content,
        tag=tag,
        Uploader=username,
        Upload_time=Upload_time
    )

    try:
        db.session.add(new_problem)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": 500, "message": f"写入数据库出错: {str(e)}"}), 500

    return jsonify({
        "status": 200,
        "message": "题目上传成功",
        "id": new_problem.id
    }), 200


# 获取所有标签
@app.route("/api/tags", methods=["GET"])
def get_tags():
    try:
        sql = text("SELECT id, tag_name FROM tags")
        result = db.session.execute(sql).fetchall()
        tag_list = [{"id": row[0], "tag_name": row[1]} for row in result]
        return jsonify({"status": 200, "data": tag_list})
    except Exception as e:
        return jsonify({"status": 500, "msg": str(e)})

# 添加新标签
# @app.route("/api/tags", methods=["POST"])
# def add_tag():
#     data = request.get_json()
#     tag_name = data.get("tag_name")
#
#     if not tag_name:
#         return jsonify({"status": 400, "message": "标签名称不能为空"}), 400
#
#     # 检查标签是否已存在
#     existing_tag = db.session.execute(text("SELECT id FROM tags WHERE tag_name = :tag_name"),
#                                       {"tag_name": tag_name}).fetchone()
#     if existing_tag:
#         return jsonify({"status": 400, "message": "标签已存在"}), 400
#
#     # 插入新标签
#     try:
#         new_tag = Tag(tag_name=tag_name)
#         db.session.add(new_tag)
#         db.session.commit()
#         return jsonify({"status": 200, "message": "标签添加成功", "id": new_tag.id})
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"status": 500, "message": f"数据库错误: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
    # 开启了debug模式
