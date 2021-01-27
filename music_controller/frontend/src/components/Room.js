// Handling the page once we create a room
import React, { Component } from 'react';

export default class Room extends Component {
    constructor(props){
        super(props);
        this.state = {
            votesToSkip: 2,
            guestCanPause: false,
            isHost: false,
        };
        // match is the prop that sorts all the information on how we got to this 
        // component from the React Router in HomePage.js
        // We can access the roomCode from the params (parameters) of the url
        this.roomCode = this.props.match.params.roomCode;
        // This will update the state and re render 
        // After the call the values will be updated
        this.getRoomDetails();
    }

    getRoomDetails(){
        // Making a call to the backend when we render /room/:codeRoom
        // We are actually setting the values of votesToSkip, guestCanPause and isHost
        // based on the data from the backend which is is stored in the data variable
        fetch('/api/get-room' + '?code=' + this.roomCode).then((response) => 
            response.json())
            .then((data) => {
            this.setState({
                votesToSkip: data.votes_to_skip,
                guestCanPause: data.guest_can_pause,
                isHost: data.is_host,
            });
        });
    }

    render(){
        return (
        <div>
            <h3>{this.roomCode}</h3>
            <p>Votes: {this.state.votesToSkip}</p>
            <p>Guest Can Pause: {this.state.guestCanPause.toString()}</p>
            <p>Host: {this.state.isHost.toString()}</p>
        </div>
        );
    }
}