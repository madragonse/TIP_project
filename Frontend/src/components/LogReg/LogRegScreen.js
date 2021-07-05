import React from "react";
import Section from "../Common/Section";
import LoginForm from "./SubComponents/LoginForm";
import RegisterForm from "./SubComponents/RegisterForm";
import "./LogRegScreen.css"
import CallWidget from "../MainPage/Calling/CallWidget";
export default function LogRegScreen() {

    return (
        <div>
            <Section>
                <div className="LogRegScreen">
                    <LoginForm id="LOGIN"/>
                    <RegisterForm id="REGISTER"/>
                </div>
            </Section>
        </div>
    );
}