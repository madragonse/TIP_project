import CallWidget from "./CallWidget";
import {useEffect, useState} from "react";
import {connect} from "react-redux";
import {
    setPhoneIncomingSession,
    setPhoneMounted, setPhoneSession,
    setPhoneState,
    setUpPhone,
    startPhone
} from "../../../redux/actions/phoneActions";
import {play,initialize,stop} from "./AudioPlayer";
import {SIP_DEBUGGING_MODE} from "../../../serverCommunication/SIPServerUtils";
import PhoneStatus, {PHONE_STATUS} from "./PhoneStatus";
import "./Phone.css"
import SessionInfo from "./SessionInfo";


function Phone({dispatch,userId,ua,mounted,session,incomingSession,status}){
    const [listenersOn,setListenersOn]=useState(false);

    useEffect(()=>{
        setListenersOn(false);
        dispatch(setPhoneMounted(true));
        dispatch(setUpPhone(userId))
    },[])


    useEffect(()=>{
        if (!ua) return;
        if (listenersOn) return;

        setListenersOn(true);

        ua.on('connected', () =>
        {
            if (!mounted) return
            dispatch(setPhoneState(PHONE_STATUS.CONNECTED))
            if (SIP_DEBUGGING_MODE) console.log("CONNECTED")
        });

        ua.on('disconnected', () =>
        {
            if (!mounted) return
            dispatch(setPhoneState(PHONE_STATUS.DISCONNECTED))
            if (SIP_DEBUGGING_MODE) console.log("DISCONNECTED")
        });

        ua.on('registered', () =>
        {
            if (!mounted) return
            dispatch(setPhoneState(PHONE_STATUS.REGISTERED))
            if (SIP_DEBUGGING_MODE) console.log("REGISTERED")
        });

        ua.on('unregistered', () =>
        {
            if (!mounted) return
            if (SIP_DEBUGGING_MODE) console.log("UNREGISTERED")
            if (ua.isConnected()) dispatch(setPhoneState(PHONE_STATUS.CONNECTED))
            else dispatch(setPhoneState(PHONE_STATUS.DISCONNECTED))
        });

        ua.on('registrationFailed', (data) =>
        {
            if (!mounted) return

            if (ua.isConnected()) dispatch(setPhoneState(PHONE_STATUS.CONNECTED));
            else dispatch(setPhoneState(PHONE_STATUS.DISCONNECTED));

            console.log(   {
                level   : 'error',
                title   : 'Registration failed',
                message : data.cause
            })
        });

        ua.on('newRTCSession', (data) =>
        {
            if (!mounted) return

            if (SIP_DEBUGGING_MODE) console.log("New RTC session")

            //prevent user from calling himself
            if (data.originator === 'local')
                return;

            const newSession = data.session;

            // Avoid if busy or other incoming
            if (session || incomingSession)
            {
                newSession.terminate(
                    {
                        'status_code'   : 486,
                        'reason_phrase' : 'Busy Here'
                    });
                return;
            }

            play('ringing');
            dispatch(setPhoneIncomingSession(newSession));

            newSession.on('failed', () =>
            {
                stop('ringing');
                dispatch(setPhoneSession(null));
                dispatch(setPhoneIncomingSession(null));
            });

            newSession.on('ended', () =>
            {
                dispatch(setPhoneSession(null));
                dispatch(setPhoneIncomingSession(null));
            });

            newSession.on('accepted', () =>
            {
                stop('ringing');
                dispatch(setPhoneSession(newSession));
                dispatch(setPhoneIncomingSession(null));
            });
        });
        dispatch(startPhone(ua));
    },[ua])

    return (
      <div className="Phone">
          <div className="PhoneContainer">
              <PhoneStatus>
                  <CallWidget/>
                  <SessionInfo/>
              </PhoneStatus>
              <div>
                  <button onClick={()=>dispatch(setPhoneSession())}>simumalte call</button>
                  <button onClick={()=>dispatch(setPhoneIncomingSession())}>simumalte incoming call</button>
                  <button onClick={()=>dispatch(setPhoneSession(null))}>end call</button>
              </div>

          </div>

      </div>
    );
}


let mapStateToProps = (state) => {
    return {
        userId: state.user.userId,
        ua: state.phone.ua,
        mounted: state.phone.mounted,
        status:state.phone.status,
        session:state.phone.session,
        incomingSession: state.phone.incomingSession
    };
}


export default connect(mapStateToProps)(Phone)