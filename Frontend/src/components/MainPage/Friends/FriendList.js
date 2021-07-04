import {connect} from "react-redux";
import React, {useEffect, useState} from "react";
import Friend, {allStatuses, FRIENDS_STATUS} from "./Friend";
import {getFriends} from "../../../serverCommunication/FriendsService";
import "./FriendList.css"
import {setFriendList} from "../../../redux/actions/friendsActions";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faArrowCircleRight} from "@fortawesome/free-solid-svg-icons";
import {faArrowCircleLeft} from "@fortawesome/free-solid-svg-icons";

function FriendList({userId, dispatch, actList, decList, rreqList, sreqList}) {
    const [chosenStatus, setChosenStatus] = useState(FRIENDS_STATUS.ACTIVE);
    const [friends,setFriends]= useState([]);
    const [page, setPage] = useState(0);
    const [maxPage,setMaxPage]= useState(1)
    const [pageLength, setPageLength] = useState(4);
    const [loading, setLoading] = useState(true);
    const rightIcon = <FontAwesomeIcon icon={faArrowCircleRight}/>;
    const leftIcon = <FontAwesomeIcon icon={faArrowCircleLeft}/>;

    async function fetchFriends() {
        setLoading(true);
        let resp = await getFriends(userId, chosenStatus.text, page, pageLength);
        if (resp === undefined) return

        let friendsArr = JSON.parse(resp.friends);
        if (friendsArr.length === 0 || !Array.isArray(friendsArr)) {
            //TODO handle empty friends list
            return;
        }

        let friendsList = friendsArr.map(
            item => {
                return <Friend name={item.username} status={chosenStatus}/>;
            })

        dispatch(setFriendList(friendsList,chosenStatus.text))
        setLoading(false);
        setMaxPage(resp.maxPages);
    }

    //on status change, reset page counter and load new list
    useEffect(() => {
        setLoading(true);
        setFriends([])
        setPage(0)
        setMaxPage(1)
        fetchFriends().then();
    }, [chosenStatus])

    //on page changes, don't reset page counters
    useEffect(() => {
        setLoading(true);
        setFriends([])
        fetchFriends().then();
    }, [page, pageLength])


    useEffect(()=>{
        if (chosenStatus === FRIENDS_STATUS.ACTIVE) setFriends(actList);
        if (chosenStatus === FRIENDS_STATUS.REQUESTED_RECEIVED)  setFriends(rreqList);
        if (chosenStatus === FRIENDS_STATUS.REQUESTED_SENT)  setFriends(sreqList);
        if (chosenStatus === FRIENDS_STATUS.DECLINED)  setFriends(decList);
    },[actList,sreqList,rreqList,decList])


    function changePage(dir){
        let newPage=(page+dir)%maxPage;
        if (newPage<0) newPage=maxPage-1;
        setPage(newPage);
    }

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
            <div className="pageController">
                <button disabled={loading} onClick={()=>changePage(-1)}>{leftIcon}</button>
                {page+1}/{maxPage}
                <button disabled={loading} onClick={()=>changePage(1)}>{rightIcon}</button>
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