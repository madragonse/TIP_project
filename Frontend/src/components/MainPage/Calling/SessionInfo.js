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
    const {timer, timeRunOut, timerRestart} = useTimer(0,1);//dev
    // var {timer, timeRunOut, timerRestart} = useTimer(SIP_MAX_INVITE_WAIT_TIME,-1);
    // const timer_down = timer;
    // const timeRunOut_down = timeRunOut;
    // const timerRestart_down = timerRestart;
    // var {timer} = useTimer(0,1);
    // const timer_up = timer;


    // var res = useTimer(SIP_MAX_INVITE_WAIT_TIME, -1);
    // console.log(res)
    // const timerRestart = res["timerRestart"]
    // const timer = res["timer"]
    // const timeRunOut = res["timeRunOut"]

    // var res2 = useTimer(0,1);
    // console.log(res2)
    // const timerRestart2 = res2["timerRestart"]
    // const timer2 = res2["timer"]
    // const timeRunOut2 = res2["timeRunOut"]


    useEffect(()=>{
        timerRestart();
    },[session])

    //if calling timer has run out on client side, abort the call
    useEffect(()=>{
        if (timeRunOut){
            //dispatch(hangUpPhone())//dev
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
                    <h2>calling&nbsp;
                       {session ? session.remote_identity.uri.user:""}
                    </h2>

                    <div className="timer">
                        <Reel  theme={theme}
                               text={formatTimeMinutes(timer)+"s"}
                        />
                        <h3>current waiting time</h3>
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
                    <h2>with&nbsp;
                        {session ? session.remote_identity.display_name:""}
                    </h2>

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
                    <h2>from&nbsp;
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