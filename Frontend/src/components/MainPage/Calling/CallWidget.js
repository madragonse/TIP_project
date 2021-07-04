import {connect} from "react-redux";
import React, {useState} from "react";
import "./CallWidget.css"
import audioPlayer from './AudioPlayer';
import * as JsSIP from "jssip";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faPhone} from "@fortawesome/free-solid-svg-icons";

function CallWidget({inCall}){
    const [uri,setUri]=useState("")
    const [feedbackMessage,setFeedbackMsg]=useState("")
    const callIcon = <FontAwesomeIcon icon={faPhone}/>;

    function HandleSubmit(e){
        e.preventDefault();
        //dispatch call event
    }

    function handleInput(input){
        setFeedbackMsg("")
        setUri(input)
    }

    return (
        <div>
            {!inCall &&
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
                    <Button type="submit"> {callIcon}</Button>
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
        inCall: state.user.inCall
    };
}

export default connect(mapStateToProps)(CallWidget);