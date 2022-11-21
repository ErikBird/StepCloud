import axios from 'axios';
import {apiUrl} from '@/env';

function authHeaders(token) {
    return {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    };
}

export const server_api = {
    /**
     * LOGIN
     */
    async logInGetToken(username, password) {
        const params = new URLSearchParams();
        params.append('username', username);
        params.append('password', password);
        return axios.post(`${apiUrl}/api/v1/login/access-token`, params);
    },
    async passwordRecovery(email) {
        return axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
    },
    /**
     * USER
     */
    async getMe(token) {
        return axios.get(`${apiUrl}/api/v1/customers/users/me`, authHeaders(token));
    },
    async updateMe(token, data) {
        return axios.put(`${apiUrl}/api/v1/customers/users/me`, data, authHeaders(token));
    },
    /**
     * DEVICE
     */
    async getDevices(token) {
        return axios.get(`${apiUrl}/api/v1/devices/`, authHeaders(token));
    },
    async getDeviceSupplier(token) {
        return axios.get(`${apiUrl}/api/v1/devices/suppliers/`, authHeaders(token));
    },
    /**
     * CUSTOMER DEVICE
     */
    async getCustomerDevicesMe(token) {
        return axios.get(`${apiUrl}/api/v1/customers/devices/me`, authHeaders(token));
    },
    async createCustomerDeviceMe(token, data) {
        return axios.post(`${apiUrl}/api/v1/customers/devices/me`, data, authHeaders(token));
    },
    async updateCustomerDevice(token, device_customer_id, data) {
        return axios.put(`${apiUrl}/api/v1/customers/devices/${device_customer_id}`, data, authHeaders(token));
    },
    /**
     * DEVICE EVENT
     */
    async createDeviceEvent(token, data) {
        return axios.post(`${apiUrl}/api/v1/customers/devices/event`, data, authHeaders(token));
    },
    async getDeviceEvents(token, customer_device_id) {
        return axios.get(`${apiUrl}/api/v1/customers/devices/${customer_device_id}/events`, authHeaders(token));
    },
    async getDeviceEventLast(token, customer_device_id) {
        return axios.get(`${apiUrl}/api/v1/customers/devices/${customer_device_id}/events/last`, authHeaders(token));
    },
    async getDeviceEvent(token, customer_device_id, event_id) {
        return axios.get(`${apiUrl}/api/v1/customers/devices/${customer_device_id}/events/${event_id}`, authHeaders(token));
    },
    /**
     * GATEWAY
     */
    async createGateway(token, data) {
        return axios.post(`${apiUrl}/api/v1/gateway/create`, data, authHeaders(token));
    },
};
