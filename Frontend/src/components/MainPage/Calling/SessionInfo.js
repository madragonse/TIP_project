import {connect} from "react-redux";
import {CSSTransition} from "react-transition-group";
import "./SessionInfo.css"

function SessionInfo({session,incomingSession}){
    //timer if in call
    //incoming call from whom
    let callerName
    return (
        <div className="SessionInfo">
            <CSSTransition
                in={session!==null}
                timeout={200}
                classNames="currentSessionInfo"
                unmountOnExit
            >
                <div className="currentSessionInfo">
                    <h1>current session info</h1>
                </div>

            </CSSTransition>

            <CSSTransition
                in={incomingSession!==null}
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