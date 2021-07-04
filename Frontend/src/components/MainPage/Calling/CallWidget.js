import {connect} from "react-redux";
import React, {useState} from "react";
import "./CallWidget.css"
import audioPlayer from './AudioPlayer';
import * as JsSIP from "jssip";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faPhone} from "@fortawesome/free-solid-svg-icons";
import {PHONE_STATUS} from "./PhoneStatus";
import {call, setPhoneIncomingSession} from "../../../redux/actions/phoneActions";

function CallWidget({status,dispatch}){
    const [uri,setUri]=useState("")
    const [feedbackMessage,setFeedbackMsg]=useState("")


    function HandleSubmit(e){
        e.preventDefault();
        //dispatch call event
        dispatch(call(uri))
        //test incoming call

    }

    function handleInput(input){
        setFeedbackMsg("")
        setUri(input)
    }

    return (
        <div>
            { status===PHONE_STATUS.REGISTERED &&
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
            }
        </div>
    );
}
let mapStateToProps = (state)=>{
    return {
        status: state.phone.status
    };
}

export default connect(mapStateToProps)(CallWidget);