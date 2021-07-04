import {connect} from "react-redux";
import {useState} from "react";
import "./CallWidget.css"
import audioPlayer from './AudioPlayer';
import * as JsSIP from "jssip";

function CallWidget({inCallR}){
    const [inCall,setInCall]= useState(inCallR);

    let socket = new JsSIP.WebSocketInterface('ws://127.0.0.1:5001');
    let configuration = {
        sockets  : [ socket ],
        uri      : 'sip:alice@example.com',
        password : 'superpassword'
    };
    let ua = new JsSIP.UA(configuration);
    JsSIP.debug.enable('JsSIP:*');
    ua.start();
    // //ua.register();
    //
    //
    // // Register callbacks to desired call events
    // let eventHandlers = {
    //     'progress': function(e) {
    //         console.log('call is in progress');
    //     },
    //     'failed': function(e) {
    //         audioPlayer.stop('calling')
    //         console.log('call failed with cause: '+ e.data.cause);
    //     },
    //     'ended': function(e) {
    //         console.log('call ended with cause: '+ e.data.cause);
    //     },
    //     'confirmed': function(e) {
    //         console.log('call confirmed');
    //     }
    // };
    //
    // let options = {
    //     'eventHandlers'    : eventHandlers,
    //     'mediaConstraints' : { 'audio': true, 'video': true }
    // };


    function startACall(){
        // console.log("CONNECTING")
        // const socket = new WebSocket('ws://localhost:5001');
        // socket.addEventListener('message', function (event) {
        //     console.log('WebSocket message: ', event);
        // });
        // socket.addEventListener('error', function (event) {
        //     console.log('WebSocket error: ', event);
        // });
        // socket.addEventListener('open', function (event) {
        //     socket.send("Otworzylo mnie")
        //     console.log('WebSocket open: ', event);
        // });
        //audioPlayer.play('calling')
        // let session = ua.call('sip:bob@example.com', options);
    }

    return (
        <div className="CallWidget">
            <h1>Call Me If you get lost</h1>
            {inCall}
            <button onClick={startACall}>CALL ME SOMETIME</button>

        </div>
    );
}
let mapStateToProps = (state)=>{
    return {
        inCall: state.user.inCall
    };
}

export default connect(mapStateToProps)(CallWidget);