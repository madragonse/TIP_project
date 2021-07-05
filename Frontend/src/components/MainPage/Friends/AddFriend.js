import React, {useState} from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import {inviteFriend, modifyFriendship} from "../../../serverCommunication/FriendsService";
import {connect} from "react-redux";
import "./AddFriend.css"
import {addToFriendList} from "../../../redux/actions/friendsActions";
import Friend, {FRIENDS_STATUS} from "./Friend";

function AddFriend({userId,dispatch}) {
    const [add, setAdd] = useState("");
    const [feedbackMessage, setFeedbackMessage] = useState("");

    async function HandleSubmit(event) {
        event.preventDefault();
        //reset error message
        if (feedbackMessage !== "") setFeedbackMessage("");

        let resp = await modifyFriendship(userId, add,"invite");
        if (resp === undefined) return;
        if (resp.error) {
            setFeedbackMessage(<div className="feedback error"><span>Error:&nbsp;</span> {resp.error}</div>);
            return;
        }
        setFeedbackMessage(<div className="feedback success"><span>Success:&nbsp;</span> {"Sent friend request to user " + add}</div>);
        setAdd("");
        dispatch(addToFriendList(<Friend name={add} status={FRIENDS_STATUS.REQUESTED_SENT}/>,'SREQ'))
    }
    function handleInput(toAdd){
        if (feedbackMessage !== "") setFeedbackMessage("");
        setAdd(toAdd);
    }
    return (
        <div className="AddFriend">
            <h2>Feeling lonely? Invite someone!</h2>
            <Form onSubmit={HandleSubmit}>
                <Form.Control
                    required
                    placeholder="Username or email..."
                    autoFocus
                    type="text"
                    value={add}
                    onChange={(e) => handleInput(e.target.value)}
                />
                <Button type="submit">Add friend</Button>
            </Form>
            {feedbackMessage !== "" &&
            <span className="feedback">{feedbackMessage}</span>
            }
        </div>
    );
}

let mapStateToProps = (state) => {
    return {
        userId: state.user.userId
    };
}
export default connect(mapStateToProps)(AddFriend)

