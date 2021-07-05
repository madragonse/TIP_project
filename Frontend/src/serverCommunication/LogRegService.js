import {sha256} from "js-sha256";
import {API_URL,handleResponse, fetchWithTimeout, FETCH_DEBUGGING_MODE} from "./APIUtils"
import {store} from "../App";

export async function login(username,password){

    try {
        let hashedPassword=sha256(password);
        const requestOptions = {
            method: 'POST',
            mode: 'cors',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ username, hashedPassword })
        };

        const response = await fetchWithTimeout(API_URL + '/user/login', requestOptions);
        const respObj = await handleResponse(response);

        if (FETCH_DEBUGGING_MODE)  console.log(respObj);
        return respObj;
    } catch (error) {
        console.log(error);
        console.log(error.name === 'AbortError');
        return {error: 'Network connection error'};
    }
}

export async function register(username,password,email){
    try {
        let hashedPassword=sha256(password);
        const requestOptions = {
            method: 'POST',
            mode: 'cors',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({username,hashedPassword,email})
        };

        const response = await fetchWithTimeout(API_URL + '/user/register', requestOptions);
        const respObj = await handleResponse(response);
        if (FETCH_DEBUGGING_MODE)  console.log(respObj);
        return respObj;
    } catch (error) {
        console.log(error.name === 'AbortError');
        return {error: 'Network connection error'};
    }
}

export async function logout(){
    const storeState=store.getState();
    let userId=storeState.user.userId;

    if(userId===undefined){
        localStorage.clear();
        sessionStorage.clear();
        window.location.reload(true);
        return;
    }

    try {
        const requestOptions = {
            method: 'GET',
            mode: 'cors',
        };

        const response = await fetchWithTimeout(API_URL + '/user/logout?userId='+userId, requestOptions);
        const respBody= await response.text();
        const respObj = JSON.parse(respBody);
        if (FETCH_DEBUGGING_MODE) console.log(respObj);
    } catch (error) {
        console.log(error);
    }

    localStorage.clear();
    sessionStorage.clear();
    window.location.reload(true); //reload to reroute to loginpage
}





