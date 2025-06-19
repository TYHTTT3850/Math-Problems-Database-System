import axios from "axios";
import type {AxiosInstance, InternalAxiosRequestConfig} from "axios";

const http: AxiosInstance = axios.create({
    baseURL: "http://127.0.0.1:5000",
    timeout: 5000,
});

http.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        const token = localStorage.getItem("token");
        if (token) {
            if (!config.headers) {
                // 这里给headers赋空对象，但用any绕开类型检查
                (config.headers as any) = {};
            }
            // 直接用索引赋值，不用 .set()
            (config.headers as any)["token"] = token;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export default http;
