import React, {Component} from "react";
import "./ProfileWidget.css";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faSignOutAlt} from "@fortawesome/free-solid-svg-icons";
import {logout} from "../../../serverCommunication/LogRegService";


class ProfileWidget extends Component{
    constructor(props) {
        super(props);
        this.username=props.username;
        this.logoutIcon=<FontAwesomeIcon
            className="NavBar-signout"
            icon={faSignOutAlt}
            onClick={logout}
        />;
    }

    render() {
        return (
            <div className="NavBar-userProfile NavProfile">
                <div className="img"/>
                <div className="NavBar-userProfile-info">
                    <h1>PROFILE</h1>
                    <h3>{this.username} | {this.logoutIcon}</h3>
                </div>
            </div>
        );
    }


}
 export default ProfileWidget;