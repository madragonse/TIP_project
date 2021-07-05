import {logout} from "./LogRegService"

const API = {
    IP: '127.0.0.1',
    PORT: '5000',
}
//no backtick at the end
export const API_URL='http://'+API.IP+':'+API.PORT;
export const FETCH_DEBUGGING_MODE= true;

//prevent network_errors from crashing fetch requests
export async function fetchWithTimeout(resource, options) {
    const {timeout = 8000} = options;

    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);

    const response = await fetch(resource, {
        ...options,
        signal: controller.signal
    });
    clearTimeout(id);

    if( response===false || response ===undefined){
        return {error: 'Network connection error'};
    }
    return response;
}

export function handleResponse(response) {
    if(response.status ===401) logout();

    return response.text().then(text => {
        const data = text && JSON.parse(text);
        return data;
    });
}



