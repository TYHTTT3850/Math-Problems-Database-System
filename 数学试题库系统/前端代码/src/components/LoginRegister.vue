<template>
    <div class="container">
        <div class="login_box" v-if="target === 1">
            <div class="head">登录</div>
            <el-form
                    :model="loginForm"
                    :rules="loginRules"
                    ref="loginFormRef"
                    label-width="0"
                    class="login_form"
            >
                <el-form-item prop="userTelephone" style="margin-left: 10px;margin-right: 10px">
                    <el-input v-model="loginForm.userTelephone" spellcheck="false" placeholder="手机号"/>
                </el-form-item>
                <el-form-item prop="password" style="margin-left: 10px;margin-right: 10px">
                    <el-input
                            v-model="loginForm.password"
                            show-password
                            spellcheck="false"
                            placeholder="密码"
                    />
                </el-form-item>
                <el-form-item class="btns">
                    <el-button type="primary" @click="llogin">登录</el-button>
                </el-form-item>
            </el-form>
            <div class="operate">
                <span id="op1" @click="change(2)">注册</span>
                <span id="op2" @click="change(3)">忘记密码</span>
            </div>
        </div>

        <div class="reg_box" v-if="target === 2">
            <div class="head">注册</div>
            <el-form :model="regForm" :rules="regRules" ref="regFormRef" class="reg_form">
                <el-form-item prop="username" style="margin-left: 10px;margin-right: 10px">
                    <el-input v-model="regForm.username" spellcheck="false" placeholder="用户名">
                        <template #prefix>
                            <i class="iconfont icon-user"/>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="password" style="margin-left: 10px;margin-right: 10px">
                    <el-input v-model="regForm.password" show-password spellcheck="false"
                              placeholder="密码(包含大小写字母、数字，长度在6-12之间)">
                        <template #prefix>
                            <i class="iconfont icon-password"/>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="telephone" style="margin-left: 10px;margin-right: 10px">
                    <el-input v-model="regForm.telephone" spellcheck="false" placeholder="手机号码">
                        <template #prefix>
                            <i class="iconfont icon-password"/>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="verifyCode" style="margin-left: 10px;margin-right: 10px">
                    <el-input
                            v-model="regForm.verifyCode"
                            spellcheck="false"
                            placeholder="验证码"
                            style="width:230px"
                    />
                    <span
                            style="width:120px;font-size:16px;cursor:pointer;margin-left: 10px;margin-right: 10px"
                            v-if="getcodeShow"
                            @click="sendVerifyCodePre"
                    >
                      获取验证码
                    </span>
                    <span style="width:120px;font-size:16px;cursor:pointer" v-else>
                      {{ timeCount }}s后重新获取
                    </span>
                </el-form-item>
                <el-form-item class="btns">
                    <el-button type="primary" @click="register">注册</el-button>
                </el-form-item>
            </el-form>
            <div>
                <span
                        @click="change(1)"
                        style="margin-left:210px;color:#000;opacity:0.5;font-weight:400;font-size:16px;cursor:pointer"
                >登录</span>
            </div>
        </div>

        <div class="forget_box" v-if="target === 3">
            <div class="head">忘记密码</div>
            <el-form :model="findBackForm" :rules="findBackRules" ref="findBackFormRef" class="reg_form">
                <el-form-item prop="userTelephone" style="margin-left: 10px;margin-right: 10px">
                    <el-input v-model="findBackForm.userTelephone" spellcheck="false" placeholder="手机号码">
                        <template #prefix>
                            <i class="iconfont icon-password"/>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="password" style="margin-left: 10px;margin-right: 10px">
                    <el-input v-model="findBackForm.password" show-password spellcheck="false" placeholder="新密码">
                        <template #prefix>
                            <i class="iconfont icon-password"/>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="verifyCode" style="margin-left: 10px;margin-right: 10px">
                    <el-input
                            v-model="findBackForm.verifyCode"
                            spellcheck="false"
                            placeholder="验证码"
                            style="width:230px"
                    />
                    <span
                            style="width:120px;font-size:16px;cursor:pointer;margin-left: 10px;margin-right: 10px"
                            v-if="getcodeShow"
                            @click="sendVerifyCodePre"
                    >
                      获取验证码
                    </span>
                    <span style="width:120px;font-size:16px;cursor:pointer" v-else>
                      {{ timeCount }}s后重新获取
                    </span>
                </el-form-item>
                <el-form-item class="btns">
                    <el-button type="primary" @click="findBack">确认修改</el-button>
                </el-form-item>
            </el-form>
            <div>
                <span
                        @click="change(1)"
                        style="margin-left:210px;color:#000;opacity:0.5;font-weight:400;font-size:16px;cursor:pointer"
                >登录</span>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import {ref, reactive} from 'vue';
