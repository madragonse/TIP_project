import CallWidget from "./CallWidget";
import {SIP_SERVER_URL} from "../../../serverCommunication/SIPServerUtils";
import * as JsSIP from "jssip";


function Phone(){
    let socket = new JsSIP.WebSocketInterface(SIP_SERVER_URL);
    let configuration = {
        sockets  : [ socket ],
        uri      : 'sip:alice@example.com',
        password : 'superpassword'
    };
    let ua = new JsSIP.UA(configuration);

    ua.start();
    return (
      <div className="Phone">
          <CallWidget/>
      </div>
    );
}


export default Phone