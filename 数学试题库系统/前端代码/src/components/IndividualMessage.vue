<template>
    <div>
        <div class="header">个人信息</div>
        <div class="body">
            <el-form ref="formRef" :model="form" label-width="120px" id="selectForm">
                <el-form-item label="用户名：">
                    <span>{{ form.username }}</span>
                </el-form-item>
                <el-form-item label="电话：">
                    <span>{{ form.telephone }}</span>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { reactive, onMounted } from 'vue';
import axios from "axios";

interface UserInfo {
    telephone: string;
    username: string;
}

const form = reactive<UserInfo>({
    telephone: "",
    username: "",
});

const getData = async () => {
    try {
        const token = localStorage.getItem("token") || "";  // 或者从其他地方获取token
        const res = await axios.get("http://127.0.0.1:5000/user/usermsg", {
            headers: {
                token: token,
            }
        });
        if (res.data.status === 200) {
            Object.assign(form, res.data.data);
        }
    } catch (error) {
        console.error("获取个人信息失败", error);
    }
};

onMounted(() => {
    getData();
});

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