import { useRouter } from 'vue-router';
import {ElMessage} from 'element-plus';
import type {FormInstance} from 'element-plus';
import axios from 'axios';

const router = useRouter();
const target = ref(1);
const getcodeShow = ref(true);
const timeCount = ref(0);
let timer: number | undefined;

const loginForm = reactive({
    userTelephone: '',
    password: '',
});
const regForm = reactive({
    username: '',
    password: '',
    telephone: '',
    verifyCode: '',
});
const findBackForm = reactive({
    userTelephone: '',
    password: '',
    verifyCode: '',
});

const loginFormRef = ref<FormInstance>();
const regFormRef = ref<FormInstance>();
const findBackFormRef = ref<FormInstance>();

const checkPassword = (_rule: any, value: string, callback: (error?: Error) => void) => {
    const regPassword = /(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{6,12}$/;
    if (regPassword.test(value)) {
        callback();
    } else {
        callback(new Error('包含大写字母、小写字母、数字，长度在6-12位之间'));
    }
};

const checkMobile = (_rule: any, value: string, callback: (error?: Error) => void) => {
    const regMobile = /^(0|86|17951)?(13[0-9]|15[0-35-9]|17[0-8]|18[0-9]|14[5-7]|19[0-9])[0-9]{8}$/;
    if (regMobile.test(value)) {
        callback();
    } else {
        callback(new Error('手机号码格式不正确'));
    }
};

const loginRules = {
    userTelephone: [
        {required: true, message: '请输入电话', trigger: 'blur'},
        {validator: checkMobile, trigger: 'blur'},
    ],
    password: [{required: true, message: '请输入密码', trigger: 'blur'}],
};

const regRules = {
    username: [{required: true, message: '请设置用户名', trigger: 'blur'}],
    password: [
        {required: true, message: '请设置密码', trigger: 'blur'},
        {validator: checkPassword, trigger: 'blur'},
    ],
    telephone: [
        {required: true, message: '请绑定手机号', trigger: 'blur'},
        {validator: checkMobile, trigger: 'blur'},
    ],
};

const findBackRules = {
    userTelephone: [
        {required: true, message: '请输入电话', trigger: 'blur'},
        {validator: checkMobile, trigger: 'blur'},
    ],
    password: [{required: true, message: '请输入密码', trigger: 'blur'}],
};

function change(id: number) {
    // console.log("切换页面，目标为：", id);
    target.value = id;
}

function startTimer() {
    if (timer) return;
    const TIME_COUNT = 60;
    timeCount.value = TIME_COUNT;
    getcodeShow.value = false;
    timer = window.setInterval(() => {
        if (timeCount.value > 0) {
            timeCount.value--;
        } else {
            getcodeShow.value = true;
            clearInterval(timer);
            timer = undefined;
        }
    }, 1000);
}

function sendVerifyCodePre() {
    if (target.value === 2) {
        regFormRef.value?.validate((valid) => {
            if (valid) {
                sendVerifyCode();
            }
        });
    } else if (target.value === 3) {
        findBackFormRef.value?.validate((valid) => {
            if (valid) {
                sendVerifyCode();
            }
        });
    }
}

function sendVerifyCode() {
    let phone = '';
    if (target.value === 2) phone = regForm.telephone;
    else if (target.value === 3) phone = findBackForm.userTelephone;

    axios
            .post('http://127.0.0.1:5000/user/register/send_sms', {telephone: phone})
            .then(() => {
                ElMessage.success('验证码发送成功');
                startTimer();
            })
            .catch(() => {
                ElMessage.error('验证码发送失败');
            });
}

function llogin() {
    loginFormRef.value?.validate((valid) => {
        if (valid) {
            login();
        }
    });
}

function login() {
    axios
            .post('http://127.0.0.1:5000/user/login', loginForm)
            .then((res) => {
                if (res.data.code !== 200) {
                    ElMessage.error(res.data.msg);
                    return;
                }
                ElMessage.success('登录成功');
                window.localStorage.setItem('token', res.data.token);
                if (res.data.role === 0) {
                    router.push('/user');
                } else {
                    router.push('/manage');
                }
            })
            .catch(() => {
                ElMessage.error('网络故障');
            });
}

function register() {
    regFormRef.value?.validate((valid) => {
        if (!valid) return;
        if (!regForm.verifyCode) return;
        axios
                .post('http://127.0.0.1:5000/user/register/test', {
                    username: regForm.username,
                    password: regForm.password,
                    verifyCode: regForm.verifyCode,
                    telephone: regForm.telephone,
                })
                .then((res) => {
                    if (res.data.status === 200) {
                        ElMessage.success('注册成功');
                        change(1);
                    } else {
                        ElMessage.error(res.data.msg);
                    }
                });
    });
}

function findBack() {
    findBackFormRef.value?.validate((valid) => {
        if (!valid) return;
        if (!findBackForm.verifyCode) return;
        // 请求修改密码接口
        // 示例请求
        axios
                .post('http://127.0.0.1:5000/user/findBack', {
                    telephone: findBackForm.userTelephone,
                    password: findBackForm.password,
                    verifyCode: findBackForm.verifyCode,
                })
                .then((res) => {
                    if (res.data.status === 200) {
                        ElMessage.success('密码修改成功');
                        change(1);
                    } else {
                        ElMessage.error(res.data.msg);
                    }
                })
                .catch(() => {
                    ElMessage.error('网络错误');
                });
    });
}
</script>

<style lang="less" scoped>
.container {
    background-image: url('../assets/background_image.png'); /* 替换为你的图片路径 */
    background-size: cover;       /* 图片覆盖整个容器 */
    background-position: center;  /* 图片居中显示 */
    height: 100vh;
    width: 100vw;
    position: relative;
}

.head {
    text-align: center;
    height: 50px;
    line-height: 50px;
    font-size: larger;
    font-weight: 600;
    color: #333;
}

.login_box,
.reg_box,
.forget_box {
    width: 450px;
    background-color: white;
    border-radius: 3px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 30px 0 40px 0;
    box-sizing: border-box;
    box-shadow: 0 4px 12px rgb(0 0 0 / 0.1);
}

.login_box {
    height: 300px;
}

.reg_box {
    height: 400px;
}

.forget_box {
    height: 350px;
}

/* 按钮容器居中 */
.btns {
    text-align: center !important;
    margin: 20px 0 0 0 !important;
}

.btns :deep(.el-form-item__content) {
    justify-content: center !important;
}

/* 按钮样式 */
.el-button {
    width: 120px;
    min-width: 120px;
    padding: 8px 30px;
}

/* 底部切换操作 */
.operate {
    text-align: center;
    color: #000;
    opacity: 0.5;
    font-weight: 400;
    font-size: 16px;
    margin-top: 10px;
    user-select: none;
}

#op1 {
    padding: 0 15px 0 0;
    border-right: 1px solid #bdb9b9;
    cursor: pointer;
}

#op2 {
    padding: 0 0 0 15px;
    cursor: pointer;
}
</style>