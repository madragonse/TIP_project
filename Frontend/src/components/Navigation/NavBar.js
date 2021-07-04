import React, {Component} from 'react';
import "./NavBar.css";
import ProfileWidget from "./SubComponents/ProfileWidget"
import LogoWidget from "./SubComponents/LogoWidget"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSignOutAlt } from "@fortawesome/free-solid-svg-icons";
import {logout} from "../../serverCommunication/LogRegService";
import {connect} from "react-redux";
import {mapAllStateToProps} from "../../redux/reducers/rootReducer";

//buttons on different subpages
let landingPageItems = ["LOGIN", "REGISTER"];

class NavBar extends Component {
    constructor(props) {
        super(props);
        this.title = props.title;
        this.currentItems = landingPageItems;
        this.logoVisible=true;
        this.playerWidgetVisible=false;

    }

    scrollToSection(sectionID) {
        let section = document.getElementById(sectionID);
        if (typeof section !== 'undefined' && section !== null) {
            section.scrollIntoView({behavior: 'smooth'});
        }
    }

    getAppropriateItems(){
        let path= this.props.location.pathname;
        if (typeof path === 'undefined' || path === null) return

        this.currentItems = [];
        this.playerWidgetVisible=true;
        this.logoVisible=false;
        if(path==="/login"){
            this.currentItems = landingPageItems;
            this.playerWidgetVisible=false;
            this.logoVisible=true;
        }

        //update menu buttons
        this.menuItemsList = this.currentItems.map(item =>
            <button key={item} onClick={() => this.scrollToSection(item)}>
                {item}
            </button>);
    }



    render() {
        this.getAppropriateItems();

        return (
            <header className="NavBar">
                {this.logoVisible && <LogoWidget/>}
                {this.playerWidgetVisible && <ProfileWidget username={this.props.username}/>}

                {this.playerWidgetVisible &&this.logoutIcon}

                <div className="NavBar-buttons NavButtons" id="navButtons">
                    {this.menuItemsList}
                </div>
            </header>
        );

    }

}
let mapStateToProps = (state)=>{
    return {
        username: state.user.username
    };
}
export default connect(mapStateToProps)(NavBar);