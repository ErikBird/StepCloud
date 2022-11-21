import axios from 'axios';

export const gateway_api = {
    async getGatewayConfig(addr) {
        return axios.get(`http://${addr}/api/v1/auth/config`)
    },
    async postAuthToken(addr, data) {
        return axios.post(`http://${addr}/api/v1/auth/token`, data);
    },
    async postConfigureDevice(addr, gateway_id, device_type) {
        return axios.post(`http://${addr}/api/v1/interface/${gateway_id}/serve/${device_type}`)
    },
    async getMyDevices(addr) {
        return axios.get(`http://${addr}/interface/all`);
    },
    async getDiscoverInterfaces(addr) {
        return axios.get(`http://${addr}/api/v1/interface/discovery/all`);
    },
    async getManualInterfaces(addr) {
        return axios.get(`http://${addr}/api/v1/interface/manual/all`);
    },
    async getErrorLog(addr) {
        return axios.get(`http://${addr}/api/v1/log/error`);
    },
    async activateDevice(addr, device_name) {
        return axios.post(`http://${addr}/interface/activate/${device_name}`);
    },
    async introductInterfaceByIP(addr, interface_name, network_ip) {
        return axios.post(`http://${addr}/api/v1/interface/introduce/${interface_name}/${network_ip}`);
    }
};

