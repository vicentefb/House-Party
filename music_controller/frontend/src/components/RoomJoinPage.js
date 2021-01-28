import React, { Component } from 'react';
import { TextField, Button, Grid, Typography } from "@material-ui/core";
import { Link } from "react-router-dom";

export default class RoomJoinPage extends Component{
    constructor(props){
        // Call the constructor of component which is necessary
        super(props);
        // roomCode whatever it was typed into the text field
        // error will store the error message state
        this.state = {
            roomCode: "",
            error: "",
        };

        // We need to bind the method and set it inside the TextFiedl onChange event
        this.handleTextFieldChange = this.handleTextFieldChange.bind(this);
        this.roomButtonPressed = this.roomButtonPressed.bind(this);
    }

    // Text field that allows the user to type in a room code and then two buttons
    render(){
        return (
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <Typography variant="h4" component="h4">
                        Join a Room
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <TextField 
                        error={this.state.error}
                        label="Code"
                        placeholder="Enter a Room Code"
                        value={this.state.roomCode}
                        helperText={this.state.error}
                        variant="outlined"
                        onChange={this.handleTextFieldChange}
                    />
                </Grid>
                <Grid item xs={12} align="center">
                    <Button variant="contained" color="primary" onClick={this.roomButtonPressed}>
                        Enter Room
                    </Button>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button variant="contained" color="secondary" to="/" component={Link}>
                        Back
                    </Button>
                </Grid>
            </Grid>
        )
    }

    // Method to catch in what's inside the text field
    // This updates the state of roomCode
    handleTextFieldChange(e){
        this.setState({
            roomCode: e.target.value,
        });
    }

    // Send a POST request to the back-end saying
    // Hey I want to join this room, does it exist?
    // if it does, can we successfully join it
    roomButtonPressed(){
        const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                code: this.state.roomCode
            })
        };

        // if response.ok is true it means we successfully joined the room
        fetch('/api/join-room', requestOptions).then((response) => {
            if(response.ok){
                this.props.history.push(`/room/${this.state.roomCode}`)
            } else {
                this.setState({error:"Room not found. "})
            }
        }).catch((error) => {
            console.log(error);
        });
    }
}
