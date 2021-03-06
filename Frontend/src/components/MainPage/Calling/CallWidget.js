import {connect} from "react-redux";
import React, {useEffect, useState} from "react";
import "./CallWidget.css"
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import {PHONE_STATUS} from "./PhoneStatus";
import {call} from "../../../redux/actions/phoneActions";
import {CSSTransition} from "react-transition-group";

function CallWidget({status, dispatch,feedback}) {
    const [uri, setUri] = useState("")
    const [feedbackMessage,setFeedbackMessage]=useState("")


    function HandleSubmit(e) {
        e.preventDefault();
        //dispatch call event
        dispatch(call(uri))
        //test incoming call
    }

    useEffect(()=>{
        setFeedbackMessage(feedback)
    },[feedback])

    function handleInput(input) {
        setFeedbackMessage("")
        setUri(input)
    }

    return (
        <CSSTransition
            in={status === PHONE_STATUS.REGISTERED}
            classNames="fade"
            unmountOnExit
            timeout={0}
        >

            <div className="CallWidget">

                <Form onSubmit={HandleSubmit}>
                    <Form.Control
                        required
                        placeholder="username or uri"
                        autoFocus
                        type="text"
                        value={uri}
                        onChange={(e) => handleInput(e.target.value)}
                    />
                    <Button type="submit"> Call</Button>
                </Form>

                {feedbackMessage !== "" &&
                <span className="feedback">{feedbackMessage}</span>
                }
            </div>

        </CSSTransition>
    );
}

let mapStateToProps = (state) => {
    return {
        status: state.phone.status
    };
}

export default connect(mapStateToProps)(CallWidget);