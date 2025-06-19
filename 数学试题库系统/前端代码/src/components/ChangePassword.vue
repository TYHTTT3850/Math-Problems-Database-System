<template>
    <div>
        <div class="header">修改密码</div>
        <div class="body">
            <el-form ref="formRef" :model="form" label-width="120px" id="selectForm" :rules="formRules">
                <el-form-item label="原密码：" prop="old_pwd">
                    <el-input v-model="form.old_pwd" type="password" show-password></el-input>
                </el-form-item>

                <el-form-item label="新密码：" prop="new_pwd">
                    <el-input v-model="form.new_pwd" type="password" show-password></el-input>
                </el-form-item>

                <el-form-item label="确认密码：" prop="check_pwd">
                    <el-input v-model="form.check_pwd" type="password" show-password></el-input>
                </el-form-item>

                <el-form-item style="text-align: center;">
                    <el-button type="primary" @click="changePassword">确定</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script lang="ts" setup>
import {ref} from "vue";
import axios from "axios";
import {ElMessage, ElForm} from "element-plus";

interface FormData {
    old_pwd: string;
    new_pwd: string;
    check_pwd: string;
}

const form = ref<FormData>({
    old_pwd: "",
    new_pwd: "",
    check_pwd: "",
});

const formRules = {
    old_pwd: [{required: true, message: "必填", trigger: "blur"}],
    new_pwd: [{required: true, message: "必填", trigger: "blur"}],
    check_pwd: [{required: true, message: "必填", trigger: "blur"}],
};

const formRef = ref<InstanceType<typeof ElForm> | null>(null);

const changePassword = () => {
    if (!formRef.value) return;

    formRef.value.validate((valid) => {
        if (!valid) return;

        // 检查新密码与确认密码
        if (form.value.check_pwd !== form.value.new_pwd) {
            ElMessage.error("新密码与确认密码不一致");
            // 清空表单数据
            form.value.old_pwd = "";
            form.value.new_pwd = "";
            form.value.check_pwd = "";
            return;
        }

        // 从本地存储中获取 token
        const token = localStorage.getItem('token');
        if (!token) {
            ElMessage.error("登录已过期，请重新登录");
            return;
        }

        // 将请求数据和 token 一同提交
        axios
                .post("http://127.0.0.1:5000/user/pwd_chg", form.value, {
                    headers: {
                        token: token,
                    },
                })
                .then((res) => {
                    if (res.data.status === 200) {
                        ElMessage.success(res.data.msg);
                    } else {
                        ElMessage.error(res.data.msg);
                    }
                })
                .catch((error) => {
                    console.error("修改密码失败:", error);
                    ElMessage.error("修改密码失败，请重试");
                })
                .finally(() => {
                    // 清空表单数据
                    form.value.old_pwd = "";
                    form.value.new_pwd = "";
                    form.value.check_pwd = "";
                });
    });
};
</script>

<style scoped>
.header {
    width: 100%;
    height: 10%;
    text-align: center;
    line-height: 64px;
    font-size: 20px;
    font-weight: 800;
    border-bottom: 1px solid #e3e3e3;
}

.body {
    width: 40%;
    margin-top: 30px;
    margin-left: 30px;
}

#selectForm ::v-deep(.el-form-item__label) {
    font-size: 18px;
}

span {
    font-size: 18px;
}
</style>
