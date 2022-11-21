import axios from 'axios';
import {serverUrl} from '@/env';

function authHeaders(token) {
    return {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    };
}

export const api = {
    async logInGetToken(username, password) {
        const params = new URLSearchParams();
        params.append('username', username);
        params.append('password', password);

        return axios.post(`${serverUrl}/api/v1/login/access-token`, params);
    },
    async getMe(token) {
        return axios.get(`${serverUrl}/api/v1/users/me`, authHeaders(token));
    },
    async updateMe(token, data) {
        return axios.put(`${serverUrl}/api/v1/users/me`, data, authHeaders(token));
    },
    async getUsers(token) {
        return axios.get(`${serverUrl}/api/v1/users/`, authHeaders(token));
    },
    async updateUser(token, userId, data) {
        return axios.put(`${serverUrl}/api/v1/users/${userId}`, data, authHeaders(token));
    },
    async createUser(token, data) {
        return axios.post(`${serverUrl}/api/v1/users/`, data, authHeaders(token));
    },
    async passwordRecovery(email) {
        return axios.post(`${serverUrl}/api/v1/password-recovery/${email}`);
    },
    async resetPassword(password, token) {
        return axios.post(`${serverUrl}/api/v1/reset-password/`, {
            new_password: password,
            token,
        });
    },
    async getCustomers(token) {
        return axios.get(`${serverUrl}/api/v1/customers/`, authHeaders(token));
    },
    async createCustomers(token, data) {
        console.log(data)
        return axios.post(`${serverUrl}/api/v1/customers/`, data, authHeaders(token));
    },
    async getDevices(token) {
        return axios.get(`${serverUrl}/api/v1/devices/`, authHeaders(token));
    },
    async createDevices(token, data) {
        console.log(data)
        return axios.post(`${serverUrl}/api/v1/devices/`, data, authHeaders(token));
    },
    async getDeviceSupplier(token) {
        return axios.get(`${serverUrl}/api/v1/deviceSuppliers/`, authHeaders(token));
    },
    async createDeviceSupplier(token, data) {
        console.log(data)
        return axios.post(`${serverUrl}/api/v1/deviceSuppliers/`, data, authHeaders(token));
    },
    async getDeviceCustomers(token, customer_id) {
        return axios.get(`${serverUrl}/api/v1/deviceCustomers/${customer_id}`, authHeaders(token))
    }
};