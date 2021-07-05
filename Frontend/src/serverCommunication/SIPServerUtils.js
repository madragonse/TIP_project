import * as JsSIP from "jssip";
import {sha256} from "js-sha256";

const SIP_SERVER = {
    IP: '127.0.0.1',
    PORT: '5001',
    PROTOCOL:'ws'
}

export const SIP_SERVER_URL=SIP_SERVER.PROTOCOL+'://'+SIP_SERVER.IP+':'+SIP_SERVER.PORT;
export const SIP_DEBUGGING_MODE= true;
if(SIP_DEBUGGING_MODE) JsSIP.debug.enable('JsSIP:*');

//in seconds
export const SIP_MAX_INVITE_WAIT_TIME=20


export function getUri(userId){
    //short hash of userId
    let userHash= sha256(userId.toString()).substr(0,7);
    return "sip:"+userHash+"@"+SIP_SERVER.IP
}