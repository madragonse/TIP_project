import CallWidget from "./CallWidget";
import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import {
    call, hangUpPhone, pickUpPhone,
    setPhoneIncomingSession,
    setPhoneSession,
    setPhoneState,
    setUpPhone,
    startPhone, togglePhoneMute, tooglePhoneMute
} from "../../../redux/actions/phoneActions";
import {play, initialize, stop} from "./AudioPlayer";
import {SIP_DEBUGGING_MODE} from "../../../serverCommunication/SIPServerUtils";
import PhoneStatus, {PHONE_STATUS} from "./PhoneStatus";
import "./Phone.css"
import SessionInfo from "./SessionInfo";
import {CSSTransition} from "react-transition-group";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faPhone, faPhoneSlash,faMicrophoneSlash,faMicrophone} from "@fortawesome/free-solid-svg-icons";
import {Tooltip} from "react-bootstrap";

function Phone({dispatch, userId,username, ua, session, incomingSession, status}) {
    const [listenersOn, setListenersOn] = useState(false);
    const [mounted, setMounted] = useState(true)
    const pickupIcon = <FontAwesomeIcon icon={faPhone} style={{'color':'var(--success-color)'}}/>;
    const hangupIcon = <FontAwesomeIcon icon={faPhoneSlash} style={{'color':'var(--fail-color)'}}/>;
    const muteIcon =  <FontAwesomeIcon icon={faMicrophoneSlash} style={{'color':'var(--fail-color)'}}/>;
    const unmuteIcon =  <FontAwesomeIcon icon={faMicrophone} style={{'color':'var(--text-color)'}}/>;

    useEffect(() => {
        setListenersOn(false);
        setMounted(true);
        dispatch(setUpPhone(userId,username))
    }, [])

    //set up phone listeners
    useEffect(() => {
        if (!ua) return;
        if (listenersOn) return;

        setListenersOn(true);

        ua.on('connected', () => {
            if (!mounted) return
            dispatch(setPhoneState(PHONE_STATUS.CONNECTED))
            if (SIP_DEBUGGING_MODE) console.log("CONNECTED")
        });

        ua.on('disconnected', () => {
            if (!mounted) return
            dispatch(setPhoneState(PHONE_STATUS.DISCONNECTED))
            if (SIP_DEBUGGING_MODE) console.log("DISCONNECTED")
        });

        ua.on('registered', () => {
            if (!mounted) return
            dispatch(setPhoneState(PHONE_STATUS.REGISTERED))
            if (SIP_DEBUGGING_MODE) console.log("REGISTERED")
        });

        ua.on('unregistered', () => {
            if (!mounted) return
            if (SIP_DEBUGGING_MODE) console.log("UNREGISTERED")
            if (ua.isConnected()) dispatch(setPhoneState(PHONE_STATUS.CONNECTED))
            else dispatch(setPhoneState(PHONE_STATUS.DISCONNECTED))
        });

        ua.on('registrationFailed', (data) => {
            if (!mounted) return

            if (ua.isConnected()) dispatch(setPhoneState(PHONE_STATUS.CONNECTED));
            else dispatch(setPhoneState(PHONE_STATUS.DISCONNECTED));

            console.log({
                level: 'error',
                title: 'Registration failed',
                message: data.cause
            })
        });

        ua.on('newRTCSession', (data) => {
            if (!mounted) return

            if (SIP_DEBUGGING_MODE) console.log("New RTC session")

            //prevent user from calling himself
            if (data.originator === 'local')
                return;

            const newSession = data.session;

            // Avoid if busy or other incoming
            if (session || incomingSession) {
                newSession.terminate(
                    {
                        'status_code': 486,
                        'reason_phrase': 'Busy Here'
                    });
                return;
            }

            play('ringing');
            dispatch(setPhoneIncomingSession(newSession));

            newSession.on('failed', () => {
                stop('ringing');
                dispatch(setPhoneSession(null));
                dispatch(setPhoneIncomingSession(null));
            });

            newSession.on('ended', () => {
                dispatch(setPhoneSession(null));
                dispatch(setPhoneIncomingSession(null));
            });

            newSession.on('accepted', () => {
                stop('ringing');
                dispatch(setPhoneSession(newSession));
                dispatch(setPhoneIncomingSession(null));
            });
        });
        dispatch(startPhone(ua));
    }, [ua])

    function showHangupButton() {
        return status === PHONE_STATUS.IN_CALL || status === PHONE_STATUS.INCOMING_CALL || status === PHONE_STATUS.CALLING;
    }

    function isMuted(){
        if (!session) return false
        return session.isMuted().audio;
    }



    return (
        <div className="Phone">
            <div className="PhoneContainer">
                <PhoneStatus>

                    <CallWidget/>

                    <SessionInfo/>

                    <div className="phoneControls">

                        <CSSTransition
                            in={status===PHONE_STATUS.INCOMING_CALL}
                            classNames="fade"
                            unmountOnExit
                        >
                            <button onClick={() => dispatch(pickUpPhone())}>
                                {pickupIcon}
                            </button>
                        </CSSTransition>

                        <CSSTransition
                            in={showHangupButton()}
                            classNames="fade"
                            unmountOnExit
                        >
                            <Tooltip title="hangup the phone">
                                <button onClick={() => dispatch(hangUpPhone())}>
                                    {hangupIcon}
                                </button>
                            </Tooltip>

                        </CSSTransition>

                        <CSSTransition
                            in={status === PHONE_STATUS.IN_CALL}
                            classNames="fade"
                            unmountOnExit
                        >
                            <button onClick={() => dispatch(togglePhoneMute())}>

                                {isMuted() &&
                                <Tooltip title="click to unmute">
                                    {muteIcon}
                                </Tooltip>}

                                {!isMuted() &&
                                <Tooltip title="click to mute">
                                    {unmuteIcon}
                                </Tooltip>}

                            </button>
                        </CSSTransition>

                    </div>
                </PhoneStatus>

                {SIP_DEBUGGING_MODE && <div>
                    <button onClick={() => dispatch(call("test123"))}>simulate call</button>
                    <button onClick={() => dispatch(setPhoneIncomingSession())}>simulate incoming call</button>
                    <button onClick={() => dispatch(hangUpPhone())}>end call</button>
                </div>

                }
            </div>

        </div>
    );
}


let mapStateToProps = (state) => {
    return {
        userId: state.user.userId,
        username: state.user.username,
        ua: state.phone.ua,
        mounted: state.phone.mounted,
        status: state.phone.status,
        session: state.phone.session,
        incomingSession: state.phone.incomingSession
    };
}


export default connect(mapStateToProps)(Phone)