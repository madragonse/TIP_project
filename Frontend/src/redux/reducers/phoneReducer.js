import * as JsSIP from "jssip";
import {getUri, SIP_SERVER_URL} from "../../serverCommunication/SIPServerUtils";
import * as actions from "../actions/phoneActions";
import {PHONE_STATUS} from "../../components/MainPage/Calling/PhoneStatus";
import {play, stop} from "../../components/MainPage/Calling/AudioPlayer";


export const phoneIntialState = {
    socket: undefined,
    ua: undefined,
    incomingCall: false,
    mounted: false,
    status: PHONE_STATUS.DISCONNECTED,
    session: null,
    incomingSession: null
};


export default function phoneReducer(state = phoneIntialState, action) {
    switch (action.type) {
        case actions.SET_UP:
            let userId = action.payload.userId;
            let username = action.payload.username;
            let socket = new JsSIP.WebSocketInterface(SIP_SERVER_URL);
            let uri = getUri(userId)
            let configuration = {
                sockets: [socket],
                uri: uri,
                display_name:username,
                session_timers: false
            };
            let ua = new JsSIP.UA(configuration);
            return {...state, socket: socket, ua: ua, status: PHONE_STATUS.DISCONNECTED, mounted: true};
        case actions.SET_SESSION:
            if (action.payload===null)  return {...state, session: action.payload,status: PHONE_STATUS.REGISTERED};
            return {...state, session: action.payload,status: PHONE_STATUS.CALLING};
        case actions.SET_INCOMING_SESSION:
            if (action.payload===null)  return {...state, session: action.payload,status: PHONE_STATUS.REGISTERED};
            return {...state, incomingSession: action.payload,status: PHONE_STATUS.INCOMING_CALL};
        case actions.START:
            let newUa = action.payload;
            newUa.start();
            return {...state, ua: newUa};

        case actions.SET_STATE:
            return {...state, status: action.payload};
        case actions.TOOGLE_MUTE:
            if (!state.session) return {...state};

            let nSession = state.session;
            if (nSession.isMuted().audio)  nSession.unmute();
            else nSession.mute();

            return {...state, session:nSession};

        case actions.CALL:
            let calling = action.payload;
            if (!state.ua) return state;

            const session = state.ua.call(calling,
                {
                    pcConfig:
                        {
                            rtcpMuxPolicy : 'negotiate',
                            iceServers    : []
                        },
                    mediaConstraints:
                        {
                            audio: true,
                            video: false
                        },
                    rtcOfferConstraints:
                        {
                            offerToReceiveAudio: 1,
                            offerToReceiveVideo: 0
                        }
                });
            return {...state,session: session};
        case actions.PICKUP:
            if (state.incomingSession!==null){
                state.incomingSession.answer()
                state.session=state.incomingSession
            }
            return {...state, session: state.session,status: PHONE_STATUS.IN_CALL};
        case actions.HANGUP:
            let curSes=state.session;
            let incSes=state.incomingSession;
            if (curSes){
                curSes.terminate();
                curSes=null;
            }
            if (incSes){
                incSes.terminate();
                incSes=null;
            }
            return {...state, session: curSes,incomingSession:incSes, status: PHONE_STATUS.REGISTERED};
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