import React from "react";
import logo from "../../../assets/logo.png";
import "./LogoWidget.css";


export default function LogoWidget(){
    return (
        <div className="logo NavProfile" >
            <img src={logo} alt="website-logo"/>
            <div className="logo-texts">
                <h1>Mów@me</h1>
                <h3>Twój nowy telefon IP</h3>
            </div>
        </div>
    );
}
