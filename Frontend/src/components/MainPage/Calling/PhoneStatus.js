import "./PhoneStatus.css"
import {connect} from "react-redux";
import Dots from "../../Common/Dots";
import {Tooltip} from "react-bootstrap";

export class PHONE_STATUS {
    static DISCONNECTED = new PHONE_STATUS("disconnected", <h2>Disconnected, attempting to reconnect<Dots/></h2>,"var(--fail-color)")
    static CONNECTED = new PHONE_STATUS("connected", <h2>Connected, awaiting registration<Dots/></h2>,"var(--primary-color)")
    static REGISTERED= new PHONE_STATUS("registered",<div><h1>ONLINE</h1><h2>Phone connected and ready for calls</h2></div>,"var(--success-color)")
    static CALLING= new PHONE_STATUS("calling",<h1>PLEASE HOLD</h1>,"var(--sec-color)")
    static INCOMING_CALL= new PHONE_STATUS("calling",<h1>INCOMING CALL</h1>,"var(--sec-color)")
    static IN_CALL= new PHONE_STATUS("inCall",<h1>IN CALL</h1>,"var(--success-color)")

    constructor(text, desc,color) {
        this.text = text;
        this.desc = desc;
        this.color= color;
    }
}

//TO DO in call displays
function PhoneStatus({status,children}){
    let borderGlowStyle={
        'boxShadow': 'inset 0 0 13px 6px var(--ring-color)'
    }

    let root = document.documentElement;
    root.style.setProperty('--ring-color', status.color);


    //modify ring speed depending on status
    if (status===PHONE_STATUS.REGISTERED){
        root.style.setProperty('--ring-speed', '2s');
    }
    if (status===PHONE_STATUS.IN_CALL || status===PHONE_STATUS.CONNECTED){
        root.style.setProperty('--ring-speed', '10s');
    }
    if (status===PHONE_STATUS.CALLING ||status===PHONE_STATUS.INCOMING_CALL  ){
        root.style.setProperty('--ring-speed', '0.7s');
    }

    return (
        <div className="PhoneStatus">
            <div  className="statusBand" style={{'backgroundColor': status.color}}>
                <div className="contentContainer" style={borderGlowStyle}>

                    {status.desc}
                    {children}
                </div>
            </div>
        </div>

    )
}

let mapStateToProps = (state) => {
    return {
        status:state.phone.status,
    };
}
export default connect(mapStateToProps)(PhoneStatus)