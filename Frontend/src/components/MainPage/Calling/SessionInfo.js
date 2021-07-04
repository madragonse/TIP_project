import {connect} from "react-redux";
import {CSSTransition} from "react-transition-group";
import "./SessionInfo.css"
import useTimer from "../../Common/Timer";
import Reel from "react-reel";
import {formatTime, formatTimeMinutes} from "../../../Utils";
import {useEffect} from "react";
import {SIP_MAX_INVITE_WAIT_TIME} from "../../../serverCommunication/SIPServerUtils";

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




function SessionInfo({session,incomingSession}){
    //timer if in call
    //incoming call from whom
    let callingName="someone";
    const {timer, timerRestart} = useTimer(SIP_MAX_INVITE_WAIT_TIME,-1);

    useEffect(()=>{
        timerRestart();
    },[session])


    return (
        <div className="SessionInfo">
            <CSSTransition
                in={session!==null && incomingSession==null}
                timeout={200}
                classNames="currentSessionInfo"
                unmountOnExit
            >

                <div className="currentSessionInfo">
                    <h2>calling {callingName}</h2>

                    <div className="timer">

                        <Reel  theme={theme}
                               text={formatTimeMinutes(timer)+"s"}
                        />
                        <h3>wait time remaining</h3>
                    </div>

                </div>

            </CSSTransition>

            <CSSTransition
                in={incomingSession!==null && session==null}
                timeout={200}
                classNames="incomingSessionInfo"
                unmountOnExit
            >
                <div className="incomingSessionInfo">
                    <h1>incoming session info</h1>
                </div>
            </CSSTransition>
        </div>
    )
}



let mapStateToProps = (state) => {
    return {
        session:state.phone.session,
        incomingSession:state.phone.incomingSession
    };
}
export default connect(mapStateToProps)(SessionInfo)