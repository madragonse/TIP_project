import * as JsSIP from "jssip";

const SIP_SERVER = {
    IP: '127.0.0.1',
    PORT: '5001',
    PROTOCOL:'ws'
}

export const SIP_SERVER_URL=SIP_SERVER.PROTOCOL+'://'+SIP_SERVER.IP+':'+SIP_SERVER.PORT;
export const SIP_DEBUGGING_MODE= true;
if(SIP_DEBUGGING_MODE) JsSIP.debug.enable('JsSIP:*');

export function getUri(userId,userIp){
    //short hash of userId
    return "alice@example.com"
}