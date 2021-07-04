import * as JsSIP from "jssip";
import {SIP_SERVER_URL} from "../../serverCommunication/SIPServerUtils";
import * as actions from "../actions/phoneActions";


export const phoneIntialState = {
    socket:undefined,
    ua:undefined,
    inCall:false,
    incomingCall:false,
};

export default function phoneReducer(state = phoneIntialState, action) {
    switch (action.type){
        case actions.CONNECT_AND_REGISTER:
            localStorage. setItem('userId',action.payload);
            return {...state, userId:action.payload};
        case actions.SET_USERNAME:
            localStorage.setItem('username',action.payload);
            return {...state,username:action.payload};
        case actions.SET_IS_IN_CALL:
            localStorage.setItem('isInCall',action.payload);
            return {...state,isInCall:action.payload};
        default:
            return state
    }
}
// let socket = new JsSIP.WebSocketInterface(SIP_SERVER_URL);
// let configuration = {
//     sockets  : [ socket ],
//     uri      : 'sip:alice@example.com',
//     password : 'superpassword'
// };
// let ua = new JsSIP.UA(configuration);
//
// ua.start();












// //ua.register();
//
//
// // Register callbacks to desired call events
// let eventHandlers = {
//     'progress': function(e) {
//         console.log('call is in progress');
//     },
//     'failed': function(e) {
//         audioPlayer.stop('calling')
//         console.log('call failed with cause: '+ e.data.cause);
//     },
//     'ended': function(e) {
//         console.log('call ended with cause: '+ e.data.cause);
//     },
//     'confirmed': function(e) {
//         console.log('call confirmed');
//     }
// };
//
// let options = {
//     'eventHandlers'    : eventHandlers,
//     'mediaConstraints' : { 'audio': true, 'video': true }
// };