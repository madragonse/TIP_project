import {connect} from "react-redux";
import {CSSTransition} from "react-transition-group";
import "./SessionInfo.css"
import useTimer from "../../Common/Timer";
import Reel from "react-reel";
import {formatTimeMinutes} from "../../../Utils";
import {useEffect, useState} from "react";
import {SIP_MAX_INVITE_WAIT_TIME} from "../../../serverCommunication/SIPServerUtils";
import {hangUpPhone} from "../../../redux/actions/phoneActions";
import {PHONE_STATUS} from "./PhoneStatus";

//used for timer
const theme = {
    reel: {
        height: "1em",
        display: "flex",
        alignItems: "flex-end",
        overflowY: "hidden",
        lineHeight: "0.95em"
    },
    group: {
        transitionDelay: "0ms",
        transitionTimingFunction: "ease-in-out",
        transform: "translate(0, 0)",
        height: "2em"
    },
    number: {
        height: "1em"
    }
};




function SessionInfo({status,session,incomingSession,dispatch}){
    //timer if in call
    //incoming call from whom
    const [displayName,setDisplayName]=useState("someone");
    const {timer, timeRunOut, timerRestart,setInitialTime,setTimerDirection} = useTimer(SIP_MAX_INVITE_WAIT_TIME,-1);


    useEffect(()=>{
        timerRestart();
        //if it's a call timer set it to count up
        if (status===PHONE_STATUS.IN_CALL){
            setInitialTime(0)
            setTimerDirection(1)
            return
        }

        setInitialTime(SIP_MAX_INVITE_WAIT_TIME)
        setTimerDirection(-1)

        //display name
        let temp_name=""
        if (incomingSession){
            temp_name=incomingSession.remote_identity.display_name
            if (!temp_name || temp_name ===""){
                temp_name=incomingSession.remote_identity.uri.user
            }
        }
        if (session){
            temp_name=session.remote_identity.display_name
            if (!temp_name || temp_name ===""){
                temp_name=session.remote_identity.uri.user
            }
        }
        setDisplayName(temp_name)
    },[status])

    //if calling timer has run out on client side, abort the call
    useEffect(()=>{
        if (timeRunOut){
            dispatch(hangUpPhone())
        }
    },[timeRunOut])

    return (
        <div className="SessionInfo">

            <CSSTransition
                in={status===PHONE_STATUS.CALLING}
                classNames="fade"
                unmountOnExit
                timeout={0}
            >

                <div className="currentSessionInfo">
                    <h2>calling&nbsp;{displayName}</h2>

                    <div className="timer">
                        <Reel  theme={theme}
                               text={formatTimeMinutes(timer)+"s"}
                        />
                        <h3>wait time remaining</h3>
                    </div>

                </div>

            </CSSTransition>


            <CSSTransition
                in={status===PHONE_STATUS.IN_CALL}
                classNames="fade"
                unmountOnExit
                timeout={0}
            >

                <div className="currentSessionInfo inCall">
                    <h2>with&nbsp;{displayName}</h2>

                    <div className="timer">
                        <Reel  theme={theme}
                               text={formatTimeMinutes(timer)+"s"}
                        />
                        <h3>current call time</h3>
                    </div>

                </div>

            </CSSTransition>

            <CSSTransition
                in={status===PHONE_STATUS.INCOMING_CALL}
                classNames="fade"
                unmountOnExit
                timeout={0}
            >
                <div className="incomingSessionInfo">
                    <h2>from&nbsp;{displayName}</h2>
                </div>
            </CSSTransition>
        </div>
    )
}



let mapStateToProps = (state) => {
    return {
        status:state.phone.status,
        session:state.phone.session,
        incomingSession:state.phone.incomingSession
    };
}
export default connect(mapStateToProps)(SessionInfo)