import {sha256} from "js-sha256";
import {API_URL, FETCH_DEBUGGING_MODE, fetchWithTimeout, handleResponse} from "./APIUtils";

export async function getFriends(userId,status,page,pageLength){
    try {
        const requestOptions = {
            method: 'GET',
            mode: 'cors',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
        };

        let path='/friends/'+userId+"/"+status+"/"+page+"-"+pageLength;
        const response = await fetchWithTimeout(API_URL + path, requestOptions);
        const respObj = await handleResponse(response);

        if (FETCH_DEBUGGING_MODE)  console.log(respObj);
        return respObj;
    } catch (error) {
        console.log(error);
        console.log(error.name === 'AbortError');
        return {error: 'Network connection error'};
    }
}

export async function modifyFriendship(userId,friendName,action){
    try {
        const requestOptions = {
            method: 'POST',
            mode: 'cors',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
        };

        let path='/friend/'+action+'/'+userId+'/'+friendName;
        const response = await fetchWithTimeout(API_URL + path, requestOptions);
        const respObj = await handleResponse(response);

        if (FETCH_DEBUGGING_MODE)  console.log(respObj);
        return respObj;
    } catch (error) {
        console.log(error);
        console.log(error.name === 'AbortError');
        return {error: 'Network connection error'};
    }
}