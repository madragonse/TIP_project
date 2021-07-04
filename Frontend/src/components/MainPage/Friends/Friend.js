import React, {useEffect, useState} from "react";
import "./Friend.css"
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faPhone, faUserMinus, faUserPlus} from "@fortawesome/free-solid-svg-icons";
import {inviteFriend, modifyFriendship} from "../../../serverCommunication/FriendsService";
import {connect} from "react-redux";
import {removeFromFriendList} from "../../../redux/actions/friendsActions";
import {CSSTransition} from "react-transition-group";

export class FRIENDS_STATUS {
    static ACTIVE = new FRIENDS_STATUS("ACT", "Friends")
    static REQUESTED_SENT = new FRIENDS_STATUS("SREQ", "Request sent")
    static REQUESTED_RECEIVED = new FRIENDS_STATUS("RREQ", "Request received")
    static DECLINED = new FRIENDS_STATUS("DEC", "Request declined")

    constructor(text, desc) {
        this.text = text;
        this.desc = desc;
    }

    static statusFromText(text) {
        switch (text) {
            case "ACT":
                return FRIENDS_STATUS.ACTIVE;
            case "SREQ":
                return FRIENDS_STATUS.REQUESTED_SENT;
            case "RREQ":
                return FRIENDS_STATUS.REQUESTED_RECEIVED;
            case "DEC":
                return FRIENDS_STATUS.DECLINED;
            default:
                return FRIENDS_STATUS.DECLINED;
        }
    }
}

export const allStatuses = [
    FRIENDS_STATUS.ACTIVE,
    FRIENDS_STATUS.REQUESTED_RECEIVED,
    FRIENDS_STATUS.REQUESTED_SENT,
    FRIENDS_STATUS.DECLINED
]

function Friend({name, status,userId,dispatch}) {
    const callIcon = <FontAwesomeIcon icon={faPhone}/>;
    const removeIcon = <FontAwesomeIcon icon={faUserMinus}/>;
    const addIcon = <FontAwesomeIcon icon={faUserPlus}/>;
    const [showCall, setShowCall] = useState(false)
    const [showRemove, setShowRemove] = useState(false)
    const [showAdd, setShowAdd] = useState(false)
    const [visible,setVisible] = useState(true)


    useEffect(() => {
        setShowCall(false)
        setShowRemove(false)
        setShowAdd(false)

        if (status === FRIENDS_STATUS.ACTIVE) {
            setShowCall(true)
            setShowRemove(true)
        }
        else if (status === FRIENDS_STATUS.REQUESTED_RECEIVED) {
            setShowAdd(true)
            setShowRemove(true)
        }
        else if (status === FRIENDS_STATUS.REQUESTED_SENT) {
            setShowRemove(true)
        }
        else if (status === FRIENDS_STATUS.DECLINED) {
            setShowAdd(true)
        }

    }, [status])

    async function beginCall() {

    }

    async function invite(){
        await modifyFriendship(userId,name,"invite")
        setVisible(false)
    }

    async function remove(){
        await modifyFriendship(userId,name,"remove")
        dispatch(removeFromFriendList(name,status.text))
        setVisible(false)
    }


return (
        <CSSTransition
            in={visible}
            timeout={200}
            classNames="Friend"
            unmountOnExit
        >
            <div className="Friend">
                <div className="userInfo">
                    {name}
                </div>
                <div className="options">
                    {showCall &&
                    <span className="call" onClick={beginCall}>
                        {callIcon}
                    </span>}

                    {showAdd &&
                    <span className="invite" onClick={invite}>
                        {addIcon}
                    </span>}

                    {showRemove &&
                    <span className="remove" onClick={remove}>
                        {removeIcon}
                    </span>}
                </div>
            </div>
        </CSSTransition>
    );
}
let mapStateToProps = (state) => {
    return {
        userId: state.user.userId
    };
}
export default connect(mapStateToProps)(Friend)