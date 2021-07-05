import React from "react";
import FriendList from "./Friends/FriendList";
import AddFriend from "./Friends/AddFriend";
import "./MainPageScreen.css"
import Phone from "./Calling/Phone";
import TransitionAppear from "../Common/TransitionAppear";

export default function MainPageScreen() {

    return (
        <TransitionAppear duration={1000}>
            <div className="MainPageScreen">
                <div className="friendsContainer">
                    <FriendList/>
                    <AddFriend/>
                </div>

                <Phone/>

            </div>
        </TransitionAppear>
    );
}