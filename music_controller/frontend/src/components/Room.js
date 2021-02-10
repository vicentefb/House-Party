// Handling the page once we create a room
import React, { Component } from 'react';
import { Grid, Button, Typography } from '@material-ui/core';
import { Link } from "react-router-dom";
import CreateRoomPage from './CreateRoomPage';
import MusicPlayer from "./MusicPlayer";

export default class Room extends Component {
    constructor(props){
        super(props);
        this.state = {
            votesToSkip: 2,
            guestCanPause: false,
            isHost: false,
            showSettings: false,
            spotifyAuthenticated: false,
            song: {},
        };
        // match is the prop that sorts all the information on how we got to this 
        // component from the React Router in HomePage.js
        // We can access the roomCode from the params (parameters) of the url
        this.roomCode = this.props.match.params.roomCode;
        this.leaveButtonPressed = this.leaveButtonPressed.bind(this);
        this.updateShowSettings = this.updateShowSettings.bind(this);
        this.renderSettingsButton = this.renderSettingsButton.bind(this);
        this.renderSettings = this.renderSettings.bind(this);
        this.getRoomDetails = this.getRoomDetails.bind(this);
        this.authenticateSpotify = this.authenticateSpotify.bind(this);
        // As soon as we get into a room, if we are the host we need to authenticate the spotify
        this.getCurrentSong = this.getCurrentSong.bind(this);
        this.getRoomDetails();
    }

    // We are going to call each second an point to get the state of the song
    componentDidMount(){
        this.interval = setInterval(this.getCurrentSong, 1000);
    }

    componentWillUnmount(){
        clearInterval(this.interval);
    }

    // This updates the values to whatever they are equal to at the moment
    getRoomDetails(){
        // Making a call to the backend when we render /room/:codeRoom
        // We are actually setting the values of votesToSkip, guestCanPause and isHost
        // based on the data from the backend which is is stored in the data variable
        // We need to make sure our response is ok, if our response is not ok we need to redirect the user to the homepage
        fetch('/api/get-room' + '?code=' + this.roomCode)
            .then((response) => {
                if(!response.ok){
                    // If we are in a room that doesn't exist
                    // This will clear the state of roomcode in the homepage
                    this.props.leaveRoomCallback();
                    this.props.history.push('/');
                }
                return response.json();
            })
            .then((data) => {
            this.setState({
                votesToSkip: data.votes_to_skip,
                guestCanPause: data.guest_can_pause,
                isHost: data.is_host,
            });
            if(this.state.isHost){
                this.authenticateSpotify();
            }
        });
    }

    authenticateSpotify(){
        // data.url is the url returned from the backedn
        fetch("/spotify/is-authenticated")
            .then((response) => response.json())
            .then((data) => {
                this.setState({spotifyAuthenticated: data.status });
                console.log(data.status);
            if(!data.status){
                fetch('/spotify/get-auth-url')
                    .then((response) => response.json())
                    .then((data) => {
                    // redirect to us the Spotify authorization page, then callback then back to frontend
                    window.location.replace(data.url);
                });
            }
        });
    }

    // After we authenticate the user we call this function
    getCurrentSong() {
        fetch("/spotify/current-song")
          .then((response) => {
            if (!response.ok) {
              return {}
            } else {
              return response.json()
            }
          })
          .then((data) => {
            this.setState({ song: data });
            console.log(data);
          });
      }

    leaveButtonPressed(){
        // Call the endpoint that actually makes the button leave the room
        const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
        };
        fetch('/api/leave-room', requestOptions).then((_response) => {
            this.props.leaveRoomCallback();
            this.props.history.push('/');
        });
    }

    updateShowSettings(value){
        this.setState({
            showSettings: value,
        });
    }

    // render the settings page
    // This tells the CreateRoomPage to be in update mode not create mode <CreateRoomPage update={true}>
    renderSettings(){
        return (
        <Grid container spacing={1}>
            <Grid item xs={12} align="center">
                <CreateRoomPage 
                    update={true} 
                    votesToSkip={this.state.votesToSkip} 
                    guestCanPause={this.state.guestCanPause} 
                    roomCode={this.roomCode}
                    updateCallback={this.getRoomDetails}
                    />
            </Grid>
            <Grid item xs={12} align="center">
                <Button 
                    variant="contained" 
                    color="secondary" 
                    onClick={() => this.updateShowSettings(false)}
                > 
                    Close
                </Button>
            </Grid>
        </Grid>
        );
    }

    // Methods that returns the html to render the button
    renderSettingsButton(){
        return(
            <Grid item xs={12} align="center">
                <Button variant="contained" color="primary" onClick={() => this.updateShowSettings(true)}> 
                    Settings
                </Button>
            </Grid>
        );
    }

    // Want to render the main content if we are not showing the settings page
    render(){
        if(this.state.showSettings){
            return this.renderSettings();
        }
        return (
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <Typography variant="h4" component="h4">
                        Code: {this.roomCode}
                    </Typography>
                </Grid>
                <MusicPlayer {...this.state.song} />
                {this.state.isHost ? this.renderSettingsButton():null}
                <Grid item xs={12} align="center">
                    <Button color="secondary" variant="contained" onClick={this.leaveButtonPressed}>
                        Leave Room
                    </Button>
                </Grid>
            </Grid>
        );
    }
}