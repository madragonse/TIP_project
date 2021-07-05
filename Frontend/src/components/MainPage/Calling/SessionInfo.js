import {connect} from "react-redux";
import {CSSTransition} from "react-transition-group";
import "./SessionInfo.css"
import useTimer from "../../Common/Timer";
import Reel from "react-reel";
import {formatTimeMinutes} from "../../../Utils";
import {useEffect} from "react";
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
    let callingName="someone";
    const {timer, timeRunOut, timerRestart} = useTimer(SIP_MAX_INVITE_WAIT_TIME,-1);

    useEffect(()=>{
        timerRestart();
    },[session])

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
            >

                <div className="currentSessionInfo">
                    <h2>calling&nbsp;
                       {session ? session.remote_identity.uri.user:""}
                    </h2>

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
            >

                <div className="currentSessionInfo inCall">
                    <h2>with&nbsp;
                        {session ? session.remote_identity.uri.user:""}
                    </h2>

                    <div className="timer">
                        <Reel  theme={theme}
                               text={formatTimeMinutes(1000)+"s"}
                        />
                        <h3>current call time</h3>
                    </div>

                </div>

            </CSSTransition>

            <CSSTransition
                in={status===PHONE_STATUS.INCOMING_CALL}
                classNames="fade"
                unmountOnExit
            >
                <div className="incomingSessionInfo">
                    <h2>from
                        {incomingSession ? incomingSession.remote_identity.uri.user:""}</h2>
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