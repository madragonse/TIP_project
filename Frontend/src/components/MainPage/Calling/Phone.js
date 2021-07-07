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
import {faPhone, faPhoneSlash, faMicrophoneSlash, faMicrophone} from "@fortawesome/free-solid-svg-icons";
import {Tooltip} from "react-bootstrap";
import Dots from "../../Common/Dots";

function Phone({dispatch, userId, username, ua, session, incomingSession, status}) {
    //i am aware this is quite a stupid way of going about it, wurks tho
    const [regListenersOn, setRegListenersOn] = useState(false);
    const [phoneListenersOn, setPhoneListenersOn] = useState(false);
    const [mounted, setMounted] = useState(true)
    const [callWidgetFeedback, setCallWidgetFeedback] = useState("")
    const pickupIcon = <FontAwesomeIcon icon={faPhone} style={{'color': 'var(--success-color)'}}/>;
    const hangupIcon = <FontAwesomeIcon icon={faPhoneSlash} style={{'color': 'var(--fail-color)'}}/>;
    const muteIcon = <FontAwesomeIcon icon={faMicrophoneSlash} style={{'color': 'var(--fail-color)'}}/>;
    const unmuteIcon = <FontAwesomeIcon icon={faMicrophone} style={{'color': 'var(--text-color)'}}/>;
    let remoteAudio = new window.Audio();
    remoteAudio.autoplay = true;
    remoteAudio.crossOrigin = "anonymous";

    useEffect(() => {
        setRegListenersOn(false);
        setMounted(true);
        dispatch(setUpPhone(userId, username))
    }, [])

    //set up phone registration listeners
    useEffect(() => {
        if (!ua) return;
        if (regListenersOn) return;

        setRegListenersOn(true);

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
            setCallWidgetFeedback(<div className="feedback error"><span>Error:&nbsp;</span> {data.cause}</div>);
            console.log({
                level: 'error',
                title: 'Registration failed',
                message: data.cause
            })
        });

        ua.on('newRTCSession', (data) => {
            if (!mounted) return

            if (SIP_DEBUGGING_MODE) console.log("New RTC session")
            if (SIP_DEBUGGING_MODE) console.log("1")
            //prevent user from calling himself
            if (data.originator === 'local')
            {
                if (SIP_DEBUGGING_MODE) console.log("1")
                return;
            }
                
            if (SIP_DEBUGGING_MODE) console.log("1")
            const newSession = data.session;
            if (SIP_DEBUGGING_MODE) console.log("1")
            // Avoid if busy or other incoming
            if (session || incomingSession) {
                newSession.terminate(
                    {
                        'status_code': 486,
                        'reason_phrase': 'Busy Here'
                    });
                dispatch(setPhoneIncomingSession(newSession));
                return;
            }
            if (SIP_DEBUGGING_MODE) console.log("1")

            play('ringing');

            newSession.on('failed', () => {
                stop('ringing');
                setTimeout(() => {
                    dispatch(setPhoneSession(null));
                    dispatch(setPhoneIncomingSession(null));
                }, 1000)

            });
            if (SIP_DEBUGGING_MODE) console.log("1")

            newSession.on('ended', () => {
                setTimeout(() => {
                    dispatch(setPhoneSession(null));
                    dispatch(setPhoneIncomingSession(null));
                }, 1000)
            });
            if (SIP_DEBUGGING_MODE) console.log("1")
            newSession.on('accepted', () => {
                setTimeout(() => {
                    dispatch(setPhoneSession(newSession));
                    dispatch(setPhoneIncomingSession(null));
                }, 1000)
                stop('ringing');
            });
            if (SIP_DEBUGGING_MODE) console.log("1")
            newSession.on('peerconnection', (e) => {
                console.log('peerconnection', e);
                const peerconnection = e.peerconnection;
                if (SIP_DEBUGGING_MODE) console.log("1")
                peerconnection.onaddstream = function (e) {
                    console.log('addstream', e);
                    remoteAudio.srcObject = e.stream;
                    remoteAudio.play();
                };
                if (SIP_DEBUGGING_MODE) console.log("1")
                let remoteStream = new MediaStream();
                console.log(peerconnection.getReceivers());
                peerconnection.getReceivers().forEach(function (receiver) {
                    console.log(receiver);
                    remoteStream.addTrack(receiver.track);
                });
            });
            
            dispatch(setPhoneIncomingSession(newSession));
        });
        dispatch(startPhone(ua));
    }, [ua])

    //set up phone call listeners
    useEffect(() => {
        if (!session) return;
        if (phoneListenersOn) return;

        setPhoneListenersOn(true);

        session.on('connecting', () => {
            play('ringback');
            setCallWidgetFeedback(<div className="feedback neutral"><span>Wait:&nbsp;</span>looking for user<Dots/>
            </div>);
        });

        session.on('progress', () => {
            play('ringback');
            setCallWidgetFeedback(<div className="feedback neutral"><span>Wait:&nbsp;</span>establishing
                connection<Dots/></div>);

            setTimeout(() => {
                dispatch(setPhoneState(PHONE_STATUS.CALLING))
            }, 1000)

        });

        session.connection.addEventListener('addstream', function (e) {
            remoteAudio.srcObject = e.stream;
        });
        
        session.on('failed', (data) => {
            stop('ringback');
            play('rejected');

            console.log(
                {
                    level: 'error',
                    title: 'Call failed',
                    message: data.cause
                });
            setCallWidgetFeedback(<div className="feedback error"><span>Fail:&nbsp;</span>User {data.cause}</div>);
            setTimeout(() => {
                dispatch(setPhoneState(PHONE_STATUS.REGISTERED))
                dispatch(setPhoneSession(null))
            }, 1000)

        });

        session.on('ended', () => {
            stop('ringback');
            setTimeout(() => {
                dispatch(setPhoneState(PHONE_STATUS.REGISTERED))
                dispatch(setPhoneSession(null))
            }, 1000)

        });

        session.on('accepted', () => {
            stop('ringback');
            play('answered');
            setTimeout(() => {
                dispatch(setPhoneState(PHONE_STATUS.IN_CALL))
            }, 1000)

        });

    }, [session]);

    function showHangupButton() {
        return status === PHONE_STATUS.IN_CALL || status === PHONE_STATUS.INCOMING_CALL || status === PHONE_STATUS.CALLING;
    }


    function isMuted() {
        if (!session) return false
        return session.isMuted().audio;
    }

    return (
        <div className="Phone">
            <div className="PhoneContainer">
                <PhoneStatus>

                    <CallWidget feedback={callWidgetFeedback}/>


                    <SessionInfo/>

                    <div className="phoneControls">

                        <CSSTransition
                            in={status === PHONE_STATUS.INCOMING_CALL}
                            classNames="fade"
                            unmountOnExit
                            timeout={0}
                        >
                            <button onClick={() => dispatch(pickUpPhone())}>
                                {pickupIcon}
                            </button>
                        </CSSTransition>

                        <CSSTransition
                            in={showHangupButton()}
                            classNames="fade"
                            unmountOnExit
                            timeout={0}
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
                            timeout={0}
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