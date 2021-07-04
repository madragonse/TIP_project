import {connect} from "react-redux";
import {useEffect, useState} from "react";
import Friend, {allStatuses, FRIENDS_STATUS} from "./Friend";
import {getFriends} from "../../../serverCommunication/FriendsService";
import "./FriendList.css"
import {setFriendList} from "../../../redux/actions/friendsActions";

function FriendList({userId, dispatch, actList, decList, rreqList, sreqList}) {
    const [chosenStatus, setChosenStatus] = useState(FRIENDS_STATUS.ACTIVE);
    const [friends,setFriends]= useState([]);
    const [page, setPage] = useState(0);
    const [pageLength, setPageLength] = useState(10);
    const [loading, setLoading] = useState(true);

    async function fetchFriends() {
        setLoading(true);
        let resp = await getFriends(userId, chosenStatus.text, page, pageLength);
        if (resp === undefined) return

        let respArr = JSON.parse(resp);
        if (respArr.length === 0 || !Array.isArray(respArr)) {
            //TODO handle empty friends list
            return;
        }

        let friendsList = respArr.map(
            item => {
                let status = FRIENDS_STATUS.statusFromText(item.status);
                return <Friend name={item.username} status={status}/>;
            })

        dispatch(setFriendList(friendsList,chosenStatus.text))
        setLoading(false);
    }


    useEffect(() => {
        setLoading(true);
        setFriends([])
        fetchFriends().then();
    }, [chosenStatus, page, pageLength])

    useEffect(()=>{
        if (chosenStatus === FRIENDS_STATUS.ACTIVE) setFriends(actList);
        if (chosenStatus === FRIENDS_STATUS.REQUESTED_RECEIVED)  setFriends(rreqList);
        if (chosenStatus === FRIENDS_STATUS.REQUESTED_SENT)  setFriends(sreqList);
        if (chosenStatus === FRIENDS_STATUS.DECLINED)  setFriends(decList);
    },[actList,sreqList,rreqList,decList])

    let chosenStyle = {
        'fontWeight': 'bold',
    }
    let notChosenStyle = {
        'fontWeight': 'normal',
    }
    let fullWidthStyle={
        'width':'100%'
    }
    return (
        <div className="FriendList">
            <div className="StatusChoice">
                {allStatuses.map((item => {
                    return (
                        <button
                            onClick={() => setChosenStatus(item)}
                            style={chosenStatus === item ? chosenStyle : notChosenStyle}
                        >
                            {item.desc}
                        </button>
                    );
                }))}
            </div>
            <div className="friendsContainer">
                {!loading && friends}
            </div>

        </div>
    );
}

let mapStateToProps = (state) => {
    return {
        userId: state.user.userId,
        actList: state.friends.actList,
        rreqList: state.friends.rreqList,
        sreqList: state.friends.sreqList,
        decList: state.friends.decList
    };
}

export default connect(mapStateToProps)(FriendList);