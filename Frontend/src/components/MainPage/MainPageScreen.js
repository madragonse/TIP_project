import React from "react";
import FriendList from "./Friends/FriendList";
import CallWidget from "./Calling/CallWidget";
import AddFriend from "./Friends/AddFriend";
import "./MainPageScreen.css"

export default function MainPageScreen() {

    return (
        <div className="MainPageScreen">
            <div className="friendsContainer">
                <FriendList/>
                <AddFriend/>
            </div>

            <div className="callContainer">
                <CallWidget/>
            </div>
        </div>
    );
}